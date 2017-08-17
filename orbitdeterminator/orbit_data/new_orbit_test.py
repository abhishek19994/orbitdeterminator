from orbitdeterminator.filters import (triple_moving_average, sav_golay, combo)
from orbitdeterminator.kep_determination import (lamberts_kalman, interpolation, gibbs)
from orbitdeterminator.util import read_data
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pylab as plt
pd.set_option('display.width', 1000)
import os
import sys
import time

# first read and save to a list all the file names
dir_path = os.path.dirname(os.path.realpath(__file__))
list_of_files = [x[2] for x in os.walk(dir_path)]
list_of_files = list_of_files[0]
file_list = [i.split('\t', 1)[0] for i in list_of_files]
file_list = file_list[1:]


# second separate all the meta files and the sim files (needed for simulation)
meta_list = []
sim_list = []
for name in file_list:
    if name.endswith("meta.csv"):
        meta_list.append(name)
    else:
        sim_list.append(name)
start = time.time()
error_2 = []


for i in range(2, 3):

    # read the correct keplerian elements from meta list
    correct_kep = np.genfromtxt(meta_list[i])
    correct_kep = correct_kep[1, 4:]
    correct_kep[0] = correct_kep[0] / 1000
    correct_kep[4], correct_kep[3] = correct_kep[3], correct_kep[4]

    # read the file that has time,x,y,z and is needed for computation
    print(sim_list[i])
    # data = read_data.load_data(sim_list[i])
    data = np.genfromtxt(sim_list[i])
    data = data[1:, :]

    data[:, 1:4] = data[:, 1:4] / 1000

    c = combo.c(20)
    window_golay = len(data) / c
    window_golay = int(window_golay)
    if window_golay % 2 == 0:
        window_golay = window_golay + 1

    data = triple_moving_average.generate_filtered_data(data, 3)

    # for window in range(251, 1051, 20):
    #     print(window)
    filtered_data = sav_golay.golay(data, window_golay, 3)

    filtered_data = filtered_data[~np.isnan(filtered_data).any(axis=1)]

    try:
        kep = lamberts_kalman.create_kep(filtered_data)
            # kep = gibbs.create_kep(filtered_data)
            # kep_final = interpolation.main(filtered_data)

        kep_final = lamberts_kalman.kalman(kep, 0.01 ** 2)
        error_2.append(np.ravel(kep_final - correct_kep))
    except:
        pass
    print(i)
            # print(correct_kep, kep_final)

        # error_2.append(np.ravel(kep_final - correct_kep))
# print(correct_kep)
# error = np.transpose(error)
df = (pd.DataFrame(error_2))
print(df)
# np.savetxt("error.csv", df, delimiter="  ,  ")
end = time.time()
print(end - start)
# print(kep_final)

# # np.savetxt("filtered.csv", filtered_data, delimiter=",")
#
# # ## Finally we plot the graph
# # mpl.rcParams['legend.fontsize'] = 10
# # fig = plt.figure()
# # ax = fig.gca(projection='3d')
# # ax.plot(data[:, 1], data[:, 2], data[:, 3], ".", label='Initial data ')
# # ax.plot(filtered_data[:, 1], filtered_data[:, 2], filtered_data[:, 3], "k", linestyle='-',
# #         label='Filtered data')
# # # ax.plot(positions[0, :], positions[1, :], positions[2, :], "r-", label='Orbit after Lamberts - Kalman')
# # ax.legend()
# # ax.can_zoom()
# # ax.set_xlabel('x (km)')
# # ax.set_ylabel('y (km)')
# # ax.set_zlabel('z (km)')
# # plt.show()
#

#
# # kep_final = interpolation.main(filtered_data)
#
# # kep = gibbs.create_kep(filtered_data)
# #
# # kep_final = lamberts_kalman.kalman(kep, 0.01 ** 2)
#
# kep_correct = np.array([[6649.576019931621,	0.8980960272830075,	109.64928714039931,	287.4973229274337, 272.06421941119504,	268.3299717534594]])
# print(kep_final - kep_correct)



