
import cPickle as pickle
#for x in rang
Num_planes = 40
num_runs = 5
num_trucks = 5
for num in range(num_runs):
    Planes = [dict() for x in range(Num_planes)]
    #print Planes2
    #Plane1 = dict([('Arrival', 0)])
    for line in open('New Data/' + str(num_trucks) + 'Trucks_Run' + str(num+1)):
        words = line.split()
        if words[0] == 'Heavy':
            print 'Heavy - ', words[2], 'Small - ', words[5]
        for x in range(Num_planes):
            if (words[0] == 'Plane' and words[1] == str(x+1)):
                #print words
                if (words[3] == 'POWER' and words[4] == 'done'):
                    Planes[x]['POWER'] = words[6]
                if (words[3] == 'POWER' and words[4] == 'finished'):
                    Planes[x]['Power_time'] = words[7]
                if (words[3] == 'BAGGAGE' and words[4] == 'done'):
                    Planes[x]['BAGGAGE'] = words[6]
                if (words[3] == 'BAGGAGE' and words[4] == 'finished'):
                    Planes[x]['Bag_time'] = words[7]
                if (words[3] == 'FUEL' and words[4] == 'done'):
                    Planes[x]['FUEL'] = words[6]
                if (words[3] == 'CLEAN' and words[4] == 'done'):
                    Planes[x]['CLEAN'] = words[6]
                if (words[3] == 'landing'):
                    Planes[x]['LANDING'] = words[5]
                if (words[2] == 'requesting' and words[4] == 'gate'):
                    Planes[x]['Arrival'] = words[6]
                if (words[3] == 'CATER' and words[4] == 'done'):
                    Planes[x]['CATER'] = words[6]
                if (words[3] == 'departing'):
                    Planes[x]['Depart'] = words[5]
                if (words[3] =='WATER' and words[4]):
                    Planes[x]['WATER'] = words[6]
                if words[3] =='late':
                    Planes[x]['Late'] = words[5]
                    #print 'Plane ' + str(x+1) + ' is late by ', Planes[x]['Late']
                    #print ' '
                if words[3] == 'early' or words[3] == 'on':
                    Planes[x]['Late'] = 0
    #print Planes[x], x
    Arrival=[0]*Num_planes
    Depart = [0]*Num_planes
    Difference = [0]*Num_planes
    Late = [0]*Num_planes
    Bag_times = [0]*Num_planes
    Power_times = [0]*Num_planes
#print Planes[1]
    for x in range(Num_planes):
        #print x
        Arrival[x] = float(Planes[x]['Arrival'])
        Depart[x] = float(Planes[x]['Depart'])
        Difference[x] = Depart[x] - Arrival[x]
        Late[x] = float(Planes[x]['Late'])
        Bag_times[x] = float(Planes[x]['Bag_time'])
        Power_times[x] = float(Planes[x]['Power_time'])
    avg_time = sum(Difference)/Num_planes
    total_bag_time = sum(Bag_times)
    average_bag_time = sum(Bag_times)/len(Bag_times)
    total_power_time = sum(Power_times)
    Late = [x for x in Late if x != 0]
#print 'Late', Late
    if len(Late) == 0:
        avg_delay = 0
    else:
        avg_delay = sum(Late)/len(Late)
    num_late = len(Late)
    print 'Number of trucks', num_trucks
    print 'Run number', (num +1)
    print 'Average time', avg_time
    print 'Average delay', avg_delay
    print 'Late_planes', num_late
    print 'Bag idle time', num_trucks*16*60 - total_bag_time
    print 'Power idle time', num_trucks*16*60 - total_power_time
    print ' '

#print 'Arrival', Arrival#, 'Departure', Depart, 'Time between arrival and departure', Difference
    pickle.dump((Planes,avg_time,avg_delay,num_late), open('Data Outputs/Run'+str(num+1) + '.pkl', 'wb'))