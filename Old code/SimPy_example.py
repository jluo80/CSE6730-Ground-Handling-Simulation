
import simpy


class Car(object):
    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            print('Start parking and charging at %d' % self.env.now)
            charge_duration = 5
            try:
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                print('Was interrupted.')

            print('Start driving at %d' % env.now)
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self, duration):
        yield self.env.timeout(duration)


def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()


env = simpy.Environment()
car = Car(env)
env.process(driver(env,car))
env.run(until=15)
