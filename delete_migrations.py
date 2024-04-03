import os

def delete_files_in_migrations(directory):
    for root, dirs, files in os.walk(directory):
        if '.venv' in dirs:
            dirs.remove('.venv')
        if 'venv' in dirs:
            dirs.remove('venv')
        
        if 'migrations' in dirs:
            migrations_dir = os.path.join(root, 'migrations')
            for filename in os.listdir(migrations_dir):
                file_path = os.path.join(migrations_dir, filename)
                if os.path.isfile(file_path) and filename != '__init__.py' and filename != '0001_initial_data.py':
                    os.remove(file_path)
                    print(f"S'ha borrat {filename} del directori {migrations_dir}")

if __name__ == "__main__":
    current_directory = os.getcwd()
    delete_files_in_migrations(current_directory)