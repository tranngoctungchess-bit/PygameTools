import os
def list_kernels():
    template_dir = "Kernel"
    kernels = []
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                kernels.append(rel_path.replace("\\", "/"))
    return kernels

if __name__ == "__main__":
    kernels = list_kernels()
    print(f"Current number of kernel files: {len(kernels)}")
    print("Kernels:")
    for t in sorted(kernels):
        print(f"  - {t}")
#For testing only