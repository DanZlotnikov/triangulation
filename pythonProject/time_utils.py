import numpy as np
from numpy.linalg import norm


################################################################################################################
# This function calculate the difference in time of arrival with time steps of 10 seconds.                     #
# Most of the time the difference is less than 0.010 seconds.                                                  #
# The function know to handle changes in remainder of division 10 (for example t_lst=[39.996, 50.002, 59.995]) #
# The function returns the time difference in seconds.                                                         #
################################################################################################################
def calculate_time_difference(t_lst):
    time_mode10_lst = np.array(t_lst) % 10
    n = time_mode10_lst.shape[0]
    time_dif_lst = time_mode10_lst[1:n] - time_mode10_lst[0:n - 1]
    time_dif_lst = np.array([val if np.abs(val) < 1.0 else val + 10 * (val < 0) - 10 * (val >= 0)
                             for val in time_dif_lst])
    return time_dif_lst


def calculate_time_difference2(t_lst):
    n = t_lst.shape[0]
    time_dif_lst = (t_lst[1:n] - t_lst[0:n - 1]) % 10
    time_dif_lst = np.array([val if np.abs(val) < 1.0 else val + 10 * (val < 0) - 10 * (val >= 0)
                             for val in time_dif_lst])
    return time_dif_lst

