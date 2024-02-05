import zipfile
import os

# Define the path to the folder you want to compress
folder_to_compress = 'Data/Images/Images 1'

# Extract the folder name from the path
folder_name = os.path.basename(folder_to_compress)

# Define the path and name of the zip file with the same name as the folder
output_zip_file = os.path.join(os.path.dirname(folder_to_compress), f'{folder_name}.zip')

# Create a zip file and add the contents of the folder to it
with zipfile.ZipFile(output_zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(folder_to_compress):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, folder_to_compress)
            zipf.write(file_path, arcname)

print(f'Folder "{folder_to_compress}" has been compressed to "{output_zip_file}"')
