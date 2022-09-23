import pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt
import AngularGrid
from glob import glob
import os

home = os.path.expanduser("~")
pkg_location = home + "/motion_ws/src/OpenTraj/opentraj/toolkit/my_test/output/ETH/"
folder = pkg_location + "SplitByTime/"
output_frame_num = 5
num_of_pieces = 72
max_dist = 8

def get_ped_info(ped_info):

  ped_id = ped_info[1]
  ped_frame = ped_info[0]
  
  return ped_frame, ped_id

def get_target_set(df):
  first_frame = df.iloc[0]['frame_id']
  target_set = []

  for i in range(len(df)):
    ped_info = df.iloc[i]
    ped_frame, ped_id = get_ped_info(ped_info)
    if ped_frame != first_frame:
      break
    else:
      target_set.append(ped_id)

  return target_set

def split_data(df, target):
    FIRST = True
    target_state=[]
    target_output=[]
    other_state=[]
    first_frame = df.iloc[0]['frame_id']

    for i in range(len(df)):
      ped_info = df.iloc[i]
      ped_frame, ped_id = get_ped_info(ped_info)
      if ped_id == target:
        if FIRST:
          FIRST = False
          target_state.append(ped_info)
        else:
          target_output.append(ped_info)

      elif ped_frame == first_frame:
        other_state.append(ped_info)
      else:
        pass
    return target_state, target_output, other_state

cnt = 0

for file in glob(os.path.join(folder,"*.csv")):
  file_name = file.split('/')[-1]
  file_name = file_name.split('.csv')[0]
  df = pd.read_csv(file)
  cols = ['frame_id', 'agent_id', 'pos_x', 'pos_y', 'vel_x', 'vel_y', 'scene_id', 'label', 'timestamp']
  target_set = get_target_set(df)
  # print('file', file_name,'target:',target_set,'working!')

  for target in target_set:
    target_state, target_output, other_state = split_data(df, target)

    target_state = pd.DataFrame(target_state)
    target_state.columns = cols

    try:
      target_output = pd.DataFrame(target_output)
      target_output.columns = cols
      if len(target_output) != output_frame_num:
        print("file", file_name, "target:", target, "doesn't have the complete trajactory!")
        continue
    except:
      print("file", file_name, "target:", target, "doesn't have the complete trajactory!")
      continue

    try:
      other_state = pd.DataFrame(other_state)
      other_state.columns = cols
      target_pt = AngularGrid.get_pt(target_state.iloc[0])
      ag = [AngularGrid.get_AngularGrid(other_state, target_pt, num_of_pieces= num_of_pieces, max_dist= max_dist)]
      ag = pd.DataFrame(ag)
    except:
      ag = [np.ones(num_of_pieces)]
      ag = pd.DataFrame(ag)
      print("file", file_name, "target:", target, "doesn't have the others!")

    target_state.to_csv(pkg_location + 'train_x/' + str(file_name) + '_' + str(target) +'.csv', header = True, index = False)
    target_output.to_csv(pkg_location + 'train_y/' + str(file_name) + '_' + str(target) +'.csv', header = True, index = False)
    ag.to_csv(pkg_location + 'train_ag/' + str(file_name) + '_' + str(target) +'.csv', header = True, index = False)
    cnt+=1

print(cnt)