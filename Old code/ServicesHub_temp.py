import random

import simpy

RANDOM_SEED = 42
NUM_TRUCKS1 = 2      # Number of trucks in the servicehub
NUM_TRUCKS2 = 2
NUM_TRUCKS3 = 2
CLEANTIME = 10      # Minutes it takes to clean an aircraft
WATERTIME = 10      # Minutes it takes to supply water to an aircraft
POWERTIME = 10      # Minutes it takes to power up an aircraft
SIM_TIME = 120     # Simulation time in minutes


class ServiceHub(object):
    """A servicehub has a limited number of trucks (``NUM_TRUCKS``) to
    serve aircrafts in parallel.

    Aircrafts have to request one of the trucks. When they got one, they
    can start the service processes and wait for it to finish (which
    takes ``XXXXTIME`` minutes).

    """
    def __init__(self, env, num_trucks1, num_trucks2, num_trucks3, cleantime, watertime, powertime):
        self.env = env
        self.truck1 = simpy.Resource(env, num_trucks1)
        self.truck2 = simpy.Resource(env, num_trucks2)
        self.truck3 = simpy.Resource(env, num_trucks3)
        self.cleantime = cleantime
        self.watertime = watertime
        self.powertime = powertime

    def clean(self, aircraft):
        """The cleaning processes. It takes a ``aircraft`` processes and tries
        to clean it."""
        yield self.env.timeout(CLEANTIME)
        print("servicehub has removed %d%% of %s's dirt." %
              (random.randint(50, 99), aircraft))

    def water(self, aircraft):
        """The water supply processes. It takes a ``aircraft`` processes and tries
        to supply water it."""
        yield self.env.timeout(WATERTIME)
        print("servicehub has supplied %d%% of %s's water." %
              (random.randint(50, 99), aircraft))

    def power(self, aircraft):
        """The power supply processes. It takes a ``aircraft`` processes and tries
        to power it."""
        yield self.env.timeout(POWERTIME)
        print("servicehub has charged %d%% of %s's power." %
              (random.randint(50, 99), aircraft))


def aircraft(env, name, sh):
    """The aircraft process (each aircraft has a ``name``) arrives at the servicehub
    (``sh``) and requests a service truck.

    It then starts the service process, waits for it to finish and
    leaves to never come back ...

    """
    print('%s arrives at the servicehub at %.2f.' % (name, env.now))
    with sh.truck.request() as request:
        yield request

        print('%s enters the servicehub at %.2f.' % (name, env.now))
        yield env.process(sh.clean(name))

        print('%s leaves the servicehub at %.2f.' % (name, env.now))


def setup(env, num_trucks1, num_trucks2, num_trucks3, cleantime, watertime, powertime):
    """Create a servicehub, a number of initial aircrafts."""

    # Create the servicehub
    servicehub = ServiceHub(env, num_trucks1, num_trucks2, num_trucks3, cleantime, watertime, powertime)

    # Create 4 initial aircrafts
    for i in range(4):
        env.process(aircraft(env, 'aircraft %d' % i, servicehub))


# Setup and start the simulation
print('Service Hub')
random.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, NUM_TRUCKS1, NUM_TRUCKS2, NUM_TRUCKS3, CLEANTIME, WATERTIME, POWERTIME))

# Execute!
env.run(until=SIM_TIME)
