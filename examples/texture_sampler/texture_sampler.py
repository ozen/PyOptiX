import sys
from os.path import dirname
sys.path.append(dirname(dirname(dirname(__file__))))

import numpy as np
from PIL import Image
from pyoptix import Context, Compiler, Buffer, Program, EntryPoint, TextureSampler
from examples.common import ImageWindow


def main():
    tex_width = 64
    tex_height = 64

    trace_width = 512
    trace_height = 384

    context = Context()
    Compiler.arch = 'sm_52'

    tex_data = []
    for j in range(tex_height):
        tex_data.append([])
        for i in range(tex_width):
            tex_data[j].append([
                (i + j) / (tex_width + tex_height) * 255,
                i / tex_width * 255,
                j / tex_height * 255,
                255
            ])

    tex_buffer = Buffer.from_array(np.array(tex_data, dtype=np.uint8), buffer_type='i', drop_last_dim=True)
    tex_sampler = TextureSampler(tex_buffer, wrap_mode='clamp_to_edge', indexing_mode='normalized_coordinates',
                                 read_mode='normalized_float', filter_mode='linear')

    context['input_texture'] = tex_sampler

    context['result_buffer'] = Buffer.empty((trace_height, trace_width, 4), dtype=np.float32,
                                            buffer_type='o', drop_last_dim=True)

    entry_point = EntryPoint(Program('draw_texture.cu', 'draw_texture'),
                             Program('draw_texture.cu', 'exception'))

    entry_point.launch((trace_width, trace_height))

    result_array = context['result_buffer'].to_array()
    result_array *= 255
    result_array = result_array.astype(np.uint8)
    result_image = Image.fromarray(result_array)
    ImageWindow(result_image)


if __name__ == '__main__':
    main()
