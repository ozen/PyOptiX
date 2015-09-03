import re
import os
import subprocess

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


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

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyoptix.conf'))
        self.ptx_path = config.get('compiler', 'ptx_path')
        self.arch = config.get('compiler', 'arch')
        self.use_fast_math = config.getboolean('compiler', 'use_fast_math')
        self.include_paths = config.get('compiler', 'include_paths').split(':')

        if not os.path.exists(self.ptx_path):
            os.makedirs(self.ptx_path)

    def compile(self, cu_file_path):
        output_path = self.ptx_path
        cu_file_name = os.path.basename(cu_file_path)
        output_file_path = os.path.join(output_path, cu_file_name + ".ptx")

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
            splitted = bash_command.split()
            process = subprocess.Popen(splitted, stdout=subprocess.PIPE)
            output = process.communicate()[0]
        else:
            print("Optix Compiler: no compiling required " + cu_file_path)

        return output_file_path
