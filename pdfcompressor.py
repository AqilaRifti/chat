import os
from typing import List
import pathlib

def get_all_file_paths(directory) -> List[os.PathLike | str]:
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings to form the full file path.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

# Example usage:
pdf_exe = "~/executables/pdfsizeopt/pdfsizeopt"
target_directory = "./resources/Buku Paket SD"
all_files = get_all_file_paths(target_directory)
# Print all file paths
slash = "/"
for file in all_files:
    if file.endswith(".pdf"):
        if not pathlib.Path(f"new/{file.split('/', maxsplit=3)[-1]}").is_file():
            os.system(f"{pdf_exe} \"{file}\" \"new/{file.split('/', maxsplit=3)[-1]}\"")