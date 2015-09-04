import re
import os
import shlex
import fnmatch
from subprocess import check_call, CalledProcessError


defaults = {
    'output_path': '/tmp/pyoptix/ptx',
    'include_paths': ['/usr/local/optix/include'],
    'arch': 'sm_21',
    'use_fast_math': True,
}


def _compile_required(cu_file_path, output_file_path):
        include_pattern = '#include\s*"(.*)"'
        dirname = os.path.dirname(cu_file_path)

        if os.path.isfile(output_file_path):
            ptx_file_time = os.path.getmtime(output_file_path)

            cu_file_time = os.path.getmtime(cu_file_path)
            if cu_file_time > ptx_file_time:
                return True

            else:
                with open(cu_file_path) as cu_file:
                    content = cu_file.read()
                    for included in re.findall(include_pattern, content):
                        included_file_time = os.path.getmtime(os.path.join(dirname, included))
                        if included_file_time > ptx_file_time:
                            return True

                return False

        else:
            return True


class OptixCompiler(object):

    def __init__(self, output_path=defaults['output_path'], include_paths=defaults['include_paths'],
                 arch=defaults['arch'], use_fast_math=defaults['use_fast_math']):
        self.output_path = output_path
        self.include_paths = include_paths
        self.arch = arch
        self.use_fast_math = use_fast_math

        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def compile(self, cu_file_path):
        cu_file_name = os.path.basename(cu_file_path)
        output_file_path = os.path.join(self.output_path, cu_file_name + ".ptx")

        if _compile_required(cu_file_path, output_file_path):
            print("Optix Compiler: compiling " + cu_file_path)
            bash_command = "nvcc " + cu_file_path
            bash_command += " -ptx"
            bash_command += " -arch=" + self.arch
            if self.use_fast_math:
                bash_command += " --use_fast_math"
            for include_path in self.include_paths:
                if os.path.exists(include_path):
                    bash_command += " -I=" + include_path
            bash_command += " -o=" + output_file_path
            print(bash_command)
            try:
                check_call(shlex.split(bash_command))
            except CalledProcessError as e:
                print(e)
        else:
            print("Optix Compiler: no compiling required " + cu_file_path)

        return output_file_path

    def clean(self):
        if os.path.exists(self.output_path):
            for dirpath, dirnames, filenames in os.walk(self.output_path):
                for filename in fnmatch.filter(filenames, '*.ptx'):
                    os.remove(os.path.join(dirpath, filename))
