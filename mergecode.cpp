#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <filesystem>

namespace fs = std::filesystem;
std::vector<std::string> pass_file = {"__init__.py", "geometry.py",
    "KernelAudio.py", "KernelColor.py", "ImageObj.py"};
void merge_code_files(const fs::path& source_dir,
                      const fs::path& output_file,
                      const std::vector<std::string>& extensions,
                      const std::vector<std::string>& skip_files) {
    std::ofstream outfile(output_file, std::ios::out | std::ios::trunc);
    if (!outfile) {
        std::cerr << "Cannot open output file\n";
        return;
    }

    for (const auto& entry : fs::recursive_directory_iterator(source_dir)) {
        if (!entry.is_regular_file()) continue;

        std::string filename = entry.path().filename().string();
        bool skip = false;
        for (const auto& skip_name : skip_files) {
            if (filename == skip_name) { skip = true; break; }
        }
        if (skip) continue;

        bool ext_ok = extensions.empty();
        for (const auto& ext : extensions) {
            if (filename.size() >= ext.size() &&
                filename.compare(filename.size() - ext.size(), ext.size(), ext) == 0) {
                ext_ok = true;
                break;
                }
        }
        if (!ext_ok) continue;

        outfile << "\n==================================================\n";
        outfile << " FILE: " << entry.path().string() << "\n";
        outfile << "==================================================\n\n";

        std::ifstream infile(entry.path());
        if (infile) {
            outfile << infile.rdbuf();
        }
        outfile << "\n";
    }
}

int main() {
    fs::path folder_path = "D:/Python/PygameTools/src/pgtkb";
    std::vector<std::string> my_extensions = {".py"};
    fs::path result_name = "mergefile.txt";

    merge_code_files(folder_path, result_name, my_extensions, pass_file);
    return 0;
}