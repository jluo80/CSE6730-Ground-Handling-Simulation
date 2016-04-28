from RNG import *
import simpy
import numpy as np
from random import seed, randint
import matplotlib.pyplot as plt
import csv
import sys
# ====================Generate Arrival Schedule Based on Long Beach Airport Data====================
generator = ClassRanGen()
arrive_depart_schedule = []
cdf = [0.07, 0.14, 0.2, 0.25, 0.31, 0.35, 0.41, 0.45, 0.51, 0.54, 0.65, 0.68, 0.79, 0.86, 0.96, 1]
real_time = [40, 40, 40, 40, 40, 40, 40, 45, 47, 49, 60, 60, 60, 60, 60, 60, 60, 62, 64, 70, 75, 75, 75, 75, 75, 75, 75, 94, 94, 94, 94, 94, 94, 94, 136, 136, 136, 136, 136, 136, 136, 180, 180, 180, 180, 180, 180, 180, 190, 190, 190, 190, 190, 240, 240, 240, 240, 240, 240, 240, 245, 245, 245, 245, 245, 245, 245, 255, 255, 255, 255, 255, 255, 289, 307, 307, 307, 307, 307, 307, 307, 340, 369, 390, 390, 390, 390, 390, 390, 390, 412, 412, 412, 412, 412, 412, 412, 425, 425, 425, 425, 425, 425, 425, 445, 445, 495, 495, 495, 495, 495, 495, 495, 500, 500, 500, 500, 500, 500, 500, 575, 575, 575, 575, 575, 575, 575, 583, 585, 606, 630, 632, 635, 635, 635, 635, 635, 635, 635, 635, 635, 635, 635, 635, 635, 635, 639, 639, 639, 639, 639, 639, 639, 672, 672, 672, 672, 672, 672, 672, 730, 730, 730, 730, 730, 730, 730, 733, 733, 733, 733, 733, 733, 733, 744, 744, 744, 744, 744, 744, 744, 748, 748, 748, 748, 748, 748, 748, 786, 787, 790, 790, 805, 805, 805, 805, 805, 805, 805, 819, 819, 822, 823, 823, 833, 855, 860, 860, 860, 860, 860, 860, 860, 875, 875, 875, 875, 875, 875, 875, 880, 880, 880, 880, 880, 880, 880, 930, 930, 930, 930, 934, 934, 934, 934, 934]
real_frequency = [17, 17, 14, 12, 14, 8, 15, 9, 14, 9, 24, 7, 28, 17, 22, 9]

for i in range(20000):
    random1 = round(generator.Rand(),2)
    random2 = round(generator.Rand(),2)
    start_time = 6 * 60 # Start from 6 a.m. (unit: min)
    time_interval = 60 # Time step (unit: min)
    if random1 < cdf[0]:
        random_arrival_time = 60 * random2 + start_time
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[1]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 1
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[2]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 2
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[3]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 3
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[4]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 4
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[5]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 5
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[6]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 6
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[7]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 7
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[8]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 8
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[9]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 9
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[10]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 10
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[11]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 11
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[12]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 12
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[13]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 13
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[14]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 14
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < cdf[15]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 15
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    else:
        random_arrival_time = 60 * random2 + start_time + time_interval * 16
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])

# Aircraft Arrival Schedule List: From 6 a.m. till 10 p.m.
arrive_depart_schedule = sorted(arrive_depart_schedule)
arrive_schedule = []
for i in arrive_depart_schedule:
 arrive_schedule.append(i[0]-360)
# print(arrive_depart_schedule)
# print(arrive_schedule)


bins = np.linspace(0, 960, 16)
x = plt.hist(arrive_schedule, bins, alpha=0.5, label='simulated arrival time', color='g')


# plt.hist(real_time, bins, alpha=0.5, label='real data')
plt.legend(loc='upper right')
plt.title("Aircraft Arrival Time Schedule")
plt.xlabel("Time Schedule")
plt.ylabel("Frequency %")
plt.show()