from collections import defaultdict

import pandas as pd
import csv
import cv2
import numpy as np

from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

# Open the video files
video_path1 = "C:/Users/MIS/yolov4-deepsort/bae_1.mp4"
cap1 = cv2.VideoCapture(video_path1)

video_path2 = "C:/Users/MIS/yolov4-deepsort/joo_1.mp4"
cap2 = cv2.VideoCapture(video_path2)

# Store the track history
track_history1 = defaultdict(lambda: [])
track_history2 = defaultdict(lambda: [])

# Get the video frame width and height
frame_width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))

frame_width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter objects
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_video_path1 = "output_video_bae.avi"
out1 = cv2.VideoWriter(output_video_path1, fourcc, 30.0, (frame_width1, frame_height1))

output_video_path2 = "output_video_joo.avi"
out2 = cv2.VideoWriter(output_video_path2, fourcc, 30.0, (frame_width2, frame_height2))


# CSV 파일 경로 설정
csv_file_path1 = "track_data_bae.csv"
csv_file_path2 = "track_data_joo.csv"

# CSV 파일 열 헤더 설정
csv_headers = ["frame_num", "track_id", "xmin", "ymin", "xmax", "ymax"]

# CSV 파일 열 헤더 쓰기
with open(csv_file_path1, mode='w', newline='') as file1:
    writer1 = csv.writer(file1)
    writer1.writerow(csv_headers)

with open(csv_file_path2, mode='w', newline='') as file2:
    writer2 = csv.writer(file2)
    writer2.writerow(csv_headers)
    
first_video_id = []
second_video_id = []

# Loop through the video frames
frame_num = 0
while cap1.isOpened():
    # print(frame_num)
    frame_num += 1
    # Read frames from the videos
    success1, frame1 = cap1.read()
    
    # print(frame1.shape)

    if success1:
        # Run YOLOv8 tracking on the frames, persisting tracks between frames
        results1 = model.track(frame1, persist=True, classes=0)

        # Check if objects are detected in the frames
        # Get the boxes and track IDs
        boxes1 = results1[0].boxes.xywh.cpu()
        xyxybox1 = results1[0].boxes.xyxy.cpu()
            
        track_ids1 = results1[0].boxes.id.int().cpu().tolist()
        
        
        if len(first_video_id) != 2 and len(track_ids1) == 2:
            first_video_id = track_ids1
        
        
        if len(boxes1) > 2: # id를 지워주자 2개가 남으면 멈춰도 돼
            for index, _id in enumerate(track_ids1):
                if _id not in first_video_id: # 해당 _id가 없으면 해당 인덱스를 지워
                    boxes1.pop(index)
                    track_ids1.pop(index)
                    if len(boxes1) == 2:
                        break

        # Visualize the results on the frame
        annotated_frame1 = results1[0].plot()
        

        # Plot the tracks
        for box, track_id, xyxybox in zip(boxes1, track_ids1, xyxybox1):
            x, y, w, h = box
            xmin, ymin, xmax, ymax = xyxybox
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)  # Convert tensor format to integers
            track = track_history1[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 30:  # retain 90 tracks for 90 frames
                track.pop(0)
                
            # CSV 파일에 데이터 기록
            with open(csv_file_path1, mode='a', newline='') as file1:
                writer1 = csv.writer(file1)
                writer1.writerow([frame_num, track_id, xmin, ymin, xmax, ymax])


        # Write frames to the output videos
        out1.write(annotated_frame1)

        # Display the annotated frames
        cv2.imshow("YOLOv8 Tracking 1", annotated_frame1)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of any video is reached
        break
    
cap1.release()
out1.release()


     
frame_num = 0
while cap2.isOpened():
    frame_num += 1
    
    success2, frame2 = cap2.read()
    if success2:
        # Run YOLOv8 tracking on the frames, persisting tracks between frames
        results2 = model.track(frame2, persist=True, classes=0)

        # Check if objects are detected in the frames

        # Get the boxes and track IDs
        boxes2 = results2[0].boxes.xywh.cpu()
        xyxybox2 = results2[0].boxes.xyxy.cpu()
        track_ids2 = results2[0].boxes.id.int().cpu().tolist()
        
        if len(second_video_id) != 2 and len(track_ids2) == 2:
            second_video_id = track_ids2
            
        # boxes2 = np.array(boxes2)   
        # if len(boxes2) > 2: # id를 지워주자 2개가 남으면 멈춰도 돼
        #     for index, _id in enumerate(track_ids2):
        #         if _id not in first_video_id: # 해당 _id가 없으면 해당 인덱스를 지워
        #             boxes2.pop(index)
        #             track_ids2.pop(index)
        #             if len(boxes2) == 2:
        #                 break
        

        # Visualize the results on the frame
        annotated_frame2 = results2[0].plot()

        # Plot the tracks
        for box, track_id, xyxybox in zip(boxes2, track_ids2, xyxybox2):
            x, y, w, h = box
            xmin, ymin, xmax, ymax = xyxybox
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)  # Convert tensor format to integers
            track = track_history2[track_id]
            track.append((float(x), float(y)))  # x, y center point
            if len(track) > 30:  # retain 90 tracks for 90 frames
                track.pop(0)
                
            # CSV 파일에 데이터 기록
            with open(csv_file_path2, mode='a', newline='') as file2:
                writer2 = csv.writer(file2)
                writer2.writerow([frame_num, track_id, xmin, ymin, xmax, ymax])

        # Write frames to the output videos
        out2.write(annotated_frame2)

        # Display the annotated frames
        cv2.imshow("YOLOv8 Tracking 2", annotated_frame2)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of any video is reached
        break


# Release video capture objects, video writers, and close display windows
cap2.release()
out2.release()
cv2.destroyAllWindows()

# print("first_video_id: ", first_video_id)
# print("second_video_id: ", second_video_id)


# print("Output video saved successfully at:", output_video_path1)
# print("Output video saved successfully at:", output_video_path2)

# 처음 id도 나와있고, csv 저장 되어 있고 -> ./track_data_bae.csv AND ./track_data_joo.csv
# 각 인덱스에 맞는 사람이 같은 사람

# 1번 csv에서 first_video_id[0]이 없어졌어 -> 2번 csv에서 second_video_id[0]을 찾아. -> 2번 csv에서 second_video_id[0] 있으면 


data1 = pd.read_csv("./track_data_bae.csv")
data2 = pd.read_csv("././track_data_joo.csv")



