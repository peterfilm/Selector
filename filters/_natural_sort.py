import os
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

if __name__ == "__main__":
    directory_path = "/path/to/your/directory"
    all_files_list = os.listdir(directory_path)
    sorted_files = sorted(all_files_list, key=natural_sort_key)

    for file_name in sorted_files:
        file_path = os.path.join(directory_path, file_name)
        print(file_path)