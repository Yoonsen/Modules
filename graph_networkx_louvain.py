import pandas as pd
import numpy as np
import requests
import json
import community
import networkx as nx
from networkx.algorithms.community import k_clique_communities
import seaborn as sns

from collections import Counter

from matplotlib import colors as mcolors


colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

from IPython.display import HTML
import sqlite3


from pylab import rcParams

rcParams['figure.figsize'] = 15, 10




import matplotlib.pyplot as plt


def make_graph_corp(word, corpus='eng'):
    result = requests.get("http://www.nb.no/sp_tjenester/beta/ngram_1/galaxies/query?terms={word}&lang=all&corpus={corpus}".
                          format(word=word, corpus=corpus))
    G = nx.DiGraph()
    edgelist = []
    if result.status_code == 200:
        graph = json.loads(result.text)
        #print(graph)
        nodes = graph['nodes']
        edges = graph['links']
        for edge in edges:
            edgelist += [(nodes[edge['source']]['name'], nodes[edge['target']]['name'], abs(edge['value']))]
    #print(edgelist)
    G.add_weighted_edges_from(edgelist)
    return G

def make_graph(word):
    result = requests.get("http://www.nb.no/sp_tjenester/beta/ngram_1/galaxies/query?terms={word}".format(word=word))
    G = nx.DiGraph()
    edgelist = []
    if result.status_code == 200:
        graph = json.loads(result.text)
        #print(graph)
        nodes = graph['nodes']
        edges = graph['links']
        for edge in edges:
            edgelist += [(nodes[edge['source']]['name'], nodes[edge['target']]['name'], abs(edge['value']))]
    #print(edgelist)
    G.add_weighted_edges_from(edgelist)
    return G



def draw_graph(G, nodelist=[], h=15, v=10, fontsize=12, layout=nx.spring_layout,
               arrows=False, node_color='orange', node_size=100, font_color='black'): 
    from pylab import rcParams
    import matplotlib.pyplot as plt
    
    if nodelist != []:
        G = G.subgraph(nodelist)
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v
    pos = layout(G)
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    nx.draw_networkx_labels(G, pos, font_size=fontsize, font_color=font_color)
    nx.draw_networkx_nodes(G, pos, alpha=0.1, node_color=node_color, node_size=node_size )
    nx.draw_networkx_edges(G, pos, alpha=0.7, arrows=arrows, edge_color='lightblue')

    rcParams['figure.figsize'] = x, y


def draw_graph_centrality(G,  h=15, v=10, deltax=0, deltay=0, fontsize=18, k=0.2, arrows=False, node_alpha=0.3, l_alpha=1, node_color='blue', centrality=nx.degree_centrality, font_color='black', threshold=0.01, multi=3000): 
    from pylab import rcParams
    import matplotlib.pyplot as plt
    
    node_dict = centrality(G)
    subnodes = dict({x:node_dict[x] for x in node_dict if node_dict[x] >= threshold})
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v
    
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    G = G.subgraph(subnodes)
    pos = nx.spring_layout(G, k=k)
    labelpos = dict({k:(pos[k][0]+ deltax, pos[k][1] + deltay) for k in pos })
    #print(labelpos)
    #print(pos)
    if l_alpha <= 1:
        nx.draw_networkx_labels(G, labelpos, font_size=fontsize, alpha = l_alpha, font_color = font_color)
    nx.draw_networkx_nodes(G, pos, alpha=node_alpha, node_color=range(len(subnodes.keys())), cmap=plt.cm.Blues, nodelist=subnodes.keys(), node_size=[v * multi for v in subnodes.values()])
    nx.draw_networkx_edges(G, pos, alpha=0.4, arrows=arrows, edge_color='lightblue')

    rcParams['figure.figsize'] = x, y
    


def draw_graph_centrality2(G, Subsets=[],  h=15, v=10, deltax=0, deltay=0, fontsize=18, k=0.2, arrows=False, 
                           node_alpha=0.3, l_alpha=1, node_color='blue', centrality=nx.degree_centrality, 
                           font_color='black', 
                           threshold=0.01, 
                           multi=3000,
                          edge_color='olive',
                          colstart=0.2,
                          coldark=0.5):
    
    from pylab import rcParams
    import matplotlib.pyplot as plt
    from matplotlib import colors as mcolors


    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
    node_dict = centrality(G)
    subnodes = dict({x:node_dict[x] for x in node_dict if node_dict[x] >= threshold})
    x, y = rcParams['figure.figsize']
    rcParams['figure.figsize'] = h, v
    
    ax = plt.subplot()
    ax.set_xticks([])
    ax.set_yticks([])
    G = G.subgraph(subnodes)
    glob_col = sns.hls_palette(len(G), h=colstart, l=coldark)[0]
    pos = nx.spring_layout(G, k=k)
    labelpos = dict({k:(pos[k][0]+ deltax, pos[k][1] + deltay) for k in pos })
    #print(labelpos)
    #print(pos)
    if l_alpha <= 1:
        nx.draw_networkx_labels(G, labelpos, font_size=fontsize, alpha = l_alpha, font_color = font_color)
    sub_color = 0
    if Subsets != []:
        i = 0
        colpalette = sns.hls_palette(len(Subsets), h=colstart, l=coldark)
        #print(colpalette)
        for Sub in Subsets:
            sublist = dict({x:subnodes[x] for x in subnodes if x in Sub})
            #print(sublist)
            #sub_col = list(colors.values())[np.random.randint(20,100)]
            sub_col= colpalette[i]
            #print(i, sub_col, sublist.keys())
            nx.draw_networkx_nodes(G, pos, alpha=node_alpha, node_color=sub_col ,  nodelist=sublist.keys(), node_size=[v * multi for v in sublist.values()])
            i += 1
    else:
        nx.draw_networkx_nodes(G, pos, alpha=node_alpha, node_color= glob_col,  nodelist=subnodes.keys(), node_size=[v * multi for v in subnodes.values()])
        True
        
    nx.draw_networkx_edges(G, pos, alpha=0.1, arrows=arrows, edge_color=edge_color)

    rcParams['figure.figsize'] = x, y



# Set palette using: sns.hls_palette(10, h=.6, l=.1)


def sentrale(Graph, top = 20):
    #mc = Counter([('ord',0)])
    #SubGraph = nx.Graph()
    #SubGraph.add_edges_from([(x,y) for (x,y) in Graph.edges() if Graph.degree(x)>1 and Graph.degree(y)>1])
    #if Graph.__len__() > 0:
    mc = Counter(nx.closeness_centrality(Graph)).most_common(top)
    return mc 




def mcommunity(Graph):

    G = Graph.to_undirected()

    m_partition = community.best_partition(G)
    #print(m_partition)
    list_nodes = []
    for com in set(m_partition.values()) :
        list_nodes += [set([nodes for nodes in m_partition.keys()
                                    if m_partition[nodes] == com])]
    return list_nodes



def kcliques(agraph):
    i=3
    x = list(k_clique_communities(agraph,i))
    comms = dict()
    while x != list():
        #print(x)
        j = 1
        for el in x:
            comms[(i,j)] = el
            j += 1
        i += 1
        x = list(k_clique_communities(agraph,i))
    return comms


def subsetgraph(comms, centrals, labels=2):
    """comms is communities """
    subgraph = nx.DiGraph()
    comkeys = sorted(comms.keys(), key=lambda x: x[0],reverse=True)
    for i in range(len(comkeys)):
        top = comkeys[i]
        label_small = str(top[0])+str(top[1])
        small_ordered = Counter({r:centrals[r] for r in comms[top]}).most_common(labels)
        label_small = label_small +' '+ ' '.join([x[0] for x in small_ordered])
        subgraph.add_node(label_small)
        j = i + 1
        found = False
        while j < len(comkeys) and not(found):
            nodej = comms[comkeys[j]]
        
            found = comms[top].issubset(nodej)
            #print(top,comkeys[j], found)
            if found:
                label_large = str(comkeys[j][0])+str(comkeys[j][1])
                large_ordered = Counter({r:centrals[r] for r in nodej}).most_common(labels)
                label_large = label_large +' '+ ' '.join([x[0] for x in large_ordered])
                #print(label_small, label_large)
                subgraph.add_edge(label_small, label_large)
            j += 1
    return subgraph



def make_cliques(words, lable_num = 2):
    ggg = make_graph(words).to_undirected()
    centrals = nx.closeness_centrality(ggg)
    coms = kcliques(ggg)
    sg = subsetgraph(coms, centrals, lable_num)
    return (ggg, coms, sg)


def make_w_graph(weight_matrix):
    """weight_matrix a list on the form [((x,y,weight), ...]"""
    
    G = nx.Graph()
    G.add_weighted_edges_from(weight_matrix)
    return G

def make_cliques_from_graph(G, lable_num = 2):
    ggg = G
    centrals = nx.closeness_centrality(ggg)
    coms = kcliques(ggg)
    sg = subsetgraph(coms, centrals, lable_num)
    return (ggg, coms, sg)



def draw_tree(G, node_size=1, node_color='slategrey', n=5, m=1):
    ax = plt.subplot()
    draw_graph(G, h= 5, v=8, layout= lambda g: tree_positions(g, n, increment=m), node_color=node_color, node_size=node_size, fontsize=18,arrows=False)
    fmin, fmax = plt.xlim()
    plt.xlim(fmin-10,fmax+10)
    ax.set_xticks([])
    ax.set_yticks([])
    #plt.savefig('krig.svg')



def my_layout(G):
    """For grafer fra make_cliques der koden ligger i de to første tallene"""
    pos = dict()
    for i in G.nodes():
        x = i.split()[0]
        pos[i] = (int(x[0]), int(x[1]))
    return pos

def tree_layout(G):
    """For grafer fra make_cliques der koden ligger i de to første tallene"""
    pos = dict()
    roots = root_nodes(G)
    for r in G.nodes():
        x = i.split()[0]
        pos[i] = (int(x[0]), int(x[1]))
    return pos

def root_nodes(G):
    res = []
    for x in G.nodes():
        found = False
        for y in G.nodes():
            found = found or (x,y) in G.edges()
            if found:
                break;
        if not found:
            res += [x]
    return res

def tree_positions(Tree, spacing, increment=1):
    root = root_nodes(Tree)[0]
    return tree_pos(root, Tree, 1, spacing, 3,1, level_increment=increment)[0]

def tree_pos(x, G, level, spacing, num, left_edge, level_increment = 1):
    """Draw from left to right for left_edge"""
    import numpy as np
    
    positions = dict()
    daughters = [y for (y,z) in G.edges() if x==z]
    if daughters == []:
        positions[x] = (left_edge, level )
        d_left = left_edge
    else: 
        i = 1
        d_left = left_edge
        vals = []
        d_level =  level + level_increment
        for d in daughters:
            d_positions, d_width = tree_pos(d, G, d_level - np.random.randint(1,5)*level_increment/10, spacing, i, d_left, level_increment=level_increment)
            i += 1
            d_left += spacing + d_width 
            positions.update(d_positions)
            vals += [d_positions[d][0]]
            #print(vals)
        averagex = np.mean(vals)    
        positions[x] = (averagex, level)
    return positions, d_left

def forest(G):
    roots = root_nodes(G)
    g_forest = []
    for r in roots:
        nr = node_set(r, G)
        g_forest += [G.subgraph(nr)]
    return g_forest

def node_set(root, G):
    span = [root]
    daughters = [y for (y,z) in G.edges() if z == root]
    if daughters != []:
        for d in daughters:
            span += node_set(d, G)
    return span

        
    
def draw_forest(F, spacing, save_name=False):
    import matplotlib.pyplot as plt
    
    rows = len(F)
    row = 1
    for tree in F:
        #print(tree.nodes())
        #plt.subplot(rows,row,1)
        plt.figure(row)
        row += 1
        draw_tree(tree, node_size=0.5)
        if save_name:
            plt.savefig('{name}-{row}.png'.format(name=save_name, row=row, dpi=300))



def print_list_of_sets(los):
    for x in los:
        print(', '.join(x),'\n')

def print_sets(graph):
    for x in graph[1]:
        print(x, ', '.join(graph[1][x]),'\n')
    return True

