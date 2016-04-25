from RNG import *
import simpy
from random import seed, randint

# Size factors depend on the size of aircraft.
SMALL_SIZE=1
LARGE_SIZE=1.5
HEAVY_SIZE=2.5
SMALL_SIZE_constant = 0.7
SMALL_SIZE_Power_constant = 0.9

class aircraft(object):
    def __init__(self, env, name, size, gate, res1, res2, res3, res4, res5, res6, arrival_air_time, departure_time):
        self.env = env
        self.name = name
        self.size = size
        self.gate = gate
        env.process(self.check_available_gate(env, name, size, gate, arrival_air_time, departure_time))


    def check_available_gate(self, env, name, size, gate, arrival_air_time, departure_time):
        # Wait for the time the plane is supposed to arrive
        yield env.timeout(arrival_air_time)
        print("%s requesting a gate at %.1f minutes" %(self.name, env.now))
        request = gate.request()

        # Request one of the 11 gates
        yield request
        landing_time = 5
        yield env.timeout(landing_time)

        # Generate new aircrafts that arrive at the service hub.
        arrival_time = env.now
        print("%s is landing at %.1f minutes." % (self.name, arrival_time))

        wait_time = 7  # wait time of 7 min applies for all aircrafts before processes can start - source Gantt chart in design doc
        yield env.timeout(wait_time)
        yield env.process(self.refuel_aircraft(env, res1, name, size, arrival_time, departure_time)) & env.process(self.water_aircraft(env, res2, name, size, arrival_time, departure_time)) & env.process(self.clean_aircraft(env, res3, name, size, arrival_time, departure_time))& env.process(self.cater_aircraft(env, res4, name, size, arrival_time, departure_time)) & env.process(self.power_aircraft(env, res5, name, size, arrival_time, departure_time)) & env.process(self.baggage_aircraft(env, res6, name, size, arrival_time, departure_time))
        if env.now >= departure_time:
            if env.now > departure_time + 15:
                print(name + " is late by %.1f minutes" % (env.now - departure_time))
            else:
                print(name + " is on time")
            print("All process are done.")
            print(name + " is departing at %.1f minutes" % (env.now))
            yield env.timeout(2) # Aircraft is leaving the gate.
            gate.release(request)
        else:
            yield env.timeout(departure_time-env.now)
            print("%s is early" % (name))
            print("All process are done.")
            print(name + " is departing at %.1f minutes" % (env.now))
            yield env.timeout(2) # Aircraft is leaving the gate.
            gate.release(request)


    def refuel_aircraft(self, env, resource, name, size, arrival_time, departure_time):
        # Requsting
        #Define the disembark time
        disembark_time = 7
        request = resource.request(priority=departure_time)  # Generate a request event
        start = env.now
        print(name + " --> FUEL request a resource at %.1f minutes." % start)
        yield request                 # Wait for access

        #Introduce a prcess specific wait to account for disembarking for refuel process
        yield env.timeout(disembark_time)

        # Working
        print(name + " --> FUEL working on at %.1f minutes." % env.now)
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE_constant * 17 #min
        elif size == LARGE_SIZE:
            working_duration = 17 #min
        else:
            working_duration = 28 #min
        yield env.timeout(working_duration)          # Do something
        print(name + " --> FUEL done at %.1f minutes." % env.now)
        end = env.now

        # Releasing
        resource.release(request)     # Release the resource
        print(name + " --> FUEL finished refueling in %.1f minutes." % (end - start))


    def water_aircraft(self, env, resource, name, size, arrival_time, departure_time):
        # Requsting
        #Define the disembark time
        disembark_time = 7
        request = resource.request(priority=departure_time)  # Generate a request event
        start = env.now
        print(name + " --> WATER request a resource at %.1f minutes." % start)
        yield request                 # Wait for access

        #Introduce a prcess specific wait to account for disembarking for supplying water process
        yield env.timeout(disembark_time)

        # Working
        print(name + " --> WATER working on at %.1f minutes." % env.now)
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE_constant * 11 #min
        elif size == LARGE_SIZE:
            working_duration = 11 #min
        else:
            working_duration = 14.5 #min
        yield env.timeout(working_duration)          # Do something
        print(name + " --> WATER done at %.1f mins." % env.now)
        end = env.now

        # Releasing
        resource.release(request)     # Release the resource
        print(name + " --> WATER finished supplying water in %.1f minutes." % (end - start))


    def clean_aircraft(self, env, resource, name, size, arrival_time, departure_time):
        # Requsting
        #Define the disembark time
        disembark_time = 7
        request = resource.request(priority=departure_time)  # Generate a request event
        start = env.now
        print(name + " --> CLEAN request a resource at %.1f minutes." % start)
        yield request                 # Wait for access

        #Introduce a prcess specific wait to account for disembarking for clening process
        yield env.timeout(disembark_time)
        resource.release(request)

        # Working
        print(name + " --> CLEAN working on at %.1f minutes." % env.now)
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE_constant * 11 #min
        elif size == LARGE_SIZE:
            working_duration = 11 #min
        else:
            working_duration = 29 #min
        yield env.timeout(working_duration)          # Do something
        print(name + " --> CLEAN done at %.1f mins." % env.now)
        end = env.now

        # Releasing
        resource.release(request)     # Release the resource
        print(name + " --> CLEAN finished cleaning in %.1f minutes." % (end - start))


    def cater_aircraft(self, env, resource, name, size, arrival_time, departure_time):
        # Requsting
        #Define the disembark time
        disembark_time = 7
        request = resource.request(priority=departure_time)  # Generate a request event
        start = env.now
        print(name + " --> CATER request a resource at %.1f minutes." % start)
        yield request                 # Wait for access

        #Introduce a process specific wait to account for disembarking for refuel process
        yield env.timeout(disembark_time)

        # Working
        print(name + " --> CATER working on at %.1f minutes." % env.now)
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE_constant * 15 #min
        elif size == LARGE_SIZE:
            working_duration = 15 #min
        else:
            working_duration = 30 #min
        yield env.timeout(working_duration)          # Do something
        print(name + " --> CATER done at %.1f minutes." % env.now)
        end = env.now

        # Releasing
        resource.release(request)     # Release the resource
        print(name + " --> CATER finished catering in %.1f minutes." % (end - start))


    def power_aircraft(self, env, resource, name, size, arrival_time, departure_time):
        # Requsting
        # do not use the disembark time since process can start earlier
        #disembark_time = 7
        request = resource.request(priority=departure_time)  # Generate a request event
        start = env.now
        print(name + " --> POWER request a resource at %.1f minutes." % start)
        yield request                 # Wait for access

        #DO NOT use disembarking for power process since it can coexist
        #yield env.timeout(disembark_time)

        # Working
        print(name + " --> POWER working on at %.1f minutes." % env.now)
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE_Power_constant * 44 #min
        elif size == LARGE_SIZE:
            working_duration = 44 #min
        else:
            working_duration = 54 #min
        yield env.timeout(working_duration)          # Do something
        print(name + " --> POWER done at %.1f minutes." % env.now)
        end = env.now

        # Releasing
        resource.release(request)     # Release the resource
        print(name + " --> POWER finished catering in %.1f minutes." % (end - start))


    # PROCESS Baggage involves loading the baggage of future passengers (departure) only
    def baggage_aircraft(self, env, resource, name, size, arrival_time, departure_time):
        # Requsting
        # do not use the disembark time since process can start earlier
        #disembark_time = 7
        request = resource.request(priority=departure_time)  # Generate a request event
        start = env.now
        print(name + " --> BAGGAGE request a resource at %.1f minutes." % start)
        yield request                 # Wait for access

        #DO NOT use disembarking for power process since it can coexist
        #yield env.timeout(disembark_time)

        # Working
        print(name + " --> BAGGAGE working on at %.1f minutes." % env.now)
        if size == SMALL_SIZE:
            working_duration = SMALL_SIZE_constant*16 #min
        elif size == LARGE_SIZE:
            working_duration = 16 #min
        else:
            working_duration = 28 #min
        yield env.timeout(working_duration)          # Do something
        print(name + " --> BAGGAGE done at %.1f minutes." % env.now)
        end = env.now

        # Releasing
        resource.release(request)     # Release the resource
        print(name + " --> BAGGAGE finished loading in %.1f minutes." % (end - start))



# ===============================Airport Ground Handling Simulation===============================
env = simpy.Environment()
# Regard gate as resource
# Regard trucks as priority resource
gate = simpy.Resource(env, capacity=11)
res1 = simpy.PriorityResource(env, capacity=2) # Refueling truck
res2 = simpy.PriorityResource(env, capacity=2) # Watering truck
res3 = simpy.PriorityResource(env, capacity=2) # Cleaning truck
res4 = simpy.PriorityResource(env, capacity=2) # Catering truck
res5 = simpy.PriorityResource(env, capacity=2) # Powering truck
res6 = simpy.PriorityResource(env, capacity=2) # Baggage truck


# ====================Generate Arrival Schedule Based on Long Beach Airport Data====================
generator = ClassRanGen()
arrive_depart_schedule = []
frequency = [0.07, 0.14, 0.2, 0.25, 0.31, 0.35, 0.41, 0.45, 0.51, 0.54, 0.65, 0.68, 0.79, 0.86, 0.96, 1]
# frequency = [0.06, 0.12, 0.18, 0.24, 0.30, 0.36, 0.42, 0.48, 0.54, 0.6, 0.66, 0.72, 0.78, 0.84, 0.90, 1]

for i in range(40):
    random1 = round(generator.Rand(),2)
    random2 = round(generator.Rand(),2)
    start_time = 6 * 60 # Start from 6 a.m. (unit: min)
    time_interval = 60 # Time step (unit: min)
    if random1 < frequency[0]:
        random_arrival_time = 60 * random2 + start_time
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[1]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 1
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[2]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 2
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[3]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 3
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[4]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 4
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[5]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 5
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[6]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 6
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[7]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 7
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[8]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 8
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[9]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 9
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[10]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 10
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[11]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 11
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[12]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 12
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[13]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 13
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[14]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 14
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    elif random1 < frequency[15]:
        random_arrival_time = 60 * random2 + start_time + time_interval * 15
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])
    else:
        random_arrival_time = 60 * random2 + start_time + time_interval * 16
        random_departure_time = random_arrival_time + float(randint(60, 120))
        arrive_depart_schedule.append([random_arrival_time, random_departure_time])

# Aircraft Arrival Schedule List: From 6 a.m. till 10 p.m.
arrive_depart_schedule = sorted(arrive_depart_schedule)
# print(arrive_depart_schedule)

# ====================Aircraft Generator====================
k = 1
for j in range(len(arrive_depart_schedule)):
    ID = 'Plane ' + str(k)

    # Size distribution based on the occurence of different size of aircraft
    s = randint(0,100)
    if s < 90:
        size = SMALL_SIZE
    elif s <94:
        size = LARGE_SIZE
    else:
        size = HEAVY_SIZE
    arrival_air_time = arrive_depart_schedule[j][0]
    departure_time = arrive_depart_schedule[j][1]
    #print arrival_air
    craft = aircraft(env, ID, size, gate, res1, res2, res3, res4, res5, res6, arrival_air_time, departure_time)
    k = k + 1
# print(k)

env.run()