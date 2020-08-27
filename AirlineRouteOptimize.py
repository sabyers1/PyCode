# Interview question for determining the minimum number of additional routes an
# airline would need to add to allow travelers to access any point in the network.
# from the starting point.  Inputs involve airports, routes, and starting point.

airports = ["BGI","CDG","DEL","DOH","DSM","EWR","EYW","HND","ICN",
    "JFK","LGA", "LHR", "ORD","SAN","SFO","SIN","TLV","BUD"]

#mp = {0:"BGI",1:"CDG",2:"DEL",3:"DOH",4:"DSM",5:"EWR",6:"EYW",7:"HND",8:"ICN",
#    9:"JFK",10:"LGA", 11:"LHR", 12:"ORD",13:"SAN",14:"SFO",15:"SIN",16:"TLV",17:"BUD"}

routes = [ # existing one-way routes from departure to arrival
    ["DSM","ORD"],
    ["ORD","BGI"],
    ["BGI","LGA"],
    ["SIN","CDG"],
    ["CDG","SIN"],
    ["CDG","BUD"],
    ["DEL","DOH"],
    ["DEL","CDG"],
    ["TLV","DEL"],
    ["EWR","HND"],
    ["HND","ICN"],
    ["ICN","JFK"],
    ["EYW","LHR"],
    ["LHR","SFO"],
    ["SFO","SAN"],
    ["SFO","DSM"],
    ["SAN","EYW"]
]

startingAirport = "LGA"

# process input
# got through list of airports, assign each string an id
# map<string,int> mp
# vector<int> adj[n];  adjacency list
# go through the routes
# find stronlgly connected components via 
# Korasaju's algorithm O(n+m)
# who(u) determines arbitrary node within a strongly connected component to represent the
# the node.
# compress the interconnected graph based on components
# vector <int> adj2[n]:
# calculate the degree[n] of each node
# who[u] == u
# for edge (u,v) if who[u]!=who[v] adj2[who[u]].push_back(who[v]):
# for edge (u,v) if who[u]!=who[v]: ++deg(who[v]):

#find number of ndegree=0 which are not S (start point) in compressed graph
#count number of u such that who[u]==u and deg[u]==0 and u!=who[S]
 
mxN = 100000
adj=[[] for i in range(mxN)]
reverseAdj=[[] for i in range(mxN)]
st = [] # stack
who=[0 for i in range(mxN)]
deg=[0 for i in range(mxN)]
vis=[False for i in range(mxN)]
vis2=[False for i in range(mxN)]

def dfs1(u): # Depth First Search 1
    vis[u] = True
    print("Visit1: [{:2}] at {}".format(u,airports[u]))
    for v in adj[u]:
        if not vis[v]:
            dfs1(v)
    st.append(u)

def dfs2(u, rep): # Depth First Search 2
    vis2[u] = True
    who[u] = rep
    print("Visit2: [{:2}] at {} Rep by: [{:2}]".format(u,airports[u],rep))
    for v in reverseAdj[u]: # why using reverse wasn't clear but it's part of Korasaju's algo
        if not vis2[v]:
            dfs2(v,rep)

def solve (airports, routes, startingAirport):
    n=len(airports)
    mp = {}
    for i in range(n):
        mp.update({airports[i] : i})
        print("{} idx: [{:2}]".format(airports[i],i))

    # O(m)
    for e in routes:
        print("{} {:2} adj to {} {:2}".format(e[0],mp[e[0]],e[1],mp[e[1]]))
        #adj[mp[e[0]]].append(mp[e[1]]) # store the id in the adjacency list
        adj[mp[e[0]]].insert(0,mp[e[1]]) # store the id in the adjacency list

    #O(n+m)
    for i in range(n):
        for j in adj[i]:
            #reverseAdj[j].append(i)
            reverseAdj[j].insert(0,i)
            print("R {} from {}".format(routes[i][1],routes[i][0]))
    #print(reverseAdj)

    #O(n+m)
    for i in range(n):
        if not vis[i]:
            dfs1(i)

    #O(n+m)
    while len(st)>0:
        u=st.pop()
        if not vis2[u]:
            dfs2(u,u)

    #O(n+m)
    for i in range(n):
        for j in adj[i]:
            if who[i]!=who[j]:
                deg[who[j]]+= 1
                print("[{:2}] has degree: {}".format(who[j],deg[who[j]]))

    #O(n)
    ans=0
    for i in range(n): #interating through original graph, but only want to  iter in compressed graph
        if who[i]==i and deg[i]==0 and i!=who[mp[startingAirport]]:
            ans += 1
            print("Zero degree at: [{:2}] add route to [{:2}]".format(i,airports[i]))
            routes.append([startingAirport,airports[i]])
    return ans


if __name__ == "__main__":
    ans = solve(airports,routes,startingAirport)
    print("The number of additional routes needed to access all airports is: {}".format(ans))


    # Visualize the airport network
    # libraries
    import pandas as pd 
    import numpy as np 
    import networkx as nx 
    import matplotlib.pyplot as plt

    # Build directed graph via edge connections
    H = nx.DiGraph()
    for e in routes:
        H.add_edge(e[0],e[1])

    # Plot it
    pos = nx.spring_layout(H,k=0.3,iterations=30)
    plt.figure(1,figsize=(8,10))
    nx.draw(H,pos=pos,with_labels=True)
    #plt.savefig("AirlineRouteOpt.png")    
    plt.suptitle('Airline Routes', fontsize=16)
    plt.show()
