# change id check를 하고 수정한 csv 파일로 bbox를 만들어보자 -> bounding box 그리기만 하는 코드임 지금은

# joo-> seo 인 부분만 체크해서 joo로 만들기

import cv2
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist


# CSV 파일에서 데이터 읽기
csv_file_path = './output2.csv'  # 바꿔야 하는 거
df = pd.read_csv(csv_file_path)

# NaN 값이 있는 행 제거
df.dropna(subset=['xmin', 'ymin', 'xmax', 'ymax'], inplace=True)

# 동영상 파일 경로
video_path = "C:/Users/MIS/yolov4-deepsort/joo_1.mp4" # 바꿔야 하는 거
output_video_path = './second_execute2_20240517.mp4' # 바꿔야 하는 거



# 동영상 불러오기
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Could not Open :", video_path)
    exit(0)

# 동영상 프레임 크기 및 FPS 설정
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Get the video frame width and height
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec and create VideoWriter objects
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# 각 객체에 대한 색상 매핑을 위한 딕셔너리 생성
color_mapping = {}
previous_frame_data = None

while True:
    # 프레임 읽기
    ret, frame = cap.read()
    
    # 동영상 끝에 도달하면 종료
    if not ret:
        break

    # 현재 프레임의 정보 얻기
    frame_number = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
    current_frame_data = df[df['frame_num'] == frame_number]


    # bounding box 그리기
    for index, row in current_frame_data.iterrows():
        
        xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        
        object_id = row['track_id']
        if object_id == 6:
            object_id = 1
        elif object_id == 10:
            object_id = 2 

        # 객체별로 고유한 색상 할당
        if object_id not in color_mapping:
            color_mapping[object_id] = tuple(np.random.randint(0, 255, 3).tolist())

        color = color_mapping[object_id]
        
        thickness = 5
        
        # print(xmin)
        # if xmin == None:
        #     xmin, ymin, xmax, ymax = 0, 0, 0 ,0

        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness)
        cv2.putText(frame, f'ID: {int(object_id)}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3,
                    cv2.LINE_AA)

    # 프레임 번호 표시
    font_size = 2
    font_thickness = 3
    font_color = (255, 255, 255)
    font_position = (10, int(frame_height - 5 / 30 * frame_height))

    cv2.putText(frame, f'Frame: {frame_number}', font_position, cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color,
                font_thickness, cv2.LINE_AA)
    
    

    # 동영상 파일에 프레임 쓰기
    out.write(frame)

    # 화면에 표시
    cv2.imshow('Video with Bounding Boxes', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# 종료
cap.release()
out.release()
cv2.destroyAllWindows()