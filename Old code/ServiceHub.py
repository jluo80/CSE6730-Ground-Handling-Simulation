import random
import simpy

import sys

# ================Service Hub================
class ServiceHub(object):
    """A servicehub has a limited number of trucks (``FUEL_TRUCKS_NUM``) to
    serve aircrafts in parallel.

    Aircrafts have to request one of the trucks. When they got one, they
    can start the service processes and wait for it to finish (which
    takes ``XXXXTIME`` minutes).

    """
    def __init__(self, env, fuel_trucks_num, refueltime):
        self.env = env
        self.fuel_trucks_num = fuel_trucks_num
        self.refueltime = refueltime


    def refuel(self, aircraft):
        """The refueling processes. It takes an ``aircraft`` processes and tries
        to refuel it."""
        print("Refueling")
        if self.fuel_trucks_num != 0:
            self.fuel_trucks_num = self.fuel_trucks_num - 1
            yield self.env.timeout(self.refueltime)
            print("Servicehub has refueled %d%% of %s's fuel." %
                  (random.randint(50, 99), aircraft))
        else:
            print("No more resource for now! Pending for service!")



# env = simpy.Environment()
# sh = ServiceHub(env, 2, 10)


# env.process(sh.refuel("A1"))
# env.process(sh.refuel("A"))

# env.run(until=500)
