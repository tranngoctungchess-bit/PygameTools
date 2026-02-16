import os


def merge_code_files(source_dir, output_file, extensions=None):
    """
    Gom tất cả các file code trong thư mục vào một file duy nhất.

    :param source_dir: Đường dẫn thư mục chứa code.
    :param output_file: Tên file kết quả.
    :param extensions: Danh sách đuôi file muốn lấy (vd: ['.py', '.js']). Nếu None sẽ lấy tất cả.
    """

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                # Kiểm tra định dạng file
                if extensions is None or any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)

                    # Viết tiêu đề phân cách giữa các file
                    outfile.write(f"\n{'=' * 50}\n")
                    outfile.write(f" FILE: {file_path}\n")
                    outfile.write(f"{'=' * 50}\n\n")

                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            outfile.write(infile.read())
                        print(f"Đã thêm: {file_path}")
                    except Exception as e:
                        print(f"Lỗi khi đọc file {file_path}: {e}")

                    outfile.write("\n")


# --- CẤU HÌNH TẠI ĐÂY ---
folder_path = 'D:/Python/PygameTools/Kernel'  # Thay bằng đường dẫn thư mục của bạn
my_extensions = ['.py']  # Chỉ lấy các file này

merge_code_files(folder_path, result_name, my_extensions)