import sys
from os.path import dirname
sys.path.append(dirname(dirname(dirname(__file__))))

import numpy as np
from PIL import Image
from pyoptix import Context, Compiler, Buffer, Program, Geometry, Material, GeometryInstance, EntryPoint, \
    GeometryGroup, Acceleration
from examples.common import ImageWindow, calculate_camera_variables

width = 1024
height = 768

Compiler.add_program_directory(dirname(__file__))


def main():
    context, entry_point = create_context()
    sphere = create_geometry()
    material = create_material()
    create_instance(context, sphere, material)

    entry_point.launch((width, height))
    result_array = context['output_buffer'].to_array()
    result_image = Image.fromarray(result_array)
    ImageWindow(result_image)

    context.pop()


def create_context():
    context = Context()

    context.set_ray_type_count(1)
    context['radiance_ray_type'] = np.array(0, dtype=np.uint32)
    context['scene_epsilon'] = np.array(1e-4, dtype=np.float32)
    context['output_buffer'] = Buffer.empty((height, width, 4), dtype=np.uint8, buffer_type='o', drop_last_dim=True)
    entry_point = EntryPoint(Program('pinhole_camera.cu', 'pinhole_camera'),
                             Program('pinhole_camera.cu', 'exception'))

    cam_eye = [0.0, 0.0, 5.0]
    lookat = [0.0, 0.0, 0.0]
    up = [0.0, 1.0, 0.0]
    hfov = 60.0
    aspect_ratio = width / height
    camera_u, camera_v, camera_w = calculate_camera_variables(cam_eye, lookat, up, hfov, aspect_ratio, True)

    context['eye'] = np.array(cam_eye, dtype=np.float32)
    context['U'] = np.array(camera_u, dtype=np.float32)
    context['V'] = np.array(camera_v, dtype=np.float32)
    context['W'] = np.array(camera_w, dtype=np.float32)

    context['bad_color'] = np.array([1.0, 0.0, 1.0], dtype=np.float32)
    context.set_miss_program(0, Program('constantbg.cu', 'miss'))
    context['bg_color'] = np.array([0.3, 0.1, 0.2], dtype=np.float32)

    return context, entry_point


def create_geometry():
    sphere = Geometry(Program('sphere.cu', 'bounds'), Program('sphere.cu', 'intersect'))
    sphere.set_primitive_count(1)
    sphere['sphere'] = np.array([0, 0, 0, 1.5], dtype=np.float32)
    return sphere


def create_material():
    return Material(closest_hit={
        0: Program('normal_shader.cu', 'closest_hit_radiance')
    })


def create_instance(context, sphere, material):
    instance = GeometryInstance(sphere, material)
    group = GeometryGroup(children=[instance])
    group.set_acceleration(Acceleration())
    context['top_object'] = group


if __name__ == '__main__':
    main()
