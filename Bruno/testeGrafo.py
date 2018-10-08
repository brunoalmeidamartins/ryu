import networkx as nx
import matplotlib.pyplot as plt
'''
g=nx.DiGraph()

g.add_node(1)
g.add_node(2)
g.add_node(3)
g.add_node('A')
g.add_node('B')

g.add_edge(1,2)
g.add_edge(1,'A')
g.add_edge(2,3)
g.add_edge(3,'B')

#g.add_edges_from([()])

#print(nx.info(g))

print(list(g))
print(g.edges.data())

#nx.draw(g)

#plt.show()
'''
g= nx.MultiGraph()

g.add_edge('h1','s1->p1',cost=1,index=0)
g.add_edge('s1->p1','s1',cost=1,index=1)
g.add_edge('h2',1,cost=1,index=1)
g.add_edge(1,2,cost=1,index=2)
g.add_edge(2,3,cost=1,index=3)
g.add_edge('h3',3,cost=1,index=4)
g.add_edge('h4',3,cost=1,index=5)

path =[]
#Caminho h1->h3
path.append(nx.dijkstra_path(g,'h1','h3',weight='cost'))
#Caminho h3->h1
path.append(nx.dijkstra_path(g,'h3','h1',weight='cost'))

#Caminho h2->h3
path.append(nx.dijkstra_path(g,'h2','h3',weight='cost'))

#Caminho h4->h2
path.append(nx.dijkstra_path(g,'h4','h2',weight='cost'))

#Caminho h1->h2
path.append(nx.dijkstra_path(g,'h1','h2',weight='cost'))


for i in path:
    print(i)
