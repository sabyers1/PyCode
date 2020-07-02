# Interview question for determining the minimum number of additional routes an
# airline would need to add to allow travelers to access any point in the network.
# from the starting point.  Inputs involve airports, routes, and starting point.

airports = ["BGI","CDG","DEL","DOH","DSM","EWR","EYW","HND","ICN",
    "JFK","LGA", "LHR", "ORD","SAN","SFO","SIN","TLV","BUD"]

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
#count number of u such that who[u]==u and deg[u]==0 and u==who[S]
 
const int mxN = 1e5;
vector<int> adj[mxN], reverseAdj[mxN], st; #a stack 
int who[mxN], deg[mxN];
Bool visited[mxN], vis2[mxN];

void dfs1(int u){
    vis[u] = True
    for (int v : adj[u])
        if(!visited[v])
            dfs1(v);
    st.push_back(u);
}

void dfs2(int u, int rep){
    vis2[u] = True
    who[u] = rep
    for (int v : reverseAdj[u]) # why using reverse wasn't clear but it's part of Korasaju's algo
        if(!vis[v])
            dfs2(v,rep)
}

 int solve (vector<string> airports, vector<vector<string>> routes, string startingAirport){
     int n=airports.size();
     map<string,int> mp; #could be an unordered map for less complexity
     # O(n)
     for(int i=0; i<n; i++){
         mp[airports[i]]=i;
     }
    # O(m)
     for(vector<string> edge: routes){
         adj[mp[e[0]]].push_back(mp[e[1]]);  # store the id in the adjacency list
     }

    #O(n+m)
    for(int i=0; i<n; i++){
        for(int j : adj[i])
            reverseAdj[j].push_back(i)
    #O(n+m)
    for(int i=0; i<n; i++)
        if(!visited[i])
            dfs1(1);
    }

    #O(n+m)
    while(st.size()>0){
        int u=st.top();
        st.pop();
        if(!vis2[u])
            dfs2(u)
    }
    #O(n+m)
    for(int i=0; i<n; i++)
        for (int j : adj[i])
            if(who[i]!=who[j])
                ++deg[who[j]];

    #O(n)
    int ans=0;
    for(inti=0; i<n; i++){ #interating through original graph, but only want to  iter in compressed graph
        if(who[i]==i&&deg[i]==0&&i==who[mp[startingAirport]])
            ans++
    }
    return ans;

 }
