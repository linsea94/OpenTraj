import sys, os
# sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'../'))
# print(sys.path)
import pandas as pd
import numpy as np
import csv
import math
import matplotlib.pyplot as plt

df = pd.read_csv('/home/amr-server/motion_ws/src/OpenTraj/opentraj/toolkit/my_test/8415.csv')

class pt:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  def distance(target, other):
    dist = (target.x - other.x)**2 + (target.y-other.y)**2
    return np.round(math.sqrt(dist), 4)
  def direction(target, other, num_of_pieces=8):
    a = other.y - target.y
    b = other.x - target.x
    theta = (round(np.arctan2(a, b)/math.pi*180,4))
    if theta < 0:
      theta = theta + 360
    a_pieces = 360 / num_of_pieces
    dir = int(theta / a_pieces)
    return dir

num_of_pieces = 72
max_dist = 10
target_id = 4
target = df.iloc[target_id]
target_pt = pt(target[2],target[3])
# plt.scatter(target[2], target[3])
# plt.text(target[2],target[3], target_id)
# other = df.iloc[10]
# other_pt = pt(other[2],other[3])
# dist = pt.distance(target_pt, other_pt)
# dir = pt.direction(target_pt, other_pt, num_of_pieces)

surrounding = np.ones(num_of_pieces)
for i in range(0,len(df)):
  if i == target_id:
    continue
  else:
    pass
  other = df.iloc[i]
  other_pt = pt(other[2],other[3])
  # plt.scatter(other[2],other[3])
  # plt.text(other[2],other[3], i)
  dist = pt.distance(target_pt, other_pt)
  dist = np.round(dist / max_dist, 4)
  if dist > 1:
    continue
  else:
    pass
  dir = pt.direction(target_pt, other_pt, num_of_pieces)
  if dist < surrounding[dir]:
    surrounding[dir] = dist

cmap = plt.get_cmap("Reds")
color = cmap(np.array(np.abs(surrounding-1)))
img = plt.pie(np.ones(num_of_pieces),
        explode = surrounding,
        labels = surrounding,
        colors = color,
        textprops = {"fontsize" : 10})
plt.show()
# plt.savefig('/home/amr-server/motion_ws/src/OpenTraj/opentraj/toolkit/my_test/surrounding.jpg')