import pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

origin_data_location = '/home/amr-server/motion_ws/src/OpenTraj/opentraj/toolkit/my_test/origin_data/ETH.csv'
df = pd.read_csv(origin_data_location)

split_frame_num = 6

FIRST=True
sample=[]
sample_cnt=0
target=[]
save_folder = '../split_data/'
file_name = 0

for i in range(len(df)):
  lst = df.iloc[i]
  new_frame = lst[0]
  ped_id = int(lst[1])

  if FIRST:
    frame = new_frame
    FIRST=False
    sample.append(lst)
    continue
  else:
    pass

  # next sample  
  if frame != new_frame:
    sample_cnt += 1
    frame = new_frame
    
    #reset
    while sample_cnt == split_frame_num:
      file_name += 1

      others_data = sample
      sample = []
      sample_cnt = 0
      df_others = pd.DataFrame(others_data)
      df_others.columns = ['frame_id', 'agent_id', 'pos_x', 'pos_y', 'vel_x', 'vel_y', 'scene_id', 'label', 'timestamp']
      with open(save_folder+ '{0:03}'.format(file_name)+'.csv', mode= 'a') as f:
        df_others.to_csv(f, header = True, index = False)
      FIRST = True
      sample.append(lst)
      continue

    sample.append(lst)

  else:
    sample.append(lst)
  

  