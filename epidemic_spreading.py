
"""
Name: Dynamics on Complex Networks
Author: Pablo Eliseo Reynoso Aguirre
Date: MaY 25, 2017
Desrcription:

 Monte Carlo sampling method is technique for performing simulations of an epidemic spreading dynamics in complex networks.
 This technique implements the SIS model in which each node represents an individual which can be:

    a) Susceptible (S): healthy but susceptible to contagious.
    b) Infected (I): already infected and possible vector of transmission.

 The task relies in performing the:
    i) Calculation of the fraction of infected nodes (p), in the stationay state,
       as a function of the infection probability of the disease beta (at least 51 values, delta_beta=0.02),
       for different values of the recovery probability mu (e.g. 0.1, 0.5, 0.9).
    ii) Try different networks (e.g. Erdos-Renyi, scale-free, real), different sizes (at least 500 nodes),
    average degrees, exponents, etc. Do not make all the combinations, about 10 plots p(beta) are enough.


"""

import networkx as nx;
import matplotlib.pyplot as plt;
import numpy as np;
import time as tme;



#Complex Networks Tools
class NetworkTools():

    def reading_networks(self, net_path):

        folder = "networks/";
        G = nx.read_pajek(folder+net_path)
        G_is_directed = nx.is_directed(G)

        if G_is_directed:
            G = nx.DiGraph(G)
        else:
            G = nx.Graph(G)

        return G

    def convert_net_to_dict(self, network):

        graph = {}
        for node in network.nodes():
            attributes = {'neighbors': network.neighbors(node),'state':'None'}
            graph[node] = attributes
        print(graph.keys());
        return graph

    def display_network(self, network):
        nx.draw(network);
        plt.show();


#Suceptible-Infected-Suceptible Model
class SIS(object):

    def __init__(self, network, mu, beta, p0):

        self.network = network
        self.mu = mu
        self.beta = beta
        self.p0 = p0
        self.N = len(network)
        self.initialize()

    def initialize(self):

        self.nodes_infected = []
        self.nodes_susceptible = []

        for node in self.network:
            if np.random.random() < self.p0:
                self.network[node]['state'] = 'I'
                self.nodes_infected.append(node)
            else:
                self.network[node]['state'] = 'S'
                self.nodes_susceptible.append(node)

    def forward_infections(self):

        forward_infected = []
        forward_susceptible = []

        for node_i in self.nodes_infected:
            if np.random.random() < self.mu:
                forward_susceptible.append(node_i)
            else:
                forward_infected.append(node_i)

        for node_s in self.nodes_susceptible:
            node_s_neighbors = self.network[node_s]['neighbors']
            i = 0
            infected = False
            while i < len(node_s_neighbors):
                if self.network[node_s_neighbors[i]]['state'] == 'I':
                    infected = np.random.random() < self.beta
                    if infected == True: break
                i += 1

            if infected:
                forward_infected.append(node_s)
            else:
                forward_susceptible.append(node_s)

        for node_i in forward_infected:
            self.network[node_i]['state'] = 'I'

        for node_s in forward_susceptible:
            self.network[node_s]['state'] = 'S'

        self.nodes_infected = forward_infected
        self.nodes_susceptible = forward_susceptible

        infection_frac = float(len(self.nodes_infected)) / self.N

        return infection_frac


# MonteCarlo simulation
def MonteCarloMethod(model, n_rep, t_max, t_trans):

    p_final = 0
    for i in range(n_rep):
        p_simulation = []
        for j in range(t_max):
            p = model.forward_infections()
            p_simulation.append(p)

        stationary_p = p_simulation[t_trans:]
        mean_p = sum(stationary_p)/len(stationary_p)
        p_final += mean_p
        model.initialize()

    p_final = p_final/n_rep

    return p_final







# parameters for SIS model
beta_s = [0.01*i for i in range(0,102,2)];
mu_s = [0.1, 0.5, 0.9]

# extra parameters for Monte Carlo simulation
n_rep = 60
p0 = 0.2
t_max = 1200
t_trans = 1100


#Epidemic Spreading Simulation

proposed_networks = ["SF_1000_g2.5.net","ER1000k8.net","airports_UW.net","GWO_CN_1496831142.net"];
networks_graphs = [];
networks_dictionaries = [];

NT = NetworkTools();

for i in range(len(proposed_networks)):
    networks_graphs.append(NT.reading_networks(proposed_networks[i]));
    networks_dictionaries.append(NT.convert_net_to_dict(networks_graphs[i]));


i = 0


network_types = ['SF(N=1000, gamma=2.5)', 'ER(N=1000, <K>=8)', 'Real(N=3618)']
for net in networks_dictionaries:

    print('Network type:', network_types[i])
    for mu in mu_s:

        p_sequence = []
        print(' mu:', mu)
        for beta in beta_s:

            print('  beta:', beta)
            start_time = tme.time()
            init_model = SIS(net, mu, beta, p0)
            p = MonteCarloMethod(init_model, n_rep, t_max, t_trans)
            end_time = tme.time()
            p_sequence.append(p)
            print('   p: %.2f' % p)
            print('   time: %.2f s' % (end_time-start_time))

        plt.plot(beta_s, p_sequence, 'o-')
        plt.xlabel('Disease Probability')
        plt.ylabel('Infection Fraction')
        plt.title(network_types[i] + ', SIS(mu=%.1f, p0=%.1f)' % (mu, p0))
        plt.savefig('figures/' + network_types[i][:2] + '_' + str(mu) + '.png')
        plt.close()

    i += 1





network_types = ['SF(N=1000, gamma=2.5)', 'ER(N=1000, <K>=8)', 'Real(N=3618)'];

NT = NetworkTools();
G = NT.reading_networks(proposed_networks[3]);
NT.display_network(G);



