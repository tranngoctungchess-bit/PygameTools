import os
def list_templates():
    template_dir = "Template"
    templates = []
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                # Lấy đường dẫn tương đối so với Template/
                rel_path = os.path.relpath(os.path.join(root, file), template_dir)
                templates.append(rel_path.replace("\\", "/"))
    return templates

if __name__ == "__main__":
    templates = list_templates()
    print(f"Current number of templates: {len(templates)}")
    print("Templates:")
    for t in sorted(templates):
        print(f"  - {t}")