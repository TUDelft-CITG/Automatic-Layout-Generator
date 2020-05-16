import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import math
import numpy as np

from LG_input import *

if equipment_type == "RTG":
    from RTG_system import *
if equipment_type == "RMG":
    from RMG_system import *
if equipment_type == "SC":
    from SC_system import *
if equipment_type == "RS":
    from RS_system import *

'(1) While loop function for generating the container blocks in the terminal'
while block_top <= max(s):

    current_origin, possible_placement, block_location, container_location, i, m = generate_blocks(current_origin, block_length, block_width, block_location, container_location, i, m)

    if equipment_type == "RTG":
        if possible_placement is False:
            block_top = block_top + block_width + rtg_bypass_lane

    if equipment_type == "RMG":
        if possible_placement is False:
            block_top = block_top + block_length + 2 * rmg_margin_stack + rmg_traffic_lane
            l = l + 1  # parameters for algorithm to limit the increasing block length on the bottom side so that it is not clashing with the container in the previous row

    if equipment_type == "SC":
        if possible_placement is False:
            block_top = block_top + block_length + sc_traffic_lane

    if equipment_type == "RS":
        if possible_placement is False:
            block_top = block_top + block_width + rs_operating_space

'(2) Results'
if equipment_type == "SC" :
    print("Results for equipment type : " + equipment_type)
else:
    print("Results for equipment type : " + equipment_type + " with number of container row in a block : " + str(number_of_container_row))

total_blocks = str(len(block_list))
total_tgs = str(len(container_list))

print("Number of container blocks = " + str(len(block_list)))
print("Number of total TGS = " + str(len(container_list)))

'Plotting'
'Title of the Plot'
# plt.suptitle('Case : Trapezoid Terminal; Long Base = 1200 m; Short Base = 500 m, Height : 500 m')

'Set x-axis and y-axis to be equal'
plt.axis('equal')

'Set label for x-axis and y-axis'
plt.xlabel('x (m)')
plt.ylabel('y (m)')

plt.plot(v, w)  # Plot total terminal area WITHOUT traffic lane'
plt.plot(r, s)  # Plot primary yard area with traffic lane'
plt.plot(t, u)  # Plot primary yard area WITHOUT traffic lane'

'Save figure'
plt.savefig(str(equipment_type) + ' - Row = ' + str(number_of_container_row) + ' - CB = ' + total_blocks + " - TGS = " + total_tgs + '.png')

'Show plot'
plt.show()

