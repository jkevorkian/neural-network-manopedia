num_handsigns = 4
videos_per_handsign = 50
frames_per_video = 30
num_landmarks = 51
num_coordinates = 3

##          PROCESS VIDEO DATASET FUNC DEFINITIONS         ##
import cv2
import mediapipe as mp
import numpy as np
import os
from tqdm import tqdm


def extract_landmarks(image, hands_results, pose_results):
    landmarks = []

    # Extract left hand landmarks (21 landmarks)
    if hands_results.multi_hand_landmarks and len(hands_results.multi_hand_landmarks) > 0:
        landmarks.extend([(lm.x, lm.y, lm.z) for lm in hands_results.multi_hand_landmarks[0].landmark])
    else:
        landmarks.extend([(0, 0, 0)] * 21)

    # Extract right hand landmarks (21 landmarks)
    if hands_results.multi_hand_landmarks and len(hands_results.multi_hand_landmarks) > 1:
        landmarks.extend([(lm.x, lm.y, lm.z) for lm in hands_results.multi_hand_landmarks[1].landmark])
    else:
        landmarks.extend([(0, 0, 0)] * 21)

    # Extract selected body landmarks (9 landmarks)
    selected_body_landmarks = [0, 11, 12, 13, 14, 15, 16, 23, 24]  # Landmarks for nose, arms, and shoulders
    if pose_results.pose_landmarks:
        for idx in selected_body_landmarks:
            lm = pose_results.pose_landmarks.landmark[idx]
            landmarks.append((lm.x, lm.y, lm.z))
    else:
        landmarks.extend([(0, 0, 0)] * 9)

    return np.array(landmarks)


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []

    mp_hands = mp.solutions.hands
    mp_pose = mp.solutions.pose

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    indices = np.linspace(0, total_frames - 1, frames_per_video, dtype=int)
    frame_set = set(indices)
    frame_count = 0

    with mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5) as hands, \
            mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while cap.isOpened() and len(frames) < frames_per_video:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count in frame_set:
                # Convert the BGR image to RGB
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process the image and extract landmarks
                hands_results = hands.process(image)
                pose_results = pose.process(image)

                # Extract landmarks
                landmarks = extract_landmarks(image, hands_results, pose_results)

                frames.append(landmarks)

            frame_count += 1

    cap.release()

    # Pad if we don't have enough frames
    if len(frames) < frames_per_video:
        frames.extend([np.zeros((51, 3))] * (frames_per_video - len(frames)))

    return np.array(frames)


def process_dataset(root_path):
    data = []

    for handsign in tqdm(range(num_handsigns), desc="Processing handsigns"):
        handsign_path = os.path.join(root_path, f"handsign_{handsign + 1}")  # Changed to match your folder naming
        if not os.path.exists(handsign_path):
            print(f"Warning: Directory {handsign_path} does not exist. Skipping.")
            data.append(np.zeros((videos_per_handsign, frames_per_video, 51, 3)))  # 51 landmarks total
            continue

        videos = [f for f in os.listdir(handsign_path) if f.endswith(('.mp4', '.avi', '.mov'))]
        videos = videos[:videos_per_handsign]  # Limit to videos_per_handsign

        handsign_data = []
        for video in tqdm(videos, desc=f"Processing videos for handsign {handsign}", leave=False):
            video_path = os.path.join(handsign_path, video)
            video_data = process_video(video_path)
            handsign_data.append(video_data)

        # Pad if we don't have enough videos
        if len(handsign_data) < videos_per_handsign:
            handsign_data.extend([np.zeros((frames_per_video, 51, 3))] * (videos_per_handsign - len(handsign_data)))

        data.append(np.array(handsign_data))

    return np.array(data)



###     VISUALIZATION      ###


def draw_landmarks(frame, landmarks):
    """
    Draws landmarks on the frame.
    :param frame: The image frame on which to draw landmarks.
    :param landmarks: The landmarks to draw.
    """
    for i, (x, y, z) in enumerate(landmarks):
        # Convert normalized coordinates to pixel coordinates
        height, width, _ = frame.shape
        x_px = int(x * width)
        y_px = int(y * height)
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
    height, width = 720, 1280  # Assuming a 720p resolution for the output video
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
data_array = np.load('../../hand_landmarks.npy')

# Specify the video and handsign indices
video_idx = 4 # Change this to visualize different videos
handsign_idx = 0  # Change this to visualize different handsigns
output_path = './video.mp4'

# Visualize landmarks and save the video
visualize_landmarks_video(data_array, video_idx, handsign_idx, output_path)

print(f"Landmarks visualization video saved to {output_path}")
