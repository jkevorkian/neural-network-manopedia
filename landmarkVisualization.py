import cv2, json, os
import numpy as np

###     VISUALIZATION      ###

# Define the parameters for the data shape
videos_per_handsign = 136  # Adjust if necessary
frames_per_video = 10
num_landmarks = 51
num_coordinates = 3

data_augmentation = True
num_augmented_versions = 3  # How many videos will be created from augmenting each video from the dataset

# Define the root directory containing handsign folders
root_path = "ACOTADONomenclatedDataset"

def get_handsign_folders(root_path):
    handsign_names = {}
    handsign_count = 0

    # Walk through the root directory
    for folder in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder)

        # Ignore non-directories
        if not os.path.isdir(folder_path):
            continue

        # If the folder starts with "#", check its subdirectories
        if folder.startswith("#"):
            for subfolder in os.listdir(folder_path):
                subfolder_path = os.path.join(folder_path, subfolder)
                if os.path.isdir(subfolder_path):
                    handsign_names[handsign_count] = subfolder
                    handsign_count += 1
        else:
            # Directly add the folder as a handsign
            handsign_names[handsign_count] = folder
            handsign_count += 1

    return handsign_names

# Get the handsign names automatically
handsign_names = get_handsign_folders(root_path)
num_handsigns = len(handsign_names)

# Output the handsign names and number of handsigns
print(f"Number of handsigns: {num_handsigns}")
print("Handsign names:")
print(json.dumps(handsign_names, indent=4))

def get_finger_name(i):
    """
    Given a landmark index, returns the hand and finger name.
    """
    hand = 'left' if i < 21 else 'right'
    idx = i % 21  # get the index within the hand (0-20)
    if idx == 0:
        return hand, 'wrist'
    elif idx in [1, 2, 3, 4]:
        return hand, 'thumb'
    elif idx in [5, 6, 7, 8]:
        return hand, 'index'
    elif idx in [9, 10, 11, 12]:
        return hand, 'middle'
    elif idx in [13, 14, 15, 16]:
        return hand, 'ring'
    elif idx in [17, 18, 19, 20]:
        return hand, 'pinky'
    else:
        return hand, 'unknown'

# Mediapipe hand connections (landmarks that should be connected to each other)
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),    # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),    # Index finger
    (0, 9), (9, 10), (10, 11), (11, 12), # Middle finger
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (0, 17), (17, 18), (18, 19), (19, 20)  # Pinky finger
]

def draw_landmarks(frame, landmarks):
    """
    Draws landmarks and connections on the frame.
    :param frame: The image frame on which to draw landmarks and connections.
    :param landmarks: The landmarks to draw.
    """
    # Define colors for fingers
    finger_colors = {
        'wrist': (0, 0, 0),          # Black
        'thumb': (255, 0, 0),        # Red
        'index': (0, 255, 0),        # Green
        'middle': (0, 0, 255),       # Blue
        'ring': (255, 255, 0),       # Yellow
        'pinky': (255, 0, 255)       # Magenta
    }

    # Draw landmarks
    for i, (x, y, z) in enumerate(landmarks):
        # Convert normalized coordinates to pixel coordinates
        height, width, _ = frame.shape
        x_px = int(x * width + 1500)
        y_px = int(y * height + 700)

        hand, finger = get_finger_name(i)
        color = finger_colors.get(finger, (255, 255, 255))  # default to white if unknown

        # Draw the landmark as a small circle
        cv2.circle(frame, (x_px, y_px), 10, color, -1)

    # Draw connections between the landmarks
    for connection in HAND_CONNECTIONS:
        start_idx, end_idx = connection
        if start_idx < len(landmarks) and end_idx < len(landmarks):
            x1, y1, _ = landmarks[start_idx]
            x2, y2, _ = landmarks[end_idx]

            # Convert normalized coordinates to pixel coordinates
            x1_px = int(x1 * width + 1500)
            y1_px = int(y1 * height + 700)
            x2_px = int(x2 * width + 1500)
            y2_px = int(y2 * height + 700)

            # Draw a line between the two points
            cv2.line(frame, (x1_px, y1_px), (x2_px, y2_px), (255, 255, 255), 2)  # White line for connections

def visualize_landmarks_video(data_array, video_idx, handsign_idx, output_path):
    """
    Visualizes the landmarks for each frame of a specified video and saves the result as a new video.
    :param data_array: The array containing the landmarks data.
    :param video_idx: The index of the video to visualize.
    :param handsign_idx: The index of the handsign to visualize.
    :param output_path: The path to save the output video.
    """
    # Get the landmarks for the specified video
    video_data = data_array[handsign_idx, video_idx]

    # Initialize video writer
    height, width = 1280 * 2, 1280 * 2  # Adjust as necessary
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 10, (width, height))

    for frame_landmarks in video_data:
        # Create a blank frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Draw landmarks and connections on the frame
        draw_landmarks(frame, frame_landmarks)

        # Write the frame to the video
        out.write(frame)

    out.release()

# Load the saved landmarks data
data_array = np.load('handsigns_data_augmented.npy')

# Specify the video and handsign indices
video_idx = 4  # Change this to visualize different videos
handsign_idx = 0  # Change this to visualize different handsigns (begins at 0)
output_path = './video.mp4'

# Visualize landmarks and save the video
visualize_landmarks_video(data_array, video_idx, handsign_idx, output_path)

print(f"Landmarks visualization video saved to {output_path}")

