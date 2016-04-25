
import itertools
import random

import simpy


RANDOM_SEED = 42
SERVICE_HUB_SIZE = 200     # liters
THRESHOLD = 10             # Threshold for calling the tank truck (in %)
FUEL_TANK_SIZE = 50        # liters
FUEL_TANK_LEVEL = [5, 25]  # Min/max levels of fuel tanks (in liters)
REFUELING_SPEED = 2        # liters / second
TANK_TRUCK_TIME = 300      # Seconds it takes the tank truck to arrive
T_INTER = [30, 300]        # Create an aircraft every [min, max] seconds
SIM_TIME = 1000            # Simulation time in seconds


def aircraft(name, env, service_hub, fuel_pump):
    """A aircraft arrives at the service hub for refueling.

    It requests one of the service hub's fuel pumps and tries to get the
    desired amount of gas from it. If the stations reservoir is
    depleted, the aircraft has to wait for the tank truck to arrive.

    """
    fuel_tank_level = random.randint(*FUEL_TANK_LEVEL)
    print('%s arriving at service hub at %.1f' % (name, env.now))
    with service_hub.request() as req:
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


def service_hub_control(env, fuel_pump):
    """Periodically check the level of the *fuel_pump* and call the tank
    truck if the level falls below a threshold."""
    while True:
        if fuel_pump.level / fuel_pump.capacity * 100 < THRESHOLD:
            # We need to call the tank truck now!
            print('Calling tank truck at %d' % env.now)
            # Wait for the tank truck to arrive and refuel the station
            yield env.process(tank_truck(env, fuel_pump))

        yield env.timeout(10)  # Check every 10 seconds


def tank_truck(env, fuel_pump):
    """Arrives at the service hub after a certain delay and refuels it."""
    yield env.timeout(TANK_TRUCK_TIME)
    print('Tank truck arriving at time %d' % env.now)
    ammount = fuel_pump.capacity - fuel_pump.level
    print('Tank truck refuelling %.1f liters.' % ammount)
    yield fuel_pump.put(ammount)


def aircraft_generator(env, service_hub, fuel_pump):
    """Generate new aircrafts that arrive at the service hub."""
    for i in itertools.count():
        yield env.timeout(random.randint(*T_INTER))
        env.process(aircraft('Aircraft %d' % i, env, service_hub, fuel_pump))


# Setup and start the simulation
print('Service Hub Refuelling')
random.seed(RANDOM_SEED)

# Create environment and start processes
env = simpy.Environment()
service_hub = simpy.Resource(env, 2)
fuel_pump = simpy.Container(env, SERVICE_HUB_SIZE, init=SERVICE_HUB_SIZE)
env.process(service_hub_control(env, fuel_pump))
env.process(aircraft_generator(env, service_hub, fuel_pump))

# Execute!
env.run(until=SIM_TIME)