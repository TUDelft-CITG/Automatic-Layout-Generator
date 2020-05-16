import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, LineString
import math

from LG_input import *

'(1) FUNCTIONS'
'Function for determining the quay length'
def calc_quay_length():

    quay_length = coords[(len(coords)) - 2][0] - coords[0][0]

    return quay_length

'Function for determining block length'
def calc_block_length():  # Number of blocks that nearest to the apron side

    'Determine number of blocks in x direction'
    max_blocks_x = math.ceil((quay_length - rs_traffic_lane) / (max_block_length + rs_traffic_lane + 2 * rs_margin_stack))

    'Determine block length"'
    block_length = math.floor((((quay_length - rs_traffic_lane) / max_blocks_x) - rs_traffic_lane - 2 * rs_margin_stack)*100)/100

    return block_length, max_blocks_x

'Function for determining block width'
def calc_block_width (): # Number of blocks that nearest to the apron side

    'Determine block width'
    block_width = number_of_container_row * rs_gross_tgs_y

    'Determine maximum number of blocks in row direction'
    max_blocks_y = math.floor((max(w) - apron_width - rs_traffic_lane) / (block_width + rs_operating_space))

    return block_width, max_blocks_y

'(2) PARAMETERS'
'Defining the parameters value'
'Define i : parameters for the algorithm, to make sure that the edge of container blocks in each row is straight'
i = 0

'Define m : parameters for the algorithm, to identify the first case of the container block generation'
m = 0

'(3b) Define the terminal area based on the coordinates'
'Nomenclature :'
'TERMINAL = Full area of the terminal based on the coordinates' # (3b)
'TERMINAL_WOTL = Effective area of the terminal WITHOUT traffic lane on the edges of the full area of the terminal' # (3b)
'PRIM_YARD = Effective area of the terminal for container stacking (primary yard)' # (4)

'(3b-1) Determining the TERMINAL'
'Creating area using line string, in order to use parallel offset function (because it is not working for polygon)'
terminal_full_line = LineString(coords)

'Creating terminal area that is already decreased by the traffic lane, because it is assumed that traffic lane is available in all side of the container terminal'
'Area that already decreased by the traffic lane = TERMINAL'
terminal_wotl_line = terminal_full_line.parallel_offset(rs_traffic_lane, 'right', join_style=2, mitre_limit=rs_traffic_lane)

'Converting AREA to Polygon'
terminal_full = Polygon(terminal_full_line)
v, w = terminal_full.exterior.xy

'Converting TERMINAL to Polygon'
terminal_wotl = Polygon(terminal_wotl_line)
x, y = terminal_wotl.exterior.xy

'(3c) Define quay area'
'Define the origin point'
origin = [0, 0]
current_origin = [0, 0]

'Determine the quay length'
quay_length = calc_quay_length()

'Draw the apron area'
apron = plt.Rectangle(origin, quay_length, apron_width, fc='red', ec="red")
plt.gca().add_patch(apron)

'(3d) Define block parameter'
'Determine block length'
block_length, max_blocks_x = calc_block_length()

'Determine block width'
block_width, max_blocks_y = calc_block_width()

'(4) DETERMINE EFFECTIVE PRIMARY YARD AREA'
'Determine terminal space in primary yard, so that it can be included to secondary yard and the terminal area can become more effective'
ps_space = max(w) - apron_width - rs_traffic_lane - max_blocks_y * (block_width + rs_operating_space)

'DETERMINE PRIMARY YARD AREA (THAT COMPLY 60-75% PRIMARY YARD TO TOTAL TERMINAL YARD RATIO)'
'Determine the y location of the line that will be iterated to find the 60-75% value primary yard ratio to total terminal yard'
line_y = max(w) - ps_space

'Determine the line'
line = LineString([[min(v) - 1/4 * max(v), line_y], [max(v) + 1/4 * max (v), line_y]])

'Define the intersection point of the line and the terminal area'
intersection = line.intersection(terminal_full_line)

if intersection.geom_type == 'MultiPoint':
    t, u = LineString(intersection).xy
elif intersection.geom_type == 'Point':
    t, u = intersection.xy

'Define parameters for the while loop in determining the primary yard boundary'
p = 0
q = 0

'Determine list for the primary yard coordinate'
coords_prim = list()

'Algorithm in determining the FIRST coordinate points for the primary yard'
'Different approach is implemented for triangular terminal (or terminal that has less or equal than 3 points, because it will generate 1 additional point'
'For case of non-triangular terminal, len(coords) > 4'
if len(coords) > 4:
    for p in range(0, len(coords)):
        if u[0] <= coords[p][1]:
            if q + 1 <= len(u):
                coords_prim.append([t[q], u[q]])
                q = q + 1
            else:
                p = p
        if u[0] >= coords[p][1]:
            coords_prim.append(coords[p])

else:
    for p in range(0, len(coords)):
        if u[0] <= coords[p][1]:
            while q + 1 <= len(u):
                coords_prim.append([t[q], u[q]])
                q = q + 1
            else:
                p = p
        if u[0] >= coords[p][1]:
            coords_prim.append(coords[p])

'Determine the area of the total terminal area'
area_terminal = terminal_full.area

'Determine the primary yard area'
prim_yard = Polygon(coords_prim)

'Determine the area of the primary yard area'
area_prim = prim_yard.area

'Algorithm to find the condition where 60-75% is the value of the primary yard ratio to total terminal yard'
'Determine the desired primary yard to total terminal area ratio'
prim_total_ratio = 0.75

while area_prim/area_terminal >= prim_total_ratio:

    'Determine the y location of the line'
    line_y = math.ceil((line_y - block_width - rs_operating_space)*100)/100

    'Determine the line'
    line = LineString([[min(v) - 1 / 4 * max(v), line_y], [max(v) + 1 / 4 * max(v), line_y]])

    'Define the intersection point of the line and the terminal area'
    intersection = line.intersection(terminal_full_line)

    if intersection.geom_type == 'MultiPoint':
        t, u = LineString(intersection).xy
    elif intersection.geom_type == 'Point':
        t, u = intersection.xy

    'Define parameters for the while loop in determining the primary yard boundary'
    p = 0
    q = 0

    'Determine the primary yard coordinate'
    coords_prim = list()

    'Algorithm in determining the coordinate points for the primary yard'
    if len(coords) > 4:
        for p in range(0, len(coords)):
            if u[0] <= coords[p][1]:
                if q + 1 <= len(u):
                    coords_prim.append([t[q], u[q]])
                    q = q + 1
                else:
                    p = p
            if u[0] >= coords[p][1]:
                coords_prim.append(coords[p])

    else:
        for p in range(0, len(coords)):
            if u[0] <= coords[p][1]:
                while q + 1 <= len(u):
                    coords_prim.append([t[q], u[q]])
                    q = q + 1
                else:
                    p = p
            if u[0] >= coords[p][1]:
                coords_prim.append(coords[p])

    'Determine the primary yard area'
    prim_yard = Polygon(coords_prim)
    area_prim = prim_yard.area

'Creating area for the primary yard using line string, to use parallel offset function (because it is not working for polygon)'
prim_yard_line = LineString(coords_prim)

'Creating terminal area that is already decreased by the traffic lane, because it is assumed that traffic lane is available in all side of the container terminal'
prim_yard_wotl_line = prim_yard_line.parallel_offset(rs_traffic_lane, 'right', join_style=2, mitre_limit=rs_traffic_lane)

'Converting TERMINAL to Polygon'
prim_yard = Polygon(prim_yard_wotl_line)
r,s = prim_yard.exterior.xy


'(5) BLOCK GENERATION PARAMETER'
'The starting origin for the container block is : x = rs_traffic_lane + rs_margin_stack ; y = apron_width + rs_operating space'
starting_origin = [rs_traffic_lane + rs_margin_stack, apron_width + rs_operating_space]

'Moving current_origin to starting origin for the container block'
current_origin = starting_origin

'Define the top of the block parameter for while loop, so it stops if it reaches the top edge of the terminal'
block_top = starting_origin[1] + block_width

'Define block list'
'To list the number of container blocks generated and the location for each container block'
block_list = list()

'Define the first container block location'
block_location = [[current_origin[0], current_origin[1]],
                  [current_origin[0], current_origin[1] + block_width],
                  [current_origin[0] + block_length, current_origin[1] + block_width],
                  [current_origin[0] + block_length, current_origin[1]],
                  [current_origin[0], current_origin[1]]]

'Define container list'
'To list the number of containers generated and the location for each container'
container_list = list()

container_location = [None] * 5