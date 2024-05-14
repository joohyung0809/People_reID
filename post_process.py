import pandas as pd
import csv
data1 = pd.read_csv("./track_data_bae.csv")
data2 = pd.read_csv("./track_data_joo.csv")


csv_file1 = open('output1.csv', 'w', newline='')
csv_file2 = open('output2.csv', 'w', newline='')
csv_writer1 = csv.writer(csv_file1)
csv_writer2 = csv.writer(csv_file2)

csv_writer1 = csv.DictWriter(csv_file1, fieldnames=['frame_num', 'track_id', 'xmin', 'ymin', 'xmax', 'ymax'])
csv_writer2 = csv.DictWriter(csv_file2, fieldnames=['frame_num', 'track_id', 'xmin', 'ymin', 'xmax', 'ymax'])

csv_writer1.writeheader()
csv_writer2.writeheader()



# 데이터를 저장할 리스트
frame_data_list1 = []
frame_data_list2 = []

# 이전 프레임 넘버 저장
prev_frame_num = None


# overlap check function
def check_overlap(record):
    box1 = record["bbox"][0]
    box2 = record["bbox"][1]
    
    x1_min, y1_min, x1_max, y1_max = box1
    x2_min, y2_min, x2_max, y2_max = box2

    # 두 bounding box가 겹치지 않는 경우
    if (x1_max < x2_min or x2_max < x1_min or y1_max < y2_min or y2_max < y1_min):
        return False
    # 두 bounding box가 겹치는 경우
    else:
        return True
    
# bbox의 ymax 비교 값 추출
def compare_ymin(box1, box2):
    return abs(box1[3] - box2[3])
        
    
    

# 데이터 프레임을 반복하면서 처리
for index1, row1 in data1.iterrows():  
    
    frame_num1, track_id1, xmin1, ymin1, xmax1, ymax1 = row1
    
    # 프레임 넘버가 이전과 같다면 동일한 프레임의 데이터라고 가정합니다.
    if frame_num1 == prev_frame_num:
        frame_data_list1[-1]["id"].append(track_id1)
        frame_data_list1[-1]["bbox"].append([xmin1, ymin1, xmax1, ymax1])
        
    else:
        # 새로운 프레임 넘버를 만났으므로 이를 기록하고 처리합니다.
        prev_frame_num = frame_num1
        frame_data_list1.append({"frame_num": frame_num1, "id": [track_id1], "bbox": [[xmin1, ymin1, xmax1, ymax1]]})
        
    
# print(frame_data_list1)
              

prev_frame_num = None     
   
for index2, row2 in data2.iterrows():   
    frame_num2, track_id2, xmin2, ymin2, xmax2, ymax2 = row2    
     
    if frame_num2 == prev_frame_num:
        frame_data_list2[-1]["id"].append(track_id2)
        frame_data_list2[-1]["bbox"].append([xmin2, ymin2, xmax2, ymax2])
    else:
        # 새로운 프레임 넘버를 만났으므로 이를 기록하고 처리합니다.
        prev_frame_num = frame_num2
        frame_data_list2.append({"frame_num": frame_num2, "id": [track_id2], "bbox": [[xmin2, ymin2, xmax2, ymax2]]}) 
        
        
# print(frame_data_list2)

  
first_video_id = [1,2]
second_video_id = [6,10]

df1 = []
df2 = []


for record1, record2 in zip(frame_data_list1, frame_data_list2):
    
    # 바뀌었는지 확인하는 과정 먼저 진행
    # if len(record1["id"]) == 2 and len(prev_record1["id"]) == 2:
    #     if check_overlap(record1): # 겹쳐있는지 확인
    #         # print(prev_record1)
            
    #         if (prev_record1["bbox"][0][3] is not None) and (prev_record1["bbox"][1][3] is not None):
    #             if compare_ymin(record1["bbox"][0], prev_record1["bbox"][0]) > compare_ymin(record1["bbox"][0], prev_record1["bbox"][1]): # 뒤에 것이 더 유사하다고 판단한 경우
    #                 if record1["id"][0] != prev_record1["id"][1]:
    #                     # 현재 기준 이후 1, 2 바꾸기
    #                     for record in frame_data_list1:
    #                         if record["id"] == 2:
    #                             if (record["id"][0] in first_video_id) and (record["id"][1] in first_video_id):
    #                                 record["id"][0], record["id"][1] = record["id"][1], record["id"][0]
    
    
                            
                        
    # if len(record2["id"]) == 2 and len(prev_record2["id"]) == 2:
    #     if check_overlap(record2): # 겹쳐있는지 확인
    #         # print(prev_record2)
            
    #         if (prev_record2["bbox"][0][3] is not None) and (prev_record2["bbox"][1][3] is not None):
    #             if compare_ymin(record2["bbox"][0], prev_record2["bbox"][0]) > compare_ymin(record2["bbox"][0], prev_record2["bbox"][1]): # 뒤에 것이 더 유사하다고 판단한 경우
    #                 if record2["id"][0] != prev_record2["id"][1]:
    #                     # 현재 기준 이후 1, 2 바꾸기
    #                     for record in frame_data_list2:
    #                         if record["id"] == 2:
    #                             if (record["id"][0] in second_video_id) and (record["id"][1] in second_video_id):
    #                                 record["id"][0], record["id"][1] = record["id"][1], record["id"][0]
    
    
    # if (first_video_id[0] in record1["id"] and second_video_id[0] in record2["id"]) or (first_video_id[1] in record1["id"] and second_video_id[1] in record2["id"]): # first_video_id의 개수가 2개인 상태부터 시작하게 하면 됨
    #     # 양쪽에 똑같은 것이 보이는 경우 -> 어떤 걸 살려야할까? -> 일단 cam2 바꾸자
    #     second_video_id[0], second_video_id[1] = second_video_id[1], second_video_id[0] # 일단 임시로 ㄱㄱ
    #     print("second_video_id: ", second_video_id)
    #     print(record2["frame_num"])
            
            
        
    if len(record1["id"]) == 2: # cam1에서 탐지한 객체가 2개인 상태
        if ((first_video_id[0] in prev_record1["id"]) and (first_video_id[0] not in record1["id"]))     or      ((first_video_id[1] in prev_record1["id"]) and (first_video_id[1] not in record1["id"])): 
            # cam1에서 이전엔 1이 있는데 지금은 없어 -> 새로운 id가 부여됐다고 봐야 함. -> 어떤 id가 새로운 id로 바뀐 건지 확인했음
            new_id = [id_ for id_ in record1["id"] if id_ not in first_video_id]
            target_id = [id_ for id_ in first_video_id if id_ not in record1["id"]]
            
            print("1번 : ...",record1["frame_num"])
            print(new_id)
            print(target_id)
            
            for original, change in zip(new_id, target_id):
                record1["id"][record1["id"].index(original)] = change
                # record1["id"].replace(original, change)
        
            # for index, original_id in enumerate(record1["id"]):
            #     for change_id in target_id:
            #         if id == change_id:
            #             record1["id"][index] = target_id[0]
                    
        # print(record1)
                    
    if len(record2["id"]) == 2: # cam2에서 탐지한 객체가 2개인 상태
    
                    
        if ((second_video_id[0] in prev_record2["id"]) and (second_video_id[0] not in record2["id"]))      or    ((second_video_id[1] in prev_record2["id"]) and (second_video_id[1] not in record2["id"])): 
            
            # print(record2["frame_num"])
            # cam2에서 이전엔 1이 있는데 지금은 없어 -> 새로운 id가 부여됐다고 봐야 함. -> 어떤 id가 새로운 id로 바뀐 건지 확인했음
            new_id = [id_ for id_ in record2["id"] if id_ not in second_video_id]
            target_id = [id_ for id_ in second_video_id if id_ not in record2["id"]]
            
            # print(new_id)
            # print(target_id)
            
            print("2번 : ...",record2["frame_num"])
            print(new_id)
            print(target_id)
            
            for original, change in zip(new_id, target_id):
                record2["id"][record2["id"].index(original)] = change
            
            # for index, id in enumerate(record2["id"]):
            #     if id == new_id[0]:
            #         record2["id"][index] = target_id[0]
                    
            # print(record1)
            # print(record2)
                    
    # print(record2)
    
    if len(record1["id"]) != 2: # cam 1에서 탐지한 객체가 2개가 아닌 상태
   
        
        
        if (first_video_id[0] not in record1["id"]) and (second_video_id[0] in record2["id"]): # 1번 캠에서 1이 가려졌는데 2번 캠에는 있는 경우
            record1["id"].append(first_video_id[0])
            record1["bbox"].append([None,None,None,None])
            
            # print(first_video_id[0])
            
        if (first_video_id[1] not in record1["id"]) and (second_video_id[1] in record2["id"]): # 1번 캠에서 2가 가려졌는데 2번 캠에는 있는 경우 
            record1["id"].append(first_video_id[1])
            record1["bbox"].append([None,None,None,None])
            
        # 3개 이상인 경우 전처리 해야 해
        if len(record1["id"]) > 2:
            delete_idx = []
            for index, _id in enumerate(record1["id"]):
                if _id not in first_video_id:
                    delete_idx.append(index)
                    
            for index in delete_idx:
                record1["id"].pop(index)
                record1["bbox"].pop(index)
        
        # print(record1["frame_num"])
            
        new_id = [id_ for id_ in record1["id"] if id_ not in first_video_id]
        target_id = [id_ for id_ in first_video_id if id_ not in record1["id"]]
        
        for original, change in zip(new_id, target_id):
                record1["id"][record1["id"].index(original)] = change
        
        # if len(new_id) > 1 and len(target_id) > 1:
        #     # print(record1["frame_num"])
            
        #     for index, id in enumerate(record1["id"]):
        #         if id == new_id[0]:
        #             record1["id"][index] = target_id[0]
            
    # print(record1)
        
    #################################################################################################################################################################################################    
       
    if len(record2["id"]) != 2: # cam 2에서 탐지한 객체가 2개가 아닌 상태
        
        
        if (second_video_id[0] not in record2["id"]) and (first_video_id[0] in record1["id"]): # 2번 캠에서 1이 가려졌는데 1번 캠에는 있는 경우
            record2["id"].append(second_video_id[0])
            record2["bbox"].append([None,None,None,None])
        
        elif (second_video_id[1] not in record2["id"]) and (first_video_id[1] in record1["id"]): # 2번 캠에서 2가 가려졌는데 1번 캠에는 있는 경우
            record2["id"].append(second_video_id[1])
            record2["bbox"].append([None,None,None,None])
        
        
        print("original: ", record2)
        if len(record2["id"]) > 2:
            
            delete_idx = []
            for index, _id in enumerate(record2["id"]):
                if _id not in second_video_id:
                    delete_idx.append(index)
                    
            for index in delete_idx:
                record2["id"].pop(index)
                record2["bbox"].pop(index)
        
        
        new_id = [id_ for id_ in record2["id"] if id_ not in second_video_id]
        target_id = [id_ for id_ in second_video_id if id_ not in record2["id"]]
        
        for original, change in zip(new_id, target_id):
                record2["id"][record2["id"].index(original)] = change
        
        
        # print(record1["frame_num"])
        # print(new_id)
        # print(target_id)
        # if len(new_id) > 0 and len(target_id) > 0:
        #     # print(record2["frame_num"])
        #     # print(new_id)
        #     # print(target_id)
        
        #     for index, id in enumerate(record2["id"]):
        #         if id == new_id[0]:
        #             record2["id"][index] = target_id[0]
                
                
            
    if ((len(record1["id"]) == 1) and (len(record2["id"]) == 1)) and record1["frame_num"] > 200:
        if (first_video_id[0] in record1["id"] and second_video_id[0] in record2["id"]) or (first_video_id[1] in record1["id"] and second_video_id[1] in record2["id"]):
            # print(record1)
            # print(record2)
            second_video_id[0], second_video_id[1] = second_video_id[1], second_video_id[0] # 일단 임시로 ㄱㄱ
        # print("second_video_id: ", second_video_id)
        # print(record2["frame_num"])
                    
    # print(record2)
    
    prev_record1 = record1
    prev_record2 = record2
    
    
    frame_num = record1['frame_num']
    for track_id, box in zip(record1['id'], record1['bbox']):
        csv_writer1.writerow({'frame_num': frame_num, 'track_id': track_id, 'xmin': box[0], 'ymin': box[1], 'xmax': box[2], 'ymax': box[3]})
        
    frame_num = record2['frame_num']
    for track_id, box in zip(record2['id'], record2['bbox']):
        csv_writer2.writerow({'frame_num': frame_num, 'track_id': track_id, 'xmin': box[0], 'ymin': box[1], 'xmax': box[2], 'ymax': box[3]})
    
# Close the CSV file
csv_file1.close()
csv_file2.close()

# print(second_video_id)