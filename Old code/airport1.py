# Airport basic example
import simpy


def Plane(env, ID, arrive, gate, charge):
        yield env.timeout(arrive)
        print("Plane %d arrived at airport at time %d"
              % (ID, env.now))
        with gate.request() as req:
            yield req
            print ("Plane %d has taxied to gate at time %d"
                   % (ID, env.now))
            with charge.request() as req2:
                yield req2
                print ("Plane %d is charging at time %d"
                       % (ID, env.now))
                yield env.timeout(15)
                print ("Plane %d is leaving at time %d"
                       % (ID, env.now))

env = simpy.Environment()
gate = simpy.Resource(env, capacity=2)
charge = simpy.Resource(env, capacity=1)
for i in range(10):
    env.process(Plane(env, i, i*10, gate, charge))
env.run()
