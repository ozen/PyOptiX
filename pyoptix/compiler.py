try:
    import configparser
except ImportError:
    import ConfigParser as configparser


class OptixCompiler(object):

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('pyoptix.conf')
        self.ptx_path = config.get('compiler', 'ptx_path')
        self.arch = config.get('compiler', 'arch')
        self.use_fast_math = config.get('compiler', 'use_fast_math')
        self.include_paths = config.get('compiler', 'use_fast_math').split(':')

    def compile(self, cu_file_path):

        compile_required = True
        output_path = self.ptx_path

        import os.path
        # Check if it is compiled before
        cu_file_name = os.path.basename(cu_file_path)

        output_file_path = os.path.join(output_path, cu_file_name + ".ptx")

        if os.path.isfile(output_file_path):
            cu_file_time = os.path.getmtime(cu_file_path)
            ptx_file_time = os.path.getmtime(output_file_path)
            if ptx_file_time > cu_file_time:
                compile_required = False

        if compile_required:
            print("Optix Compiler: compiling " + cu_file_path)
            bashCommand = "nvcc -c"
            bashCommand += " "
            bashCommand += cu_file_path
            bashCommand += " "
            bashCommand += "-ptx"
            bashCommand += " "
            bashCommand += "-arch=" + self.arch
            bashCommand += " "
            if self.use_fast_math:
                bashCommand += "--use_fast_math"
                bashCommand += " "
            for include_path in self.include_paths:
                if os.path.exists(include_path):
                    bashCommand += "--include-path="
                    bashCommand += include_path + " "

            bashCommand += "--output-file=" + output_file_path
            bashCommand += " "

            print(bashCommand)
            import subprocess
            splited = bashCommand.split()
            process = subprocess.Popen(splited, stdout=subprocess.PIPE)
            output = process.communicate()[0]
        else:
            print("Optix Compiler: no compiling required " + cu_file_path)

        return output_file_path