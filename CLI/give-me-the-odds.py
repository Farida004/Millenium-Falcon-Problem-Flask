from collections import defaultdict
  

''' This class represents a millennium falcon with a path (directed graph) '''
class Millennium_Falcon:
  
    def __init__(self,autonomy):
        self.map = defaultdict(list)
        self.num_of_days = {}
        self.autonomy = autonomy
        self.complete_paths = []
  
    ''' A Fucntion that adds a route to a path (edge to a graph)'''
    def addRoute(self, u, v, weight):
        self.map[u].append(v)
        self.num_of_days[(u, v)] = weight
  
    '''A recursive function that generates all paths from 'source planet' to 'destination planet'.
    visited[] keeps track of planets in current path.
    path[] stores actual planets. Complete paths stores all the possible paths found.'''
    def find_all_paths(self, departure, arrival, countdown, visited, path ):
 
        visited = set()
        path.append(departure)
        visited.add(departure)
        complete_paths=[]
 
        if departure == arrival :
            travel_time = self.getTime(path)
            if(travel_time <=countdown):
              self.complete_paths.append(path.copy())
        else:
            for i in self.map[departure]:
                if i not in visited:
                    self.find_all_paths(i, arrival, countdown, visited, path) 
        path.pop()

    ''' This function prints the calculated probability based on the paths found '''
    def print_all_paths(self, departure, arrival, countdown, bounty_hunters_info):
        visited =[]
        path = []
        probabilities = []
        self.find_all_paths(departure, arrival, countdown, visited, path)
        for i in self.complete_paths:
          probabilities.append(self.calculateProbability(i, bounty_hunters_info))
        if(len(probabilities)>=1):
          return max(probabilities)
        else:
          return 0

    ''' This function computes the total days spent on the flight from source to destination taking into account the fueling needs.'''
    def getTime(self,path):
      total_days = 0
      fuel_status = self.autonomy
      refuel_day = 1
      for i in range(0, len(path) - 1):
        next_hop_in_days = self.num_of_days[(path[i], path[i + 1])]
        if fuel_status < next_hop_in_days:
          total_days += next_hop_in_days + refuel_day
          fuel_status += 6 - next_hop_in_days
        else:
          total_days += next_hop_in_days
          fuel_status -= next_hop_in_days
      return total_days

    ''' This function calculates the probability based on the paths found and the schedule of bounting hunters '''
    def calculateProbability(self,path,bounty_hunters_info):
      probability = 0
      cnt_refuel_hunters = 0
      travel_plan = self.get_detailed_path_info(path)
      cnt = 0
      for i in range(0,len(bounty_hunters_info)):
          bh = bounty_hunters_info[i]
          cnt = path.count(bh['planet'])
          hunters = [item for item in travel_plan if item[0] == bh['planet'] and item[1]==bh['day']]
          if(len(hunters)==1):
            cnt_refuel_hunters+=1
      if(cnt_refuel_hunters>1):
        cnt+=1
      if (cnt == 1):
        probability+= 0.1
      elif(cnt > 1):
        probability = 0.1
        for i in range(1,cnt):
          probability+=((9**(cnt-1)/(10**cnt)))
      return int((1-probability)*100)

    ''' This function allows to get the detailed information of the flight. We see the planets we are going to visit and when.'''
    def get_detailed_path_info(self, path):
        travel_plan = []
        total_days = 0
        current_fuel = self.autonomy
        refuelling_day = 1

        if not path:
            return travel_plan

        for i in range(0, len(path) - 1):
            travel_plan.append((path[i], total_days))

            next_hop_in_days = self.num_of_days[(path[i], path[i + 1])]

            if current_fuel < next_hop_in_days:
                total_days += refuelling_day
                current_fuel += 6
                travel_plan.append((path[i], total_days))

            total_days += next_hop_in_days
            current_fuel -= next_hop_in_days
        travel_plan.append((path[-1], total_days))
        return travel_plan

from flask import Flask
import json
import sqlite3
import argparse

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('path1',type=str)
    parser.add_argument('path2',type=str)
    args = parser.parse_args()

    milleniumpath = args.path1
    empirepath= args.path2

    # Opening JSON file
    milleniumfalcon = open(milleniumpath)
    empire = open(empirepath)

    # returns JSON object as 
    # a dictionary
    mf_data = json.load(milleniumfalcon)
    e_data = json.load(empire)

    # creating file path
    dbfile = './examples/example1/universe.db'
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect(dbfile)

    # creating cursor
    cur = con.cursor()

    # MF data

    autonomy = mf_data['autonomy']
    departure = mf_data['departure']
    arrival = mf_data['arrival']

    #Empire data

    countdown = e_data['countdown']
    bounty_hunters_info = e_data['bounty_hunters']

    # Create a graph given in the above diagram
    mf = Millennium_Falcon(autonomy)

    #Universe db data
    cur.execute("SELECT * FROM routes")

    rows = cur.fetchall()

    for row in rows:
        mf.addRoute(*row)

    print(mf.print_all_paths(departure, arrival,countdown, bounty_hunters_info))

