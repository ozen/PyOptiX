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

#include <optix.h>
#include <optixu/optixu_math_namespace.h>
#include <optixu/optixu_matrix_namespace.h>
#include <optixu/optixu_aabb_namespace.h>

#include "helpers.h"

using namespace optix;

rtDeclareVariable(float4, sphere, , );
rtDeclareVariable(float3, rotation, , );

rtDeclareVariable(float3, matrix_row_0, , );
rtDeclareVariable(float3, matrix_row_1, , );
rtDeclareVariable(float3, matrix_row_2, , );

rtDeclareVariable(optix::Ray, ray, rtCurrentRay, );

rtDeclareVariable(float3, texcoord, attribute texcoord, ); 
rtDeclareVariable(float3, geometric_normal, attribute geometric_normal, ); 
rtDeclareVariable(float3, shading_normal, attribute shading_normal, ); 

RT_PROGRAM void intersect(int primIdx)
{
  float3 center = make_float3(sphere);
  float3 O = ray.origin - center;
  float3 D = ray.direction;
  float radius = sphere.w;

  float b = dot(O, D);
  float c = dot(O, O)-radius*radius;
  float disc = b*b-c;
  if(disc > 0.0f){
    float sdisc = sqrtf(disc);
    float root1 = (-b - sdisc);
    bool check_second = true;
    if( rtPotentialIntersection( root1 ) ) {
      shading_normal = geometric_normal = (O + root1*D)/radius;

      float3 polar;
      polar.x = dot(matrix_row_0, geometric_normal);
      polar.y = dot(matrix_row_1, geometric_normal);
      polar.z = dot(matrix_row_2, geometric_normal);
      polar = optix::cart_to_pol(polar);

      texcoord = make_float3( polar.x*0.5f*M_1_PIf, (polar.y+M_PI_2f)*M_1_PIf, polar.z/radius );

      if(rtReportIntersection(0))
        check_second = false;
    } 
    if(check_second) {
      float root2 = (-b + sdisc);
      if( rtPotentialIntersection( root2 ) ) {
        shading_normal = geometric_normal = (O + root2*D)/radius;

        float3 polar;
        polar.x = dot(matrix_row_0, geometric_normal);
        polar.y = dot(matrix_row_1, geometric_normal);
        polar.z = dot(matrix_row_2, geometric_normal);
        polar = optix::cart_to_pol(polar);

        texcoord = make_float3( polar.x*0.5f*M_1_PIf, (polar.y+M_PI_2f)*M_1_PIf, polar.z/radius );

        rtReportIntersection(0);
      }
    }
  }
}

RT_PROGRAM void bounds (int, optix::Aabb* aabb)
{
  const float3 cen = make_float3( sphere );
  const float3 rad = make_float3( sphere.w );
  
  if( rad.x > 0.0f && !isinf(rad.x) ) {
    aabb->m_min = cen - rad;
    aabb->m_max = cen + rad;
  } else {
    aabb->invalidate();
  }
}

