
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))
from toolkit.loaders.loader_eth import load_eth
file_path = "/home/amr-server/motion_ws/src/motion_prediction/OpenTraj/datasets/ETH/seq_eth/obsmat.txt"
save_folder = "/home/amr-server/motion_ws/src/motion_prediction/OpenTraj/opentraj/toolkit/my_test/"
# fixme: replace OPENTRAJ_ROOT with the address to root folder of OpenTraj
traj_dataset = load_eth(file_path)
trajs = traj_dataset.get_trajectories()
data = traj_dataset.data
print(traj_dataset.data)

with open(save_folder +'ETH.csv', mode= 'a') as f:
  data.to_csv(f, header = True, index = False)