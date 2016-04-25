import random
import sys
import simpy

from ServiceHub import ServiceHub as sh
from Aircraft import Aircraft as ac

# ================Setup================

RANDOM_SEED = 42
NUM_TRUCKS1 = 2             # Number of trucks for cleaning in the servicehub
NUM_TRUCKS2 = 2             # Number of trucks for water supply in the servicehub
NUM_TRUCKS3 = 2             # Number of trucks for power supply in the servicehub
CLEANTIME = 10              # Minutes it takes to clean an aircraft
WATERTIME = 10              # Minutes it takes to supply water to an aircraft
POWERTIME = 10              # Minutes it takes to power up an aircraft
SIM_TIME = 120              # Simulation time in minutes
T_INTER = [30, 300]         # Create an aircraft every [min, max] mins

# class Main(object):
#     def __init__(self, env, num_trucks1, num_trucks2, num_trucks3, cleantime, watertime, powertime):
#         self.env = env
#         self.name = name
#         self.size = size
def aircraft(name, env, service_hub, fuel_pump, Gates):
    """A car arrives at the gas station for refueling.
        
        It requests one of the gas station's fuel pumps and tries to get the
        desired amount of gas from it. If the stations reservoir is
        depleted, the car has to wait for the tank truck to arrive.
        
        """
    
    
    fuel_tank_level = random.randint(*FUEL_TANK_LEVEL)
    print('%s arriving at airport at %.1f' % (name, env.now))
    if 
    with gas_station_control.request() as req:
        start = env.now
        # Request one of the gas pumps
        yield req
        
        # Get the required amount of fuel
        liters_required = FUEL_TANK_SIZE - fuel_tank_level
        yield fuel_pump.get(liters_required)
        
        # The "actual" refueling process takes some time
        yield env.timeout(liters_required / REFUELING_SPEED)
        
        print('%s finished refueling in %.1f seconds.' % (name,
                                                          env.now - start))


def aircraft_generator(env, service_hub, fuel_pump):
    """Generate new aircrafts that arrive at the service hub."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(aircraft('Aircraft %d' % i, env, service_hub, fuel_pump))

# Setup and start the simulation
print('Aircraft Service Ground Handling')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
# Create the servicehub
service_hub = sh(env, 2, 10)
# Create one aircraft
env.process(gas_station_control(env, fuel_pump))
env.process(aircraft_generator(env, gas_station, fuel_pump))

env.run(until=500)


# if __name__ == '__main__': Main()
