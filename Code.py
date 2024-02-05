import requests
import os
from PIL import Image
from io import BytesIO
import time
import csv
import pandas as pd
import imghdr  # Import the imghdr library

# Set the path to your CSV file
csv_file_path = 'Data/Data.csv'

# Create a folder for downloaded images if it doesn't exist
os.makedirs('Data/Images', exist_ok=True)

# Define a function to download and save images in WebP format
def download_and_save_as_webp(image_url, image_id, index):
    max_retries = 3  # Maximum number of download retries
    retry_delay = 15  # Seconds to wait before each retry
    
    for retry_count in range(max_retries):
        try:
            if image_url and not pd.isna(image_url):  # Skip empty URLs
                response = requests.get(image_url, timeout=15)  # Set a timeout of 15 seconds
                if response.status_code == 200:
                    image_data = response.content
                    image_type = imghdr.what(None, h=image_data)  # Determine the image type
                    if image_type:
                        image = Image.open(BytesIO(image_data))
                        image_id = int(image_id)  # Convert 'File ID' to an integer
                        
                        # Save the image in WebP format
                        image.save(f'Data/Images/{image_id}.webp', 'WEBP')
                        
                        print(f"Image {image_id}.webp downloaded and saved. Time: {time.strftime('%H:%M:%S', time.gmtime())}")
                        break  # Break the loop on successful download
                    else:
                        print(f"Downloaded content for image {image_id} is not a valid image.")
                else:
                    print(f"Failed to download image {image_id}. Status code: {response.status_code}")
            else:
                print(f"Skipped empty column in URL at row {index + 1}")
                break  # Break the loop for empty URLs
        except requests.exceptions.RequestException as re:
            print(f"Error downloading image {image_id}: {str(re)}")
            if retry_count < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                log_error(image_id, f"Error downloading image {image_id} after {max_retries} retries.")
                break  # Break the loop on too many retries
        except Exception as e:
            print(f"Other error downloading image {image_id}: {str(e)}")
            log_error(image_id, f"Other error downloading image {image_id}: {str(e)}")
            break  # Break the loop on other errors

# Function to log errors to a CSV file
def log_error(error_id, error_info):
    error_log_file = 'Data/Error_Log.csv'
    with open(error_log_file, mode='a', newline='') as error_file:
        error_writer = csv.writer(error_file)
        if not os.path.isfile(error_log_file):
            error_writer.writerow(['Error ID', 'Error Info'])
        error_writer.writerow([error_id, error_info])

try:
    # Read the CSV file using pandas
    df = pd.read_csv(csv_file_path)

    # Define the starting row as an integer
    start_row = 1

    # Record the start time
    start_time = time.time()

    # Loop through the rows in the CSV file
    for index, row in df.iterrows():
        if index < start_row:
            continue
        
        image_url = row['Image URL']
        image_id_str = row['File ID']  # Retrieve 'File ID' as a string
        
        try:
            image_id = int(image_id_str)  # Attempt to convert 'File ID' to an integer
        except ValueError as ve:
            print(f"Error converting image ID to integer: {ve}")
            continue  # Skip this row if conversion fails
        
        download_and_save_as_webp(image_url, image_id, index)
        print(f"Completed row {index + 1}. Time: {time.strftime('%H:%M:%S', time.gmtime())}")
        
    # Record the end time
    end_time = time.time()

    # Calculate the total time elapsed
    total_time = end_time - start_time

    # Log the process completion and total time elapsed
    print(f"Image download and saving process completed. Total Time: {total_time:.2f} seconds")

except Exception as ex:
    print(f"An error occurred: {str(ex)}")
