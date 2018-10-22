import collections
import math



class Graph:
  def __init__(self):
    self.vertices = set()

    # makes the default datatype of the values as a list

    self.edges = collections.defaultdict(list)
    self.weights = {}
    self.cordinates = collections.defaultdict(list)

  def add_vertex(self, value, cordinates):
    self.vertices.add(value)
    self.cordinates[value] = cordinates

  def add_edge(self, from_vertex, to_vertex):
    if from_vertex == to_vertex: 
      pass 
    
    distance  = self.calc_distance(from_vertex, to_vertex)

    self.edges[from_vertex].append(to_vertex)
    self.weights[(from_vertex, to_vertex)] = distance


## same as calc distance. however heuristic will be called with goal vertex as the to_vertex
## so the heuristic function for each node is basically the eucleadian distance of that node from the goal

  def heuristic(self, from_vertex, to_vertex):
    x1 = self.cordinates[from_vertex][0]
    y1 = self.cordinates[from_vertex][1]
    x2 = self.cordinates[to_vertex][0]
    y2 = self.cordinates[to_vertex][1]

    dist = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))

    return dist

  ## calculates the distance between the two nodes
  def calc_distance(self, from_vertex, to_vertex):
    x1 = self.cordinates[from_vertex][0]
    y1 = self.cordinates[from_vertex][1]
    x2 = self.cordinates[to_vertex][0]
    y2 = self.cordinates[to_vertex][1]

    dist = math.sqrt(((x2-x1)**2) + ((y2-y1)**2))

    return dist


  ## funtion to override the default print function when printing graph.
  ## __str__() function is called when we do print(Graph)

  def __str__(self):
    string = "Vertices: " + str(self.vertices) + "\n"
    string += "Edges: " + str(self.edges) + "\n"
    string += "Edge Weights: " + str(self.weights)
    return string


def dijkstra(graph, start):

  # Set of visited nodes
  visited_nodes = set()

  ## creates 2 dictianaries where the keys are all the vertices from graph.vertices anf the values are set to the second parameter mentioned(infinity and None in this case)
  
  # this is the dictionary which holds the vertex(key) and the min diastance to that vertex(val)
  dij_graph = dict.fromkeys(list(graph.vertices), math.inf)
  
  #this dict holds the vertex(key) and the previous node(val) which resulted in the shotest path to that vertex
  previous = dict.fromkeys(list(graph.vertices), None)

  ## value of start node is now zero

  dij_graph[start] = 0

  
  ## Runs the while loop until visited_nodes has all the vertices

  while visited_nodes != graph.vertices:

    ## returns the vertex witht the min value
    v = min((set(dij_graph.keys()) - visited_nodes), key=dij_graph.get)

    # iterating through all the neighbors of the min vertex
    for neighbor in set(graph.edges[v]) - visited_nodes:
      new_dist = dij_graph[v] + graph.weights[v,neighbor]

      # is the new diatance lesser than the previous distance to that vertex 
      if new_dist < dij_graph[neighbor]:
        dij_graph[neighbor] = new_dist
        previous[neighbor] = v


    visited_nodes.add(v)

  return (dij_graph, previous)



## returns the shortest path from source to target

def a_star(graph, start, target):

  
  # keeps track of the actual distances tot hat nmode
  dij_graph, previous = dijkstra(graph, start)

  path = [start]

  frontier = graph.edges[start]

  target_found = False

  while not target_found:
    min_dist = math.inf
    min_node = None

    for node in frontier:
      a_dist = dij_graph[node] + graph.heuristic(node, target)

      if a_dist < min_dist:
        min_dist = a_dist
        min_node = node

    path.append(min_node)

    if min_node == target:
      target_found = True
      break

    frontier = graph.edges[min_node]


  return path



def shortest_path(graph, start, end):
  dij_graph, previous = dijkstra(graph, start)
  
  path = []
  vertex = end

  while vertex is not None:
    path.append(vertex)
    vertex = previous[vertex]

  path.reverse()
  return path


#Creating a Graph

G = Graph()
G.add_vertex('a',[10,10])
G.add_vertex('b',[15,10])
G.add_vertex('c',[15,15])
G.add_vertex('d',[10,20])
G.add_vertex('e',[13,25])
G.add_vertex('f',[20,13])
G.add_vertex('g',[0,13])


G.add_edge('a', 'b')
G.add_edge('a', 'c')
G.add_edge('b', 'c')
G.add_edge('a', 'd')
G.add_edge('d', 'e')
G.add_edge('c', 'e')
G.add_edge('b', 'f')
G.add_edge('f', 'c')
G.add_edge('a', 'g')
G.add_edge('g', 'd')

print('This is the GRAPH : \n')
print(G)
print('\nGiven below is the path between a and e calculated using Dijkstra\n') 
print(shortest_path(G, 'a', 'e'))
print('\nGiven below is the path between a and e calculated using A * \n')
print(a_star(G, 'a', 'e'))













