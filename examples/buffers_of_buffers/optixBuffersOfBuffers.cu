/* 
 * Copyright (c) 2016, NVIDIA CORPORATION. All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *  * Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *  * Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *  * Neither the name of NVIDIA CORPORATION nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include <optix_world.h>
#include "commonStructs.h"
#include "helpers.h"

struct PerRayData_radiance
{
  float3 result;
  float importance;
  int depth;
};

struct PerRayData_shadow
{
  float3 attenuation;
};


//
// Declaration of our Buffer of Buffers
//
rtBuffer<rtBufferId<uchar4, 2> > Kd_layers;

rtBuffer<BasicLight>                 lights;
rtDeclareVariable(float3,            ambient_light_color, , );
rtDeclareVariable(unsigned int,      radiance_ray_type, , );
rtDeclareVariable(unsigned int,      shadow_ray_type, , );
rtDeclareVariable(rtObject,          top_object, , );
rtDeclareVariable(rtObject,          top_shadower, , );
rtDeclareVariable(float,             scene_epsilon, , );

rtDeclareVariable(float3, geometric_normal, attribute geometric_normal, ); 
rtDeclareVariable(float3, shading_normal,   attribute shading_normal, ); 
rtDeclareVariable(float3, texcoord,         attribute texcoord, ); 

rtDeclareVariable(optix::Ray,          ray,        rtCurrentRay, );
rtDeclareVariable(float,               t_hit,      rtIntersectionDistance, );
rtDeclareVariable(PerRayData_radiance, prd,        rtPayload, );
rtDeclareVariable(PerRayData_shadow,   prd_shadow, rtPayload, );

RT_PROGRAM void any_hit_shadow()
{
  // this material is opaque, so it fully attenuates all shadow rays
  prd_shadow.attenuation = optix::make_float3(0.0f);
  rtTerminateRay();
}


RT_PROGRAM void closest_hit_radiance()
{
  float3 world_shading_normal = optix::normalize( 
      rtTransformNormal( RT_OBJECT_TO_WORLD, shading_normal ) );
  float3 world_geometric_normal = optix::normalize( 
      rtTransformNormal( RT_OBJECT_TO_WORLD, geometric_normal ) );
  float3 normal = optix::faceforward(
      world_shading_normal, -ray.direction, world_geometric_normal );

  float3 hit_point = ray.origin + t_hit * ray.direction;
  
  //
  // Calculate Kd - loop over all nested buffers, accumulating color
  //
  float3 Kd = make_float3( 1.0f ); 
  for( int i = 0; i < Kd_layers.size(); ++i )
  {
    // Grab a refernce to the nested buffer so we dont need to perform
    // the buffer lookup multiple times 
    rtBufferId<uchar4, 2>& layer = Kd_layers[i];

    optix::size_t2 size  = layer.size();
    uint2  idx  = make_uint2( min( texcoord.x*size.x, size.x-1.0f ),
                              min( texcoord.y*size.y, size.y-1.0f ) );
    uchar4 val  = layer[ idx ]; 
    float4 fval = make_float4( val.x / 256.0f,
                               val.y / 256.0f,
                               val.z / 256.0f,
                               val.w / 256.0f );
    Kd = make_float3( fval )*fval.w + Kd*(1.0f - fval.w );
  }

  // ambient contribution
  float3 result = Kd * ambient_light_color;

  // compute direct lighting
  unsigned int num_lights = lights.size();
  for(int i = 0; i < num_lights; ++i) {
    BasicLight light = lights[i];
    float Ldist = optix::length(light.pos - hit_point);
    float3 L = optix::normalize(light.pos - hit_point);
    float nDl = optix::dot( normal, L);

    // cast shadow ray
    float3 light_attenuation = make_float3(static_cast<float>( nDl > 0.0f ));
    if ( nDl > 0.0f && light.casts_shadow ) {
      PerRayData_shadow shadow_prd;
      shadow_prd.attenuation = make_float3(1.0f);
      optix::Ray shadow_ray = optix::make_Ray(
          hit_point, L, shadow_ray_type, scene_epsilon, Ldist );
      rtTrace(top_shadower, shadow_ray, shadow_prd);
      light_attenuation = shadow_prd.attenuation;
    }

    // If not completely shadowed, light the hit point
    if( fmaxf(light_attenuation) > 0.0f ) {
      float3 Lc = light.color * light_attenuation;
      result += Kd * nDl * Lc;
    }
  }

  // pass the color back up the tree
  prd.result = result;
}
