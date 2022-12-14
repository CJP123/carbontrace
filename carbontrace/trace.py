# AUTOGENERATED! DO NOT EDIT! File to edit: ../10_losses.ipynb.

# %% auto 0
__all__ = ['hex_list', 'float_list', 'cmap_1000']

# %% ../10_losses.ipynb 2
from fastcore.utils import *
from .network import *
import networkx as nx
from numpy.linalg import inv
from numpy.linalg import matrix_power
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from continuous_cmap.cmap import *
hex_list = ['#2AA364', '#F5EB4D', '#9E4229', '#381D02', '#381D02', '#381D02']
float_list=[0, 0.15, .6,.75,.8,1]
cmap_1000 = get_continuous_cmap(hex_list = hex_list, float_list = float_list)

# %% ../10_losses.ipynb 10
@patch
def plot2(self:Trace, plot_nodes = None, oer=None ):
        self.fuel = {'I_HYDRO':'Hydro',
        'I_GEO':'Geothermal',
        'II':'Coal',
        'IV':'Geothermal'}
        pos = {'I':(0,0),
                    'II':(.5,0),
                    'III':(1,0),
                    'IV':(1,-.5),
                    'V':(1.5,0),
                    'VI':(1.5,.5),
                    'I_HYDRO':(-.35,0.35),
                    'I_GEO':(-.35,-.35)}
        
        sub_net = self.network.subgraph(plot_nodes) if plot_nodes else self.network
        fig = plt.figure(1, figsize=(20, 10), dpi=60)
        # node_cols = [cmap_1000(self.get_oer(x)[0]) for x in sub_net.nodes]
        # node_cols[1] = cmap_1000(.3)

        options = {
            "font_size": 20,
            "font_color":'black',
            "node_size": 5000,
            "node_color": 'red',
            # "edge_cmap": "cm.magma",
            "edgecolors": 'black',
            "arrowstyle":"->",
            "arrowsize":20,
            "width":5,
            "cmap": cmap_1000
        }

        tmp = nx.draw_networkx(sub_net, pos, **options)

        for x in sub_net.nodes:
            #GENERATION
            flip = 1
            if self.network.nodes[x]['GENERATION_MW'] > 0:
                plt.annotate(f'{round(self.network.nodes[x]["GENERATION_MW"],1)} MW', 
                                xy=(pos[x][0]-.06*np.sin(np.pi/4),
                                    pos[x][1]-.06*np.cos(np.pi/4)), 
                                xytext=(pos[x][0]-.2*np.sin(np.pi/4),
                                        pos[x][1]-.2*np.cos(np.pi/4)),
                                    color='black',
                                    fontsize=12,
                                arrowprops=dict(arrowstyle="->", 
                                                lw=4, 
                                                color="g"))
            #DEMAND
            if self.network.nodes[x]['DEMAND_MW'] > 0:
                plt.annotate(f'{round(self.network.nodes[x]["DEMAND_MW"],1)} MW', 
                            xy=(pos[x][0]+.06*np.sin(np.pi/4),
                                pos[x][1]-.06*np.cos(np.pi/4)), 
                            xytext=(pos[x][0]+.2*np.sin(np.pi/4)-.05,
                                    pos[x][1]-.2*np.cos(np.pi/4)),
                            color='r',fontsize=12,
                            arrowprops=dict(arrowstyle="<-", 
                        lw=4, color="red"))


#       
    
        edge_labels = {}
        for x in sub_net.edges:
#             print(x,self.pos[x[0]],self.pos[x[1]],0.5*abs(self.pos[x[0]][0]+self.pos[x[1]][0]))
            a = sub_net._adj[x[0]][x[1]]["FROM_MW"]
            b = sub_net._adj[x[0]][x[1]]["TO_MW"]
            c = ''+ str(a) + ' MW ' if a==b else ''+str(round(a,1))+' MW / '+str(round(b,1))+ ' MW '
            edge_labels[x] = c
#         cmap = mpl.cm.cool
#         norm = mpl.colors.Normalize(vmin=5, vmax=10)
#         ax = plt.gca()
#         plt.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
#              cax=ax, orientation='horizontal', label='Some Units')

        nx.draw_networkx_edge_labels(
                sub_net, pos,
                edge_labels=edge_labels,
                font_color='black',
                font_size =10
            )
        sm = plt.cm.ScalarMappable(cmap=cmap_1000)
        sm.set_array([])
        cbar = plt.colorbar(sm)
        cbar.ax.get_yaxis().labelpad = 10
        cbar.ax.set_ylabel('kgeCO2/kWh', rotation=270, fontsize=10)
        cbar.ax.set_title('Operating\n Emission Rate')
        plt.axis("off")
        return plt
