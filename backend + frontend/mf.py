from collections import defaultdict
  
# This class represents a directed graph
# using adjacency list representation
class Millennium_Falcon:
  
    def __init__(self,autonomy):
        # default dictionary to store graph
        self.map = defaultdict(list)
        self.num_of_days = {}
        self.autonomy = autonomy
        self.complete_paths = []
  
    # function to add an edge to graph
    def addRoute(self, u, v, weight):
        self.map[u].append(v)
        self.num_of_days[(u, v)] = weight
  
    '''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''
    def find_all_paths(self, departure, arrival, countdown, visited, path ):
 
        # Mark the current node as visited and store in path
        visited = set()
        path.append(departure)
        visited.add(departure)
        complete_paths=[]
 
        # If current vertex is same as destination, then print
        # current path[]
        if departure == arrival :
            travel_time = self.getTime(path)
            if(travel_time> countdown):
              print((f"Time Exceeded"))
            else:
              print(f"Found path: {path}")
              self.complete_paths.append(path.copy())
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for i in self.map[departure]:
                if i not in visited:
                    self.find_all_paths(i, arrival, countdown, visited, path) 
        path.pop()
  
    # Prints all paths from 's' to 'd'
    def print_all_paths(self, departure, arrival, countdown, bounty_hunters_info):
        # Mark all the vertices as not visited
        visited =[]
        # Create an array to store paths
        path = []

        probabilities = []
        # Call the recursive helper function to print all paths
        self.find_all_paths(departure, arrival, countdown, visited, path)
        for i in self.complete_paths:
          probabilities.append(self.calculateProbability(i, bounty_hunters_info))
        if(len(probabilities)>=1):
          return max(probabilities)
        else:
          return 0

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
