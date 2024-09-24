import os
import shutil

def organize_videos(input_folder):
    # Create a list of all files in the input folder
    files = os.listdir(input_folder)

    # Loop through all files in the input folder
    for file_name in files:
        # Ensure it's a video file (mp4 in this case)
        if file_name.endswith(".mp4"):
            # Extract the first three digits and subtract 1
            try:
                first_three_numbers = int(file_name[:3])
                folder_index = first_three_numbers - 1
                folder_name = f"handsign_{folder_index}"
                
                # Create the destination folder if it doesn't exist
                destination_folder = os.path.join(input_folder, folder_name)
                os.makedirs(destination_folder, exist_ok=True)
                
                # Move the file to the destination folder
                src_path = os.path.join(input_folder, file_name)
                dest_path = os.path.join(destination_folder, file_name)
                shutil.move(src_path, dest_path)
                print(f'Moved {file_name} to {folder_name}')
            
            except ValueError:
                print(f"Skipping {file_name}, not starting with a number.")

# Define your input folder path
input_folder = "all_cut"

# Call the function
organize_videos(input_folder)
