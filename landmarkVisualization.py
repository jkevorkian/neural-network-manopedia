import cv2
import numpy as np


###     VISUALIZATION      ###

num_handsigns = 2
videos_per_handsign = 82
frames_per_video = 30
num_landmarks = 51
num_coordinates = 3

def draw_landmarks(frame, landmarks):
    """
    Draws landmarks on the frame.
    :param frame: The image frame on which to draw landmarks.
    :param landmarks: The landmarks to draw.
    """
    for i, (x, y, z) in enumerate(landmarks):
        # Convert normalized coordinates to pixel coordinates
        height, width, _ = frame.shape
        x_px = int(x * width+1500)
        y_px = int(y * height+700)
        # Draw the landmark as a small circle
        cv2.circle(frame, (x_px, y_px), 5, (0, 255, 0), -1)


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
    height, width = 720*2, 1280*2  # Assuming a 720p resolution for the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 10, (width, height))

    for frame_landmarks in video_data:
        # Create a blank frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Draw landmarks on the frame
        draw_landmarks(frame, frame_landmarks)

        # Write the frame to the video
        out.write(frame)

    out.release()


# Load the saved landmarks data
data_array = np.load('handsigns_data.npy')

# Specify the video and handsign indices
video_idx =120 # Change this to visualize different videos
handsign_idx = 2  # Change this to visualize different handsigns (begins at 0)
output_path = './video.mp4'

# Visualize landmarks and save the video
visualize_landmarks_video(data_array, video_idx, handsign_idx, output_path)

print(f"Landmarks visualization video saved to {output_path}")
