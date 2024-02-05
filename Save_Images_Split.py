import os
import shutil

# Source folder with 21,000 images
source_folder = 'Data/Images'  # Replace with the path to your source folder

# Create destination folder
destination_folder = 'Data/Liquor_Depo_images'

# Create subfolders Images 1, Images 2, Images 3
subfolder_names = ['Images 1', 'Images 2', 'Images 3']
subfolders = [os.path.join(destination_folder, name) for name in subfolder_names]

for subfolder in subfolders:
    os.makedirs(subfolder, exist_ok=True)

# List all files in the source folder
file_list = os.listdir(source_folder)

# Split files into 3 subfolders
for i, file_name in enumerate(file_list):
    source_path = os.path.join(source_folder, file_name)
    if os.path.isfile(source_path):
        subfolder_index = i % 3  # Distribute files evenly among the 3 subfolders
        destination_path = os.path.join(subfolders[subfolder_index], file_name)
        shutil.move(source_path, destination_path)

print("Splitting of files into 3 subfolders completed.")