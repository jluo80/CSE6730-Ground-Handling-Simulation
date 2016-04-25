# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:44:20 2016

@author: sumsen
"""

import itertools
import random

import simpy


RANDOM_SEED = 42
SERVICE_HUB_SIZE = 17000     # liters (tank size * 10)
THRESHOLD = 10             # Threshold for calling the tank truck (in %)
WATER_TANK_SIZE = 1700        # liters (sourced from internet for large aircraft)
WATER_TANK_LEVEL = [50, 1500]  # Min/max levels of water tanks (in liters)
REFILLING_SPEED = 0.2        # liters / second
TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
T_INTER = [30, 300]        # Create a aircraft every [min, max] seconds
SIM_TIME = 1000            # Simulation time in seconds


def airc(name, env, service_hub, water_pump):
    """A aircraft arrives at the service hub for refilling.

    It requests one of the service hub's water pumps and tries to get the
    desired amount of water from it. If the stations reservoir is
    depleted, the aircraft has to wait for the tank truck to arrive.

    """
    water_tank_level = random.randint(*WATER_TANK_LEVEL)
    print('%s arriving at airport at %.1f' % (name, env.now))
    with service_hub.request() as req:
        start = env.now
        # Request one of the water truck
        yield req

        # Get the required amount of water
        liters_required = WATER_TANK_SIZE - water_tank_level
        yield water_pump.get(liters_required)

        # The "actual" refilling process takes some time
        yield env.timeout(liters_required / REFILLING_SPEED)

        print('%s finished refilling in %.1f seconds.' % (name,
                                                          env.now - start))


def service_hub_control(env, water_pump):
    """Periodically check the level of the *water_pump* and call the tank
    truck if the level falls below a threshold."""
    while True:
        if water_pump.level / water_pump.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Calling tank truck at %d' % env.now)
            # Wait for the tank truck to arrive and rewater the station
            yield env.process(tank_truck(env, water_pump))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, water_pump):
    """Arrives at the service hub after a certain delay and refills it."""
    yield env.timeout(TANK_TRUCK_TIME)
    print('Tank truck arriving at time %d' % env.now)
    ammount = water_pump.capacity - water_pump.level
    print('Tank truck refilling %.1f liters.' % ammount)
    yield water_pump.put(ammount)


def airc_generator(env, service_hub, water_pump):
    """Generate new aircrafts that arrive at the service hub."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(airc('Aircraft %d' % i, env, service_hub, water_pump))


# Setup and start the simulation
print('Service Hub refilling')
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
service_hub = simpy.Resource(env, 2)
water_pump = simpy.Container(env, SERVICE_HUB_SIZE, init=SERVICE_HUB_SIZE)
env.process(service_hub_control(env, water_pump))
env.process(airc_generator(env, service_hub, water_pump))

# Execute!
env.run(until=SIM_TIME)