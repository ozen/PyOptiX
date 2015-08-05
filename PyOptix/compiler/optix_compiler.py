__author__ = 'vizera-ubuntu'

from PyOptix import config

class OptixCompiler(object):

    def __init__(self):
        pass

    def compile(self, cu_file_path):

        compile_required = True
        output_path = config.compiler["output_temp_path"]

        import os.path, time
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
            bashCommand += "-arch=" + config.compiler["arch"]
            bashCommand += " "
            if config.compiler["use_fast_math"]:
                bashCommand += "--use_fast_math"
                bashCommand += " "
            include_paths = config.compiler["include_paths"]
            for include_path in include_paths:
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