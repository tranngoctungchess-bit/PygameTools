import os
pass_file = ['KernelColor.py', '__init__.py', 'geometry.py', 'KernelAudio.py', 'KernelColor.py', 'ImageObj.py',
             'KernelLayout.py', 'KernelPosition.py', 'VFlags.py', 'Uflags.py', 'RFlags.py', 'KernelInit.py',
             'LinkRenderfunc.py', 'RRender.py', 'Render.py', 'TextObj.py']

pf1 = ['__init__.py']
def merge_code_files(source_dir, output_file, extensions=None, skip_files=None):

    if skip_files is None:
        skip_files = []

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file in skip_files:
                    continue

                if extensions is None or any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)

                    outfile.write(f"\n{'=' * 50}\n")
                    outfile.write(f" FILE: {file_path}\n")
                    outfile.write(f"{'=' * 50}\n\n")
                    with open(file_path, encoding='utf-8') as infile:
                        outfile.write(infile.read())

                    outfile.write("\n")

folder_path = 'src/pgtkb'
my_extensions = ['.py']
result_name = 'haha.txt'
merge_code_files(folder_path, result_name, my_extensions, pf1)