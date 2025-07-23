import os

# Folder base
base_dir = "src/app"

# Target folders and unke files
folder_files = {
    "api": ["routes.py"],
    "core": ["config.py", "security.py"],
    "db": ["database.py", "init_db.py"],
    "models": ["news.py", "user.py"],
    "schemas": ["news.py", "user.py"],
    "services": ["news_service.py", "user_service.py"],
    "templates": ["base.html"],
    "static": ["readme.txt"]  # Just to create placeholder
}

for folder, files in folder_files.items():
    path = os.path.join(base_dir, folder)
    for file in files:
        file_path = os.path.join(path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# {file} for {folder} module\n")

# tests folder
tests_path = "src/tests"
test_files = ["test_main.py"]
for file in test_files:
    file_path = os.path.join(tests_path, file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"# Unit tests - {file}\n")

print("📄 Python files created in all folders.")
