import os

folder_path = 'Data/Liquor_Depo_images/Images 3'  # Replace with the path to your folder

def remove_png_extension(file_path):
    base_name, extension = os.path.splitext(file_path)
    if extension.lower() == '.png':
        new_file_path = base_name
        os.rename(file_path, new_file_path)
        return new_file_path
    return file_path

# List all files in the folder
file_list = os.listdir(folder_path)

for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        new_file_path = remove_png_extension(file_path)
        print(f"Removed .png extension from file: {file_name} - Renamed to {new_file_path}")
