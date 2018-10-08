import networkx as nx
g = nx.Graph
g.add_edge('a',1,coast=1,index=0)
g.add_edge(1,2,coast=1,index=0)
g.add_edge(2,3,coast=1,index=0)
g.add_edge(3,'b',coast=1,index=0)
print(nx.dijkstra_path(g,'a','b'))
