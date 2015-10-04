#!/usr/bin/env python

# controllers for MVC/API

import sys
import copy
import json
import time

from urllib2 import *

def defineShortestPath(startingPoint=None, destinationList=None):
    #print "startingPoint: {0},\tdestinationList: {1}".format(startingPoint, destinationList)
    print "Length of destinationList: {0}".format(len(destinationList))
    counter=0
    distanceFromPointList=[]
    for line in destinationList:
        if line['firstName'] == startingPoint or line['secondName'] == startingPoint:
            counter +=1
            distanceFromPointList.append(line['distance']['value'])
    print min(distanceFromPointList)
    print "Length of counter: {0}".format(counter)
    
    
def cleanString(spacedString):
    return spacedString.replace(" ","+")


def setDestinations(destlist, request):
    distanceList=[]
    foobar = destlist
    destlist=[]
    counter=0
    selectedList = request.session.get('selectedList')

    while counter < len(foobar):
        print "selectedList[{0}]['name']: {1}".format(counter, selectedList[counter]['name'])
#        for name in selectedList['name']:
        dic=foobar[counter]['location']

        state=dic['state_code']
        street=cleanString(dic['address'][0])
        city=cleanString(dic['city'])
        destlist.insert(counter,{'city':city, 'street':street, 'state':state, 'name': selectedList[counter]['name']})
        counter+=1
    dunno=(getDistances(destlist, distanceList))
    return dunno

def getDistances(destlist, distanceList):

    ### Improvement:
    ### go back to old-improvement way, but do math correctly this time! ={ =P
    counter = len(destlist) - 1
#    print len(destlist)
    while counter > 0:
        cleanDict = {}
        firstCity=destlist[counter]['city']
        firstStreet=destlist[counter]['street']
        firstState=destlist[counter]['state']
        firstName=destlist[counter]['name']
        secondCity=destlist[0]['city']
        secondState=destlist[0]['state']
        secondStreet=destlist[0]['street']
        secondName=destlist[0]['name']
        BASE_URL= "https://maps.googleapis.com/maps/api/directions/json?origin={0},+{1},+{2}&destination={3},+{4},+{5}&mode=driving".format(firstStreet,firstCity,firstState,secondStreet,secondCity,secondState)    
        request = Request(BASE_URL)
        time.sleep(1)
        print "QUERYING GOOGLE! =)"
        response = urlopen(request)
        js = json.loads(response.read())
        cleanDict['firstCity'] = firstCity
        cleanDict['firstState'] = firstState
        cleanDict['firstStreet'] = firstStreet
        cleanDict['firstName'] = firstName
        cleanDict['secondState']=secondState
        cleanDict['secondCity']=secondCity
        cleanDict['secondStreet']=secondState
        cleanDict['secondName'] = secondName
        cleanDict['distance']=js['routes'][0]['legs'][0]['duration']
        distanceList.append(cleanDict)
        #print len(distanceList)
        counter -= 1
    if len(destlist) != 2:
        del destlist[0]
        return getDistances(destlist, distanceList)
    else:

        return distanceList


inp=[
     {'city':'san+francisco', 'state':'CA','street':'100+spear+st'},
     {'city':'san+francisco', 'state':'CA','street':'1+embarcadero'},
     {'city':'el+cerrito', 'state':'CA','street':'11565+San+Pablo+Ave'},
     {'city':cleanString('Santa Rosa'), 'state':'CA','street':cleanString('2525 Gardner Ave')},
     {'city':cleanString('Santa Rosa'), 'state':'CA','street':cleanString('1670 Mendocino Ave')},
     {'city':cleanString('Reno'), 'state':'NV','street':cleanString('1855 E Peckham')},
     {'city':cleanString('Somerville'), 'state':'MA','street':cleanString('180 Somerville Ave')},
 ]


if __name__ == '__main__':
    distanceList = []
    getDistances(inp, distanceList)
    