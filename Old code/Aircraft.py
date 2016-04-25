import random
import simpy
from mpi4py import MPI

# ================Aircrafts================

class Aircraft(object):
    """The aircraft process (each aircraft has a ``name``) arrives at the servicehub
    (``sh``) and requests a service truck.

    It then starts the service process, waits for it to finish and
    leaves to never come back ...

    """
    def __init__(self, env, name, size):
        self.env = env
        self.name = name
        self.size = size

    def request_service(self):
        arrivalTime = self.env.now
        print('%s arrives at the servicehub at %.2f.' % (self.name, arrivalTime))



    # with sh.truck.request() as request:
    #     yield request
    #     enterTime = self.env.now
    #     print('%s enters the servicehub at %.2f.' % (name, enterTime))
    #     yield env.process(sh.clean(name))

    #     departTime = self.env.now
    #     print('%s departs the servicehub at %.2f.' % (name, departTime))

env = simpy.Environment()
A1 = Aircraft(env, "A1", 1)
A1.request_service()

env.run(until=500)
