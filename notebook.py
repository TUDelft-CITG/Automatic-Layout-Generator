#!/usr/bin/env python
# coding: utf-8

# # Container terminal example
# This notebook provides an example of the development of an container terminal over time with changing demand as the main driver.

# The example uses the OpenTISim package. For a given terminal type the package contains an:
# * _objects module_ - specifying potential properties of terminal objects, a
# * _defaults module_ - listing a range of reasonable default values that can be used to instantiate terminal objects, and a
# * _system module_ - that contains the parametric relations to develop the terminal.
# 
# Some variables need to be set at the beginning:
# * _startyear_ - can be any year
# * _lifecycle_ - the number of years for which the simulation need to run, e.g. 10 years
# * _system elements_ - elements the terminal needs to start with (minimum demand scenarios and vessel distribution)
# * _terminal_defaults_ - the default equipment to use when several options are available

# The simulation follows the 'complete supply chain' concept. The simulation starts at the predicted cargo scenario. From that for each year 
# * --> the number of required vessels is determined 
# * --> based on a berth occupancy triggers the nr of required berths and quay length is calculated 
# * --> then the nr of unloading cranes required is calculated (trigger: berth occupancy + unloading default) 
# * --> next the nr of horizontal transport units required is calculated (trigger: berth occupancy) 
# * --> next required stack capacity is calculated (trigger: berth occupancy & dwell time + storage default) 
# * --> next the capacity of the hinterland connection required is calculated  


# Whenever the simulation decides to add a terminal object it adds this to the Terminal.elements list. At the end of the simulation a cash flow analysis is performed. Based on the year an element is added (known from Terminal.elements\[object\]) the elements CAPEX and OPEX are calculated. Some of the operational expenses are a function of the actual throughput (e.g. energy costs). 

# Each terminal element is assumed to carry a value identical to its purchasing cost, which is linearly depreciated over its lifespan. Once an asset reaches the end of its lifespan, it is assumed that a full reinvestment is required. At the end of the project’s lifecycle, the value of all remaining assets is compounded into a single virtual positive cashflow in the last year, thus contributing to a project’s NPV.

# Once all cashflows are known the performance of the terminal can be translated to Net Present Value (NPV). 

'0. Import libraries'

import numpy as np
import pandas as pd
import statistics as st

import matplotlib.pyplot as plt
import math

import container_objects
import container_defaults
import container_system
import core
import plot
from container_objects import *

'1. Prepare inputs'
'1.1 Specify startyear and required lifecycle'
startyear = 2020
lifecycle = 10
years = list(range(startyear, startyear + lifecycle))

'1.2 Specify demand'
# 'scenario_data': demand for containers during 'years'
scenario_data = {}
scenario_data.update({'year': [], 'volume': []})

for year in years:
    if year <= 2025:
        throughput = 500_000
    else:
        throughput = 800_000

    scenario_data['year'].append(year)
    scenario_data['volume'].append(throughput)

# modify container defaults according to case at hand
# - specify modal split over calling vessels
container_defaults.container_data['fully_cellular_perc'] = 0
container_defaults.container_data['panamax_perc'] = 0
container_defaults.container_data['panamax_max_perc'] = 0
container_defaults.container_data['post_panamax_I_perc'] = 0
container_defaults.container_data['post_panamax_II_perc'] = 0
container_defaults.container_data['new_panamax_perc'] = 100
container_defaults.container_data['VLCS_perc'] = 0
container_defaults.container_data['ULCS_perc'] = 0

# instantiate commodity object (add scenario_data) and add commodity object to 'demand' variable
container = container_objects.Commodity(**container_defaults.container_data)
container.scenario_data = pd.DataFrame(data=scenario_data)

# demand variable: contains info on cargo (to be added to Terminal.elements)
demand = [container]

#container.plot_demand()

'1.3 Specify vessels'

# instantiate vessels
fully_cellular = container_objects.Vessel(**container_defaults.fully_cellular_data)
panamax = container_objects.Vessel(**container_defaults.panamax_data)
panamax_max = container_objects.Vessel(**container_defaults.panamax_max_data)
post_panamax_I = container_objects.Vessel(**container_defaults.post_panamax_I_data)
post_panamax_II = container_objects.Vessel(**container_defaults.post_panamax_II_data)
new_panamax = container_objects.Vessel(**container_defaults.new_panamax_data)
VLCS = container_objects.Vessel(**container_defaults.VLCS_data)
ULCS = container_objects.Vessel(**container_defaults.ULCS_data)

# vessels variable: contains info on vessels (to be added to Terminal.elements)
vessels = [fully_cellular, panamax, panamax_max, post_panamax_I, post_panamax_II, new_panamax, ULCS, VLCS]


'1.4 Specify terminal shape and dimensions'
# Rectangular
rectangular = [[0, 0],
          [0,800],
          [1200,800],
          [1200, 0],
          [0, 0]]

# Triangular
triangular = [[0,0],
          [0,1800],
          [1800,0],
          [0,0]]

# Reversed Triangular
triangular_rev = [[0,0],
          [1800,1800],
          [1800,0],
          [0,0]]

# Small Trapezoidal
trapezoidal_s = [[0, 0],
          [0,300],
          [400,600],
          [800,600],
          [1200,300],
          [1200,0],
          [0,0]]

# Medium Trapezoidal
trapezoidal_m = [[0, 0],
          [0,450],
          [600,900],
          [1200,900],
          [1800,450],
          [1800,0],
          [0,0]]

# Large Trapezoidal
trapezoidal_l = [[0, 0],
          [0,600],
          [800,1200],
          [1600,1200],
          [2400,600],
          [2400,0],
          [0,0]]

trapezoidal_xl = [[0, 0],
          [0,900],
          [1200,1600],
          [2400,1600],
          [3600,900],
          [3600,0],
          [0,0]]

# Small Reverse Trapezoidal
trapezoidal_s_rev = [[0, 0],
          [-400,300],
          [-400,600],
          [800,600],
          [800,300],
          [400,0],
          [0,0]]

# Medium Reverse Trapezoidal
trapezoidal_m_rev = [[0, 0],
          [-600,450],
          [-600,900],
          [1200,900],
          [1200,450],
          [600,0],
          [0,0]]

# Large  Reverse Trapezoidal
trapezoidal_l_rev = [[0, 0],
          [-800,600],
          [-800,1200],
          [1600,1200],
          [1600,600],
          [800,0],
          [0,0]]

# Xtra Large Reverse Trapezoidal
trapezoidal_xl_rev = [[0, 0],
          [-1200,800],
          [-1200,1600],
          [2400,1600],
          [2400,800],
          [1200,0],
          [0,0]]

# Port Mauritius Case
mauritius = [[0,0],
          [0,190],
          [390,380],
          [790,460],
          [1245,460],
          [1245,0],
          [0,0]]

# Reversed Port Mauritius Case
mauritius_rev = [[0,0],
          [0,460],
          [455,460],
          [855,380],
          [1245,190],
          [1245,0],
          [0,0]]

# Any terminal shape and dimension can be determined here by coodinates
custom = [[]]

'Define terminal coordinates'
coords = rectangular

'2. Instantiate terminal system'

# initialise terminal object with: startyear, lifecycle, elements (demand + vessels) + defaults
Terminal = container_system.System(
    terminal_name='Terminal 01',  # terminal name
    startyear=startyear,  # startyear
    lifecycle=lifecycle,  # number of simulation years
    elements=demand + vessels,  # terminal elements at T=0
    operational_hours=7500,  # operational hours (example Wijnand: 5840)
    debug=True,  # toggle: intermediate print statements
    crane_type_defaults=container_defaults.sts_crane_data,  # specify defaults: crane type to use
    stack_equipment='rtg',  # specify defaults: stack equipment to use
    laden_stack='rtg',  # specify defaults: crane type to use
    space_boundary=True,
    coords=coords)   # toggle: including the space boundary)   # specify defaults: number of row per container block

'3. Start simulation'

Terminal.simulate()

# ## Report all elements

if False:
    for element in Terminal.elements:
        print("")
        print(element.name)
        print("")
        print(element.__dict__)

# ### Plot when terminal elements come online

self = Terminal
quay = core.find_elements(self, Quay_wall)

print('')
print('*** Summary: {}'.format(self.terminal_name))
print('Number of quays: {}'.format(len(core.find_elements(self, Quay_wall))))
print('Quay length: {:.2f}'.format(np.sum([element.length for element in core.find_elements(self, Quay_wall)])))
print('Quay unit rate: {:.2f} USD / m'.format(np.mean([element.unit_rate for element in core.find_elements(self, Quay_wall)])))
print('Quay retaining height: {:.2f} m [2 * (draught + max_sinkage + wave_motion + safety_margin + freeboard)]'.format(
    np.mean([element.retaining_height for element in core.find_elements(self, Quay_wall)])))
print('Apron surface: {:.2f} ha'.format(np.sum([element.length for element in core.find_elements(self, Quay_wall)]) * quay[0].apron_width * 0.0001))
print('STS cranes: {}'.format(len(core.find_elements(self, Cyclic_Unloader))))
print('Horizontal transport: {} (coupled with STS cranes)'.format(len(core.find_elements(self, Horizontal_Transport))))
print('Stack equipment: {} (type: {})'.format(len(core.find_elements(self, Stack_Equipment)), self.stack_equipment))
print('Number of laden/reefer stacks: {}'.format(len(core.find_elements(self, Laden_Stack))))
print('Number of emtpy stacks: {}'.format(len(core.find_elements(self, Empty_Stack))))
print('Number of OOG stacks: {}'.format(len(core.find_elements(self, OOG_Stack))))
print('Empty handlers: {} (coupled with STS cranes)'.format(len(core.find_elements(self, Empty_Handler))))
print('Number of gates: {}'.format(len(core.find_elements(self, Gate))))

Terminal.terminal_elements_plot(demand_step=100000)

# ### Calculate and plot cashflows

cash_flows, cash_flows_WACC_real = core.add_cashflow_elements(Terminal, container_objects.Labour(**container_defaults.labour_data))

plot.cashflow_plot(Terminal, cash_flows, title='Cash flow plot')

plot.cashflow_plot(Terminal, cash_flows_WACC_real, title='Cash flow plot (WACC real)')

df = core.NPV(Terminal, container_objects.Labour(**container_defaults.labour_data))

# ### Terminal operation plots
Terminal.land_use_plot()

Terminal.terminal_capacity_plot()

Terminal.terminal_layout_plot()

plt.show()