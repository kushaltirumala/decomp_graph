import argparse, pulp
import networkx as nx
import numpy as np
import random


def gen_graph(max_n, min_n, g_type='erdos_renyi', edge=4):
    # choose a random number of vertices in the graph between max_n and min_n
    cur_n = np.random.randint(max_n - min_n + 1) + min_n

    g = None

    # create the right corresponding type of graph
    if g_type == 'erdos_renyi':
        g = nx.erdos_renyi_graph(n=cur_n, p=0.15)
    elif g_type == 'powerlaw':
        g = nx.powerlaw_cluster_graph(n=cur_n, m=4, p=0.05)
    elif g_type == 'barabasi_albert':
        g = nx.barabasi_albert_graph(n=cur_n, m=edge)
    elif g_type == 'watts_strogatz':
        g = nx.watts_strogatz_graph(n=cur_n, k=cur_n // 10, p=0.1)

    # randomly give weights to the graph
    for edge in nx.edges(g):
        g[edge[0]][edge[1]]['weight'] = random.uniform(0, 1)

    return g


def getEdgeVar(v1, v2, vert):
    u1 = min(v1, v2)
    u2 = max(v1, v2)
    if not ((u1, u2) in vert):
        vert[(u1, u2)] = pulp.LpVariable('u%d_%d' % (u1, u2), 0, 1, pulp.LpInteger)

    return vert[(u1, u2)]


def getNodeVar(v, node):
    if not v in node:
        node[v] = pulp.LpVariable('v%d' % v, 0, 1, pulp.LpInteger)

    return node[v]


def createOpt(G):
    prob = pulp.LpProblem('MILP Maximum Cut', pulp.LpMinimize)
    edgeVar = {}
    nodeVar = {}
    obj = 0

    for j, (v1, v2) in enumerate(G.edges()):
        e12 = getEdgeVar(v1, v2, edgeVar)
        node1 = getNodeVar(v1, nodeVar)
        node2 = getNodeVar(v2, nodeVar)

        prob.addConstraint(e12 <= node1 + node2)
        prob.addConstraint(e12 <= 2 - node1 - node2)

        obj = obj + (G[v1][v2]['weight']) * e12

    prob.setObjective(-1 * obj)  # Note that this is LpMinimum
    return prob


def cmdLineParser():
    '''
    Command Line Parser.
    '''
    parser = argparse.ArgumentParser(description='Minimum Vertex Cover')
    parser.add_argument('-o', dest='outPrefix', type=str, action='store', default=None, help='Output Prefix')
    parser.add_argument('-g', dest='g_type', type=str, action='store', default='erdos_renyi', help='Graph type')
    parser.add_argument('-max_n', dest='max_n', type=int, action='store', default=700, help='max number of nodes')
    parser.add_argument('-min_n', dest='min_n', type=int, action='store', default=500, help='min number of nodes')
    return parser.parse_args()


def generateInstance(max_n, min_n, g_type, edge, outPrefix=None):
    G = gen_graph(max_n, min_n, g_type, edge)
    P = createOpt(G)

    if outPrefix != None:
        # Write out
        nx.write_gpickle(G, outPrefix.replace('lpfiles', 'gpickle') + '.gpickle')
        P.writeLP(outPrefix + '.lp')


def main():
    args = cmdLineParser()
    G = gen_graph(args.max_n, args.min_n, args.g_type)
    P = createOpt(G)

    if args.outPrefix != None:
        # Write out
        nx.write_gpickle(G, args.outPrefix + '.gpickle')
        P.writeLP(args.outPrefix + '.lp')


if __name__ == '__main__':
    main()

