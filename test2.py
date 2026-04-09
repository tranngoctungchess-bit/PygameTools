import os

pass_file = ['KernelColor.py', '__init__.py', 'geometry.py', 'KernelAudio.py', 'KernelColor.py', 'ImageObj.py'
             'KernelLayout.py', 'KernelPosition.py', 'VFlags.py', 'Uflags.py', 'RFlags.py']


def merge_code_files(source_dir, output_file, extensions=None, skip_files=None):
    """
    Gom tất cả các file code trong thư mục vào một file duy nhất.

    :param source_dir: Đường dẫn thư mục chứa code.
    :param output_file: Tên file kết quả.
    :param extensions: Danh sách đuôi file muốn lấy (vd: ['.py']). Nếu None sẽ lấy tất cả.
    :param skip_files: Danh sách tên file muốn bỏ qua.
    """

    if skip_files is None:
        skip_files = []

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                # Kiểm tra nếu file nằm trong danh sách bỏ qua
                if file in skip_files:
                    continue

                # Kiểm tra định dạng file
                if extensions is None or any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)

                    # Viết tiêu đề phân cách giữa các file
                    outfile.write(f"\n{'=' * 50}\n")
                    outfile.write(f" FILE: {file_path}\n")
                    outfile.write(f"{'=' * 50}\n\n")
                    with open(file_path, encoding='utf-8') as infile:
                        outfile.write(infile.read())

                    outfile.write("\n")

# --- CẤU HÌNH TẠI ĐÂY ---
folder_path = 'src/pgtkb'  # Thay bằng đường dẫn thư mục của bạn
my_extensions = ['.py']  # Chỉ lấy các file này
result_name = 'haha.txt'
merge_code_files(folder_path, result_name, my_extensions)