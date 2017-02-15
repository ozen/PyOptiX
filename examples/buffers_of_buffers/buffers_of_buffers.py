import sys
from os.path import dirname
sys.path.append(dirname(dirname(dirname(__file__))))

from random import random as randf
import numpy as np
from PIL import Image
from pyoptix import Context, Buffer, Program, EntryPoint, Geometry, Material, GeometryInstance, GeometryGroup, \
    Acceleration, Compiler
from examples.common import ImageWindow, calculate_camera_variables
from examples.buffers_of_buffers.common_structs import BasicLight


width = 512
height = 512

MAX_BUFFER_WIDTH = 64
MAX_BUFFER_HEIGHT = 32

Compiler.add_program_directory(dirname(__file__))


def create_random_buffer(max_width, max_height):
    scale = randf()
    w = int(max(max_width * scale, 1))
    h = int(max(max_height * scale, 1))

    arr = []
    red, green, blue = randf(), randf(), randf()

    for y in range(h):
        arr.append([])
        for x in range(w):
            if randf() < 0.1:
                arr[y].append([red * 255.0, green * 255.0, blue * 255.0, 255])
            else:
                arr[y].append([255, 255, 255, 0])

    return Buffer.from_array(np.array(arr, dtype=np.uint8), buffer_type='i', drop_last_dim=True)


def create_context():
    context = Context()

    context.set_ray_type_count(2)
    context.set_stack_size(1200)
    context.set_print_enabled(True)
    context.set_all_exceptions_enabled(True)

    # here pyoptix won't be able to deduce types of these variables,
    # so we must put them inside numpy arrays with proper dtypes
    context['max_depth'] = np.array(5, dtype=np.int32)
    context['radiance_ray_type'] = np.array(0, dtype=np.uint32)
    context['shadow_ray_type'] = np.array(1, dtype=np.uint32)
    context['scene_epsilon'] = np.array(1e-4, dtype=np.float32)

    context['output_buffer'] = Buffer.empty((height, width, 4), dtype=np.uint8, buffer_type='o', drop_last_dim=True)

    cam_eye = [2.0, 1.5, -2.0]
    lookat = [0.0, 1.2, 0.0]
    up = [0.0, 1.0, 0.0]
    hfov = 60.0
    aspect_ratio = width / height
    camera_u, camera_v, camera_w = calculate_camera_variables(cam_eye, lookat, up, hfov, aspect_ratio)

    context['eye'] = np.array(cam_eye, dtype=np.float32)
    context['U'] = np.array(camera_u, dtype=np.float32)
    context['V'] = np.array(camera_v, dtype=np.float32)
    context['W'] = np.array(camera_w, dtype=np.float32)

    ray_gen_program = Program('pinhole_camera.cu', 'pinhole_camera')
    exception_program = Program('pinhole_camera.cu', 'exception')
    entry_point = EntryPoint(ray_gen_program, exception_program)

    context['bad_color'] = np.array([0, 1, 1], dtype=np.float32)

    context.set_miss_program(0, Program('constantbg.cu', 'miss'))
    context['bg_color'] = np.array([0.4, 0.33, 0.21], dtype=np.float32)

    return context, entry_point


def create_scene(context, num_buffers):
    # Sphere
    sphere = Geometry(Program('sphere_texcoord.cu', 'bounds'), Program('sphere_texcoord.cu', 'intersect'))
    sphere.set_primitive_count(1)
    sphere['sphere'] = np.array([0.0, 1.2, 0.0, 1.0], dtype=np.float32)
    sphere['matrix_row_0'] = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    sphere['matrix_row_1'] = np.array([0.0, 1.0, 0.0], dtype=np.float32)
    sphere['matrix_row_2'] = np.array([0.0, 0.0, 1.0], dtype=np.float32)

    # Floor
    parallelogram = Geometry(Program('parallelogram.cu', 'bounds'), Program('parallelogram.cu', 'intersect'))
    parallelogram.set_primitive_count(1)
    anchor = np.array([-20.0, 0.01, 20.0], dtype=np.float32)
    v1 = np.array([40.0, 0.0, 0.0], dtype=np.float32)
    v2 = np.array([0.0, 0.0, -40.0], dtype=np.float32)
    normal = np.cross(v1, v2)
    normal /= np.linalg.norm(normal)
    d = np.dot(normal, anchor)
    v1 *= 1 / np.dot(v1, v1)
    v2 *= 1 / np.dot(v2, v2)
    plane = np.append(normal, d)
    parallelogram['plane'] = plane
    parallelogram['v1'] = v1
    parallelogram['v2'] = v2
    parallelogram['anchor'] = anchor

    # Sphere material
    sphere_matl = Material(
        closest_hit={
            0: Program('optixBuffersOfBuffers.cu', 'closest_hit_radiance')
        },
        any_hit={
            1: Program('optixBuffersOfBuffers.cu', 'any_hit_shadow')
        }
    )

    buffers = [create_random_buffer(MAX_BUFFER_WIDTH, MAX_BUFFER_HEIGHT) for _ in range(num_buffers)]

    # mark buffers as bindless so that they won't be destroyed when `buffers` list is garbage-collected
    for buffer in buffers:
        buffer.bindless = True

    sphere_matl['Kd_layers'] = Buffer.from_array([buf.get_id() for buf in buffers], dtype=np.int32, buffer_type='i')

    # Floor material
    floor_matl = Material(
        closest_hit={
            0: Program('phong.cu', 'closest_hit_radiance')
        },
        any_hit={
            1: Program('phong.cu', 'any_hit_shadow')
        }
    )
    floor_matl['Kd'] = np.array([0.7, 0.7, 0.7], dtype=np.float32)
    floor_matl['Ka'] = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    floor_matl['Kr'] = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    floor_matl['phong_exp'] = np.array(1.0, dtype=np.float32)

    # Place geometry into hierarchy
    geometrygroup = GeometryGroup()
    geometrygroup.add_child(GeometryInstance(sphere, sphere_matl))
    geometrygroup.add_child(GeometryInstance(parallelogram, floor_matl))
    acc = Acceleration('Sbvh', 'Bvh')
    geometrygroup.set_acceleration(acc)

    context['top_object'] = geometrygroup
    context['top_shadower'] = geometrygroup

    # Lights
    context['ambient_light_color'] = np.array([0.1, 0.1, 0.1], dtype=np.float32)
    lights = [
        np.array(BasicLight([0.0, 8.0, -5.0], [0.4, 0.4, 0.4], True)),
        np.array(BasicLight([5.0, 8.0, 0.0], [0.4, 0.4, 0.4], True)),
    ]
    context["lights"] = Buffer.from_array(np.array(lights), buffer_type='i', drop_last_dim=True)


def main():
    num_buffers = 4
    context, entry_point = create_context()
    create_scene(context, num_buffers)
    entry_point.launch((width, height))

    result_array = context['output_buffer'].to_array()
    result_image = Image.fromarray(result_array)
    ImageWindow(result_image.rotate(180))


if __name__ == '__main__':
    main()
