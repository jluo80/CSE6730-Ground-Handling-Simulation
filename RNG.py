import time
import math
from datetime import datetime
class ClassRanGen(object):
    def __init__(self):
##        seedpool=[1,1086380712,733801345,303537024,887865146,449835042,775074867,1279134555,694937072,1073050889]
# seedpool from 10 # away from each 1 million iteration for independent randomability.
##        self.seed=seedpool[int(math.ceil(100*time.time())%10)]
        self.systime=datetime.now().microsecond
        #print("systime=",self.systime)
        self.seed=(math.ceil(self.systime))
        #print("sysseed=",self.seed)
# call system time for random seed decision.
        self.a=16807
        self.c=0
        self.m=2147483647
        #print("seed_init=",self.seed)
    def Rand(self):
        #print("system time=",self.seed)
        self.seed=(self.a*int(self.seed)+self.c)%self.m
        #print("seed_updated=",self.seed)
        RanNo=round(float(self.seed)/float(self.m),5)
        if (self.seed==1):
            print("loop back!!!!!","seed=",self.seed)
        else:
            pass
        # deal with overflow for compatible 32 bit int
        if (self.seed>self.m):
            self.seed=1
            print("WARNING: out of upper bound!!")
            print("seed=",self.seed)
        else:
            pass
        # deal with underflow for positive requirement
        if (self.seed<=0):
            #print("self.seed=",self.seed)
            self.seed=1
            print("WARNING: out of lower bound!!")
        else:
            pass
        #print("updatedSeed=",self.seed)
        print("Rand_Number=",RanNo)
        return RanNo

a = ClassRanGen()
a.Rand()