#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin
        self.weight = 1     # inicialmente con peso 1

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)


class Airport:
    def __init__ (self, iden=None, name=None, index=None):
        self.code = iden
        self.name = name
        self.routeHash = dict()
        self.outweight = 0.0
        self.index = index

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

    def addIncomingEdge(self, incomingAirport):
        if not incomingAirport in self.routeHash:       # si la arista no esta en su lista ruta, lo anadimos
            e = Edge(incomingAirport)
            self.routeHash[incomingAirport] = e
        else:                                           # si esta en lista ruta, incrementamos el peso
            e = self.routeHash[incomingAirport]
            e.weight += 1

        airportHash[e.origin].outweight += 1



airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
PR = []

L = 0.85
diff = 10**(-10)     # diferencia aceptable entre P y Q

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
            a.index = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print("There were {0} Airports with IATA code".format(cont))


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            originCode = temp[2]
            destCode = temp[4]
            if destCode in airportHash and originCode in airportHash:
                # add edge for destination airport
                destAirport = airportHash[destCode]
                destAirport.addIncomingEdge(originCode)
            else:
                raise Exception('inexistent Airports')

        except Exception as inst:
            pass
        else:
            cont += 1
    routesTxt.close()
    print("There were {0} Edges with both IATA code".format(cont))


def conectarNodosDosEnDos(discAirp):        # conecta una lista de nodos dos a dos
    i = 0;
    while(i < len(discAirp)):
        discAirp[i].addIncomingEdge(discAirp[i+1].code)
        discAirp[i+1].addIncomingEdge(discAirp[i].code)
        i += 2



def computePageRanks():
    n = len(airportHash)
    P = [1/n]*n
    # Disconnected nodes PR calculation
    discAirp = (list(filter(lambda a: a.outweight == 0.0, airportList)))
    print(len(discAirp))


    if len(discAirp)%2 == 0:
        conectarNodosDosEnDos(discAirp)

    else:


        print(discAirp[0].index)
        discAirp[0].addIncomingEdge(discAirp[1].code)
        discAirp[1].addIncomingEdge(discAirp[2].code)
        discAirp[2].addIncomingEdge(discAirp[1].code)
        discAirp.remove(discAirp[0])
        discAirp.remove(discAirp[1])
        discAirp.remove(discAirp[2])
        conectarNodosDosEnDos(discAirp)


    stop = False
    it = 0
    while (not stop):
        Q = [0.0]*n
        for i in range(n):
            a = airportList[i]
            sumPR = 0
            for k,v in a.routeHash.items():
                sumPR += P[airportHash[k].index] * v.weight / airportHash[k].outweight
            Q[i] = L * sumPR + (1-L)/n 
        stop = checkDifference(diff, P, Q)
        P = Q

        print("sum PR (iter", it, "):" , sum(i for i in P))    # print sum of P
        it += 1

    global PR
    PR = P.copy()

    return it

def checkDifference(diff, P, Q):
    
    for x, y in zip(P,Q):
        if (abs(x-y) > diff):
            return False
    return True

def outputPageRanks():
    L = []
    i = 0
    for k in airportHash:
        a = airportHash[k]
        x = (a.name, PR[i])
        L.append(x)
        i += 1
    L.sort(key = lambda x: x[1], reverse = True)

    s = ""
    s += " (Airport_Name, Location : PageRank) \n"
    for (x,y) in L:
        s += ("(%s : %s)\n"%(x, y))

    f = open("output.txt", "w")
    f.write(s)
    f.close()



def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("# Iterations:", iterations, ", with", diff, "Difference between iterations")
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())