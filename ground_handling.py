# -*- coding: utf-8 -*-
# @Author: Jiahao
# @Date:   2016-04-13 10:21:41
# @Last Modified by:   Jiahao
# @Last Modified time: 2016-04-21 14:45:59

from RNG import *
import simpy
from random import seed, randint
import itertools
import numpy as np
import matplotlib.pyplot as plt

SMALL_SIZE = 1
LARGE_SIZE = 1.2


class aircraft(object):
    def __init__(self, env, name, size, gate, res1, res2):
        self.env = env
        self.name = name
        self.size = size
        self.gate = gate
        self.res1 = res1
        self.res2 = res2

        env.process(self.check_available_gate(env, name, size, gate))

    def check_available_gate(self, env, name, size, gate):
        request = gate.request()
        # Request one of the 11 gates
        yield request

        # Generate new aircrafts that arrive at the service hub. #
        arrival_time = env.now
        num_of_processes = 0
        print("%s is landing at %.1f mins." % (self.name, arrival_time))
        yield env.timeout(10)
        yield env.process(self.refuel_aircraft(env, res1, name, size, arrival_time)) & env.process(self.water_aircraft(env, res2, name, size, arrival_time))
        print("All process are done. " + name + " is departing now")
        gate.release(request)

    def refuel_aircraft(self, env, resource, name, size, arrival_time,):
        # Requsting
        request = resource.request()  # Generate a request event
        start = env.now
        print(name + "--> FUEL request a resource at %.1f mins." % start)
        yield request                 # Wait for access

        # Working
        print(name + "--> FUEL working on at %.1f mins." % env.now)
        unit_time_consuming = 2
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE * (unit_time_consuming)
        else:
            working_duration = LARGE_SIZE * unit_time_consuming
        yield env.timeout(working_duration)          # Do something
        print(name + "--> FUEL done at %.1f mins." % env.now)

        # Releasing
        resource.release(request)     # Release the resource
        print(name + "--> FUEL finished refueling in %.1f mins." % (env.now - start))


    def water_aircraft(self, env, resource, name, size, arrival_time):
        # Requsting
        request = resource.request()  # Generate a request event
        start = env.now
        print(name + "--> WATER request a resource at %.1f mins." % start)
        yield request                 # Wait for access

        # Working
        print(name + "--> WATER working on at %.1f mins." % env.now)
        unit_time_consuming = 2
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE * (unit_time_consuming)
        else:
            working_duration = LARGE_SIZE * unit_time_consuming
        yield env.timeout(working_duration)          # Do something
        print(name + "--> WATER done at %.1f mins." % env.now)

        # Releasing
        resource.release(request)     # Release the resource
        print(name + "--> WATER finished water supply in %.1f mins." % (env.now - start))





env = simpy.Environment()




gate = simpy.Resource(env, capacity=2)
res1 = simpy.PriorityResource(env, capacity=2)
res2 = simpy.PriorityResource(env, capacity=2)
A1 = aircraft(env, '1', SMALL_SIZE, gate, res1, res2)
A2 = aircraft(env, '2', LARGE_SIZE, gate, res1, res2)
A3 = aircraft(env, '3', LARGE_SIZE, gate, res1, res2)


temp_schedule = []
generator = ClassRanGen()
for i in range(50):
    random_arrival_time = round(24 * generator.Rand(), 2)
    temp_schedule.append(random_arrival_time)
random_arrival_time = sorted(temp_schedule)
print(random_arrival_time)

# # Gaussian distribution
# mu, sigma = 0, 0.1 # mean and standard deviation
# s = np.random.normal(mu, sigma, 1000)
# x = mu + sigma*np.random.randn(10000)


# count, bins, ignored = plt.hist(s, 30, facecolor='cyan', normed=True)
# plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *
#                np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#          linewidth=2, color='r')
# plt.show()

env.run()