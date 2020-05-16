import numpy as np
from RMG_parameters import *

'(1) FUNCTIONS'
'Function for determining whether the block is inside or outside of the terminal'
def check_block_inside (block_location):

    np_array = np.array(block_location)
    np_round_to_tenths = np.around(np_array,2)

    block_location = list(np_round_to_tenths)

    'Check whether point 0 is inside the location'
    if Point(block_location[0]).within(prim_yard) is True or Point(block_location[0]).touches(prim_yard) is True:
        point_0_inside = True
    else:
        point_0_inside = False

    'Check whether point 1 is inside the location'
    if Point(block_location[1]).within(prim_yard) is True or Point(block_location[1]).touches(prim_yard) is True:
        point_1_inside = True
    else:
        point_1_inside = False

    'Check whether point 2 is inside the location'
    if Point(block_location[2]).within(prim_yard) is True or Point(block_location[2]).touches(prim_yard) is True:
        point_2_inside = True
    else:
        point_2_inside = False

    'Check whether point 3 is inside the location'
    if Point(block_location[3]).within(prim_yard) is True or Point(block_location[3]).touches(prim_yard) is True:
        point_3_inside = True
    else:
        point_3_inside = False

    return point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location

'Function for checking whether the points are inside or outside the terminal'
def check_point_inside_com (check_point):

    'Check whether check_point 0 is inside the location'
    if Point(check_point[0]).within(prim_yard) is True or Point(check_point[0]).touches(prim_yard) is True:
        check_point_1 = True
    else:
        check_point_1 = False

    'Check whether check_point 1 is inside the location'
    if Point(check_point[1]).within(prim_yard) is True or Point(check_point[1]).touches(prim_yard) is True:
        check_point_2 = True
    else:
        check_point_2 = False

    'Check whether all check_point is inside the container terminal'
    if check_point_1 is True and check_point_2 is True:
        check_point_inside = True
    else:
        check_point_inside = False

    return check_point_inside

'(2) Algorithm for container blocks generation'
def generate_blocks (current_origin, block_length, block_width, block_location, container_location, i, m):

    'Check whether the point in block is inside the terminal'
    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

    """Algorithm for the case : There is possibility for : 
    A  container block can be placed in the space on the x- direction
    
    But, this is an exception for the first container block, because the algorithm should not be repeated
    This exception is indicated by the parameter : m"""

    if block_location[0][0] == starting_origin[0] and block_location[0][1] == starting_origin[1] and m == 0:

        'Check whether it is possible to place a container block that fulfill minimum block length requirement'
        'Check point on the top of the container block'
        check_point_top = [[block_location[1][0], block_location[1][1] - min_block_length],
                           [block_location[2][0] + block_width, block_location[2][1] - min_block_length]]

        check_point_inside_top = check_point_inside_com(check_point_top)

        'Check point on the top of the container block'
        check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                           [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

        check_point_inside_bot = check_point_inside_com(check_point_bot)

        if (check_point_inside_top is True and point_0_inside is True and point_3_inside is True) or (check_point_inside_bot is True and point_1_inside is True and point_2_inside is True):
            while (check_point_inside_top is True and point_0_inside is True and point_3_inside is True) or (check_point_inside_bot is True and point_1_inside is True and point_2_inside is True):

                'Move the current origin to the previous block in the bay direction'
                current_origin[0] = block_location[0][0] - block_width - rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                'Check point on the top of the container block'
                check_point_top = [[block_location[1][0], block_location[1][1] - min_block_length],
                                   [block_location[2][0] + block_width, block_location[2][1] - min_block_length]]

                check_point_inside_top = check_point_inside_com(check_point_top)

                'Check point on the top of the container block'
                check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                                   [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

                check_point_inside_bot = check_point_inside_com(check_point_bot)

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            'Determine the location after the while loop: Move the current origin by 1 block'
            current_origin[0] = block_location[0][0] + block_width + rmg_margin_parallel

            'Determine all new points of the container block'
            block_location = [[current_origin[0], current_origin[1]],
                              [current_origin[0], current_origin[1] + block_length],
                              [current_origin[0] + block_width, current_origin[1] + block_length],
                              [current_origin[0] + block_width, current_origin[1]],
                              [current_origin[0], current_origin[1]]]

            'Parameters for exception case : first container block'
            m = m + 1

            'Check whether all points of the point in block is inside the terminal'
            point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                block_location)

    'Case 1 : Check all block_location, whether all is inside'
    if point_0_inside is True and point_1_inside is True and point_2_inside is True and point_3_inside is True:

        'Define that it is possible to place on the next container block in bay direction'
        possible_placement = True

        'Draw the container block'
        if block_location[1][1] - block_location[0][1] > min_block_length:

            # Drawing rectangle for the representation of the blocks
            rectangle = plt.Rectangle(block_location[0], block_width, block_location[1][1] - block_location[0][1], fc='white', ec="black")
            plt.gca().add_patch(rectangle)

            'Determine number of container in the container block on bay direction'
            number_of_container_bay = math.floor((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) / rmg_gross_tgs_y)

            'Define clearance space for each container'
            container_clearance_x = rmg_gross_tgs_x - container_x
            container_clearance_y = ((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) - number_of_container_bay * container_y) / (number_of_container_bay - 1)

            'Define new current origin for the algorithm in drawing the TGS'
            container_current_origin = block_location[0][0] + rmg_track_width + container_clearance_x / 2, block_location[0][1] + rmg_length_buffer

            p = 0
            q = 0

            for p in range (0,number_of_container_row):
                for q in range (0, number_of_container_bay):
                    # container = plt.Rectangle(container_current_origin, container_x, container_y, fc = "white", ec = "black")
                    # plt.gca().add_patch(container)
                    # above are not active because takes a lot of computational to draw each containers, but it can be activated for visualization

                    'Determine the container location'
                    container_location[0] = [container_current_origin[0], container_current_origin[1]]
                    container_location[1] = [container_current_origin[0], container_current_origin[1] + container_y]
                    container_location[2] = [container_current_origin[0] + container_x, container_current_origin[1] + container_y]
                    container_location[3] = [container_current_origin[0], +container_x, container_current_origin[1]]
                    container_location[4] = [container_current_origin[0], container_current_origin[1]]

                    'Determine new all points of the container block'
                    container_location = [container_location[0],
                                          container_location[1],
                                          container_location[2],
                                          container_location[3],
                                          container_location[4]]

                    'Add the current container_location to the container_list'
                    container_list.append(container_location)

                    'Move container to the next location'
                    container_current_origin = container_current_origin[0], container_current_origin[1] + container_y + container_clearance_y

                'Move container to the next location'
                q = 0
                container_current_origin = container_current_origin[0] + container_x + container_clearance_x , block_location[0][1] + rmg_length_buffer

            'Add the current block location to the block_list'
            block_list.append(block_location)

        'Move the current origin to the next block in the bay direction'
        current_origin[0] = block_location[3][0] + rmg_margin_parallel

        'Determine all new points of the container block'
        block_location = [[current_origin[0], current_origin[1]],
                          [current_origin[0], current_origin[1] + block_length],
                          [current_origin[0] + block_width, current_origin[1] + block_length],
                          [current_origin[0] + block_width, current_origin[1]],
                          [current_origin[0], current_origin[1]]]

        return current_origin, possible_placement, block_location, container_location, i, m

    'Case 2 : Check block_location[1] or block_location[2], whether it is inside and whether it is still possible to place a container block that fulfill minimum block length'
    if point_1_inside is False or point_2_inside is False:
        'Check whether it is possible to place a container block that fulfill minimum block length requirement'
        'Check point on the top of the container block'
        check_point_top = [[block_location[0][0], block_location[0][1] + min_block_length],
                           [block_location[3][0], block_location[3][1] + min_block_length]]

        check_point_inside_top = check_point_inside_com(check_point_top)

        if check_point_inside_top is True:
            'Algorithm to decrease the block length on the top side'
            while point_1_inside is False or point_2_inside is False:
                'Determine the new block location on the new row direction'
                block_location[0] = block_location[0]
                block_location[1] = [block_location[1][0], block_location[1][1] - rmg_gross_tgs_y]
                block_location[2] = [block_location[2][0], block_location[2][1] - rmg_gross_tgs_y]
                block_location[3] = block_location[3]
                block_location[4] = block_location[4]

                'Determine new all points of the container block'
                block_location = [block_location[0],
                                  block_location[1],
                                  block_location[2],
                                  block_location[3],
                                  block_location[4]]

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            'Algorithm to increase the block length on the bottom side'
            'Algorithm to limit the increasing block length on the bottom side so that it is not clashing with the container in the previous row'

            if triangular == 1:
                if l >= 1:
                    k = max_number_of_blocks_bay * (l - 1) + 1
                else:
                    k = 0
            else:
                if l >= 1:
                    k = max_number_of_blocks_bay * (l - 1) + 5
                else:
                    k = 0

            if m == 1 or 'reversed_triangular' in globals():

                'This is an exception for the first container block, because the algorithm should not be repeated'
                'The exception is indicated by the parameter : m'

                if m == 1 or reversed_triangular == 1:
                    'Define that it is possible to place on the next container block in bay direction'
                    possible_placement = True

                    'Draw the container block'
                    if block_location[1][1] - block_location[0][1] > min_block_length:
                        # Drawing rectangle for the representation of the blocks
                        rectangle = plt.Rectangle(block_location[0], block_width, block_location[1][1] - block_location[0][1], fc='white', ec="black")
                        plt.gca().add_patch(rectangle)

                        'Determine number of container in the container block on bay direction'
                        number_of_container_bay = math.floor((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) / rmg_gross_tgs_y)

                        'Define clearance space for each container'
                        container_clearance_x = rmg_gross_tgs_x - container_x
                        container_clearance_y = ((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) - number_of_container_bay * container_y) / (number_of_container_bay - 1)

                        'Define new current origin for the algorithm in drawing the TGS'
                        container_current_origin = block_location[0][0] + rmg_track_width + container_clearance_x / 2, block_location[0][1] + rmg_length_buffer

                        p = 0
                        q = 0

                        for p in range (0,number_of_container_row):
                            for q in range (0, number_of_container_bay):
                                # container = plt.Rectangle(container_current_origin, container_x, container_y, fc = "white", ec = "black")
                                # plt.gca().add_patch(container)
                                # above are not active because takes a lot of computational to draw each containers, but it can be activated for visualization

                                'Determine the container location'
                                container_location[0] = [container_current_origin[0], container_current_origin[1]]
                                container_location[1] = [container_current_origin[0], container_current_origin[1] + container_y]
                                container_location[2] = [container_current_origin[0] + container_x, container_current_origin[1] + container_y]
                                container_location[3] = [container_current_origin[0], +container_x, container_current_origin[1]]
                                container_location[4] = [container_current_origin[0], container_current_origin[1]]

                                'Determine new all points of the container block'
                                container_location = [container_location[0],
                                                      container_location[1],
                                                      container_location[2],
                                                      container_location[3],
                                                      container_location[4]]

                                'Add the current container_location to the container_list'
                                container_list.append(container_location)

                                'Move container to the next location'
                                container_current_origin = container_current_origin[0], container_current_origin[1] + container_y + container_clearance_y

                            'Move container to the next location'
                            q = 0
                            container_current_origin = container_current_origin[0] + container_x + container_clearance_x , block_location[0][1] + rmg_length_buffer

                        'Add the current block location to the block_list'
                        block_list.append(block_location)

                        'Move the current origin to the next block in the bay direction'
                        current_origin[0] = block_location[3][0] + rmg_margin_parallel

                        'Determine all new points of the container block'
                        block_location = [[current_origin[0], current_origin[1]],
                                          [current_origin[0], current_origin[1] + block_length],
                                          [current_origin[0] + block_width, current_origin[1] + block_length],
                                          [current_origin[0] + block_width, current_origin[1]],
                                          [current_origin[0], current_origin[1]]]

                        'Parameters for exception case : first container block'
                        m = m + 1

                        'Check whether the point in block is inside the terminal'
                        point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            elif block_location[0][1] - block_list[k][1][1] >= 2 * rmg_margin_stack + rmg_traffic_lane - 0.1:
                while point_0_inside is True and point_3_inside is True and block_location[0][1] - block_list[k][1][1] >= 2 * rmg_margin_stack + rmg_traffic_lane - 0.1:  # THERE IS ALSO A PROBLEM HERE
                    'Determine the new block location on the new row direction'
                    block_location[0] = [block_location[0][0], block_location[0][1] - rmg_gross_tgs_y]
                    block_location[1] = [block_location[1][0], block_location[1][1]]
                    block_location[2] = [block_location[2][0], block_location[2][1]]
                    block_location[3] = [block_location[3][0], block_location[3][1] - rmg_gross_tgs_y]
                    block_location[4] = [block_location[4][0], block_location[4][1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether the point in block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                'Determine the new block location on the new row direction'
                block_location[0] = [block_location[0][0], block_location[0][1] + rmg_gross_tgs_y]
                block_location[1] = [block_location[1][0], block_location[1][1]]
                block_location[2] = [block_location[2][0], block_location[2][1]]
                block_location[3] = [block_location[3][0], block_location[3][1] + rmg_gross_tgs_y]
                block_location[4] = [block_location[4][0], block_location[4][1]]

                'Determine new all points of the container block'
                block_location = [block_location[0],
                                  block_location[1],
                                  block_location[2],
                                  block_location[3],
                                  block_location[0]]

                'Check whether the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                'Determine the new current_origin'
                current_origin = [block_location[0][0], block_location[0][1]]

            if point_0_inside is True and point_1_inside is True and point_2_inside is True and point_3_inside is True:
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = True

                'Draw the container block'
                if block_location[1][1] - block_location[0][1] > min_block_length:
                    # Drawing rectangle for the representation of the blocks
                    rectangle = plt.Rectangle(block_location[0], block_width, block_location[1][1] - block_location[0][1], fc='white', ec="black")
                    plt.gca().add_patch(rectangle)

                    'Determine number of container in the container block on bay direction'
                    number_of_container_bay = math.floor((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) / rmg_gross_tgs_y)

                    'Define clearance space for each container'
                    container_clearance_x = rmg_gross_tgs_x - container_x
                    container_clearance_y = ((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) - number_of_container_bay * container_y) / (number_of_container_bay - 1)

                    'Define new current origin for the algorithm in drawing the TGS'
                    container_current_origin = block_location[0][0] + rmg_track_width + container_clearance_x / 2, block_location[0][1] + rmg_length_buffer

                    p = 0
                    q = 0

                    for p in range (0,number_of_container_row):
                        for q in range (0, number_of_container_bay):
                            # container = plt.Rectangle(container_current_origin, container_x, container_y, fc = "white", ec = "black")
                            # plt.gca().add_patch(container)
                            # above are not active because takes a lot of computational to draw each containers, but it can be activated for visualization

                            'Determine the container location'
                            container_location[0] = [container_current_origin[0], container_current_origin[1]]
                            container_location[1] = [container_current_origin[0], container_current_origin[1] + container_y]
                            container_location[2] = [container_current_origin[0] + container_x, container_current_origin[1] + container_y]
                            container_location[3] = [container_current_origin[0], +container_x, container_current_origin[1]]
                            container_location[4] = [container_current_origin[0], container_current_origin[1]]

                            'Determine new all points of the container block'
                            container_location = [container_location[0],
                                                  container_location[1],
                                                  container_location[2],
                                                  container_location[3],
                                                  container_location[4]]

                            'Add the current container_location to the container_list'
                            container_list.append(container_location)

                            'Move container to the next location'
                            container_current_origin = container_current_origin[0], container_current_origin[1] + container_y + container_clearance_y

                        'Move container to the next location'
                        q = 0
                        container_current_origin = container_current_origin[0] + container_x + container_clearance_x , block_location[0][1] + rmg_length_buffer

                    'Add the current block location to the block_list'
                    block_list.append(block_location)

                'Move the current origin to the next block in the bay direction'
                current_origin[0] = block_location[3][0] + rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

            return current_origin, possible_placement, block_location, container_location, i, m

        else:
            'j : parameters that is the indicator for the while loop to stop if the loop is already reached 20 times --> stops '
            j = 0

            while check_point_inside_top is False and j in range(0, 20):
                j = j + 1

                'Move the current origin to the next block in the bay direction'
                current_origin[0] = block_location[3][0] + rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                'Check point on the top of the container block'
                check_point_top = [[block_location[0][0], block_location[0][1] + min_block_length],
                                   [block_location[3][0] + block_width, block_location[3][1] + min_block_length]]

                check_point_inside_top = check_point_inside_com(check_point_top)

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            if j == 20:
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = False

                'Define new current_origin point to the next container block in row direction'
                current_origin = [block_list[0][0][0], current_origin[1] + block_length + rmg_traffic_lane + 2 * rmg_margin_stack]

                block_location[0] = [block_list[0][0][0], current_origin[1]]
                block_location[1] = [block_list[0][1][0], current_origin[1] + block_length]
                block_location[2] = [block_list[0][2][0], current_origin[1] + block_length]
                block_location[3] = [block_list[0][3][0], current_origin[1]]
                block_location[4] = [block_list[0][0][0], current_origin[1]]

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                """Algorithm for the case : There is possibility for : 
                A  container block can be placed in the space on the x- direction"""

                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                'Check point on the top of the container block'
                check_point_top = [[block_location[1][0], block_location[1][1] - min_block_length],
                                   [block_location[2][0] + block_width, block_location[2][1] - min_block_length]]

                check_point_inside_top = check_point_inside_com(check_point_top)

                'Check point on the top of the container block'
                check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                                   [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

                check_point_inside_bot = check_point_inside_com(check_point_bot)

                while (check_point_inside_top is True and point_0_inside is True and point_3_inside is True) or (check_point_inside_bot is True and point_1_inside is True and point_2_inside is True):
                    'Move the current origin to the previous block in the bay direction'
                    current_origin[0] = block_location[0][0] - block_width - rmg_margin_parallel

                    'Determine all new points of the container block'
                    block_location = [[current_origin[0], current_origin[1]],
                                      [current_origin[0], current_origin[1] + block_length],
                                      [current_origin[0] + block_width, current_origin[1] + block_length],
                                      [current_origin[0] + block_width, current_origin[1]],
                                      [current_origin[0], current_origin[1]]]

                    'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                    'Check point on the top of the container block'
                    check_point_top = [[block_location[1][0], block_location[1][1] - min_block_length],
                                       [block_location[2][0] + block_width, block_location[2][1] - min_block_length]]

                    check_point_inside_top = check_point_inside_com(check_point_top)

                    'Check point on the top of the container block'
                    check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                                       [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

                    check_point_inside_bot = check_point_inside_com(check_point_bot)

                    'Check whether all points of the point in block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                        block_location)

                'Determine the location after the while loop: Move the current origin by 1 block'
                current_origin[0] = block_location[0][0] + block_width + rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            else:
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = True

            return current_origin, possible_placement, block_location, container_location, i, m

    'Case 3 : Check block_location[0] or block_location[3], whether it is inside and whether it is still possible to place a container block that fulfill minimum block length'
    if point_0_inside is False or point_3_inside is False:

        'Check whether it is possible to place a container block that fulfill minimum block length requirement'
        'Check point on the bottom of the container block'
        check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                           [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

        check_point_inside_bot = check_point_inside_com(check_point_bot)

        if check_point_inside_bot is True:
            while point_0_inside is False or point_3_inside is False:
                'Determine the new block location on the new row direction'
                block_location[0] = [block_location[0][0], block_location[0][1] + + rmg_gross_tgs_y]
                block_location[1] = [block_location[1][0], block_location[1][1]]
                block_location[2] = [block_location[2][0], block_location[2][1]]
                block_location[3] = [block_location[3][0], block_location[3][1] + rmg_gross_tgs_y]
                block_location[4] = [block_location[4][0], block_location[4][1]]

                'Determine new all points of the container block'
                block_location = [block_location[0],
                                  block_location[1],
                                  block_location[2],
                                  block_location[3],
                                  block_location[4]]

                'Check whether all points in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            if point_0_inside is True and point_1_inside is True and point_2_inside is True and point_3_inside is True:
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = True

                'Draw the container block'
                if block_location[1][1] - block_location[0][1] > min_block_length:
                    # Drawing rectangle for the representation of the blocks
                    rectangle = plt.Rectangle(block_location[0], block_width, block_location[1][1] - block_location[0][1], fc='white', ec="black")
                    plt.gca().add_patch(rectangle)

                    'Determine number of container in the container block on bay direction'
                    number_of_container_bay = math.floor((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) / rmg_gross_tgs_y)

                    'Define clearance space for each container'
                    container_clearance_x = rmg_gross_tgs_x - container_x
                    container_clearance_y = ((block_location[1][1] - block_location[0][1] - 2 * rmg_length_buffer) - number_of_container_bay * container_y) / (number_of_container_bay - 1)

                    'Define new current origin for the algorithm in drawing the TGS'
                    container_current_origin = block_location[0][0] + rmg_track_width + container_clearance_x / 2, block_location[0][1] + rmg_length_buffer

                    p = 0
                    q = 0

                    for p in range(0, number_of_container_row):
                        for q in range(0, number_of_container_bay):
                            # container = plt.Rectangle(container_current_origin, container_x, container_y, fc = "white", ec = "black")
                            # plt.gca().add_patch(container)
                            # above are not active because takes a lot of computational to draw each containers, but it can be activated for visualization

                            'Determine the container location'
                            container_location[0] = [container_current_origin[0], container_current_origin[1]]
                            container_location[1] = [container_current_origin[0], container_current_origin[1] + container_y]
                            container_location[2] = [container_current_origin[0] + container_x, container_current_origin[1] + container_y]
                            container_location[3] = [container_current_origin[0], +container_x, container_current_origin[1]]
                            container_location[4] = [container_current_origin[0], container_current_origin[1]]

                            'Determine new all points of the container block'
                            container_location = [container_location[0],
                                                  container_location[1],
                                                  container_location[2],
                                                  container_location[3],
                                                  container_location[4]]

                            'Add the current container_location to the container_list'
                            container_list.append(container_location)

                            'Move container to the next location'
                            container_current_origin = container_current_origin[0], container_current_origin[1] + container_y + container_clearance_y

                        'Move container to the next location'
                        q = 0
                        container_current_origin = container_current_origin[0] + container_x + container_clearance_x, block_location[0][1] + rmg_length_buffer

                    'Add the current block location to the block_list'
                    block_list.append(block_location)

                'Move the current origin to the next block in the bay direction'
                current_origin[0] = block_location[3][0] + rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

            return current_origin, possible_placement, block_location, container_location, i, m

        else:
            'j : parameters that is the indicator for the while loop to stop if the loop is already reached 20 times --> stops '
            j = 0

            while check_point_inside_bot is False and j in range(0, 20):
                j = j + 1

                'Move the current origin to the next block in the bay direction'
                current_origin[0] = block_location[3][0] + rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                'Check point on the bottom of the container block'
                check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                                   [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

                check_point_inside_bot = check_point_inside_com(check_point_bot)

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            if j == 20:
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = False

                'Define new current_origin point to the next container block in row direction'
                current_origin = [block_list[0][0][0], current_origin[1] + block_length + rmg_traffic_lane + 2 * rmg_margin_stack]

                block_location[0] = [block_list[0][0][0], current_origin[1]]
                block_location[1] = [block_list[0][1][0], current_origin[1] + block_length]
                block_location[2] = [block_list[0][2][0], current_origin[1] + block_length]
                block_location[3] = [block_list[0][3][0], current_origin[1]]
                block_location[4] = [block_list[0][0][0], current_origin[1]]

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                """Algorithm for the case : There is possibility for : 
                A  container block can be placed in the space on the x- direction"""

                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                'Check point on the top of the container block'
                check_point_top = [[block_location[1][0], block_location[1][1] - min_block_length],
                                   [block_location[2][0] + block_width, block_location[2][1] - min_block_length]]

                check_point_inside_top = check_point_inside_com(check_point_top)

                'Check point on the top of the container block'
                check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                                   [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

                check_point_inside_bot = check_point_inside_com(check_point_bot)

                while (check_point_inside_top is True and point_0_inside is True and point_3_inside is True) or (check_point_inside_bot is True and point_1_inside is True and point_2_inside is True):
                    'Move the current origin to the previous block in the bay direction'
                    current_origin[0] = block_location[0][0] - block_width - rmg_margin_parallel

                    'Determine all new points of the container block'
                    block_location = [[current_origin[0], current_origin[1]],
                                      [current_origin[0], current_origin[1] + block_length],
                                      [current_origin[0] + block_width, current_origin[1] + block_length],
                                      [current_origin[0] + block_width, current_origin[1]],
                                      [current_origin[0], current_origin[1]]]

                    'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                    'Check point on the top of the container block'
                    check_point_top = [[block_location[1][0], block_location[1][1] - min_block_length],
                                       [block_location[2][0] + block_width, block_location[2][1] - min_block_length]]

                    check_point_inside_top = check_point_inside_com(check_point_top)

                    'Check point on the top of the container block'
                    check_point_bot = [[block_location[0][0], block_location[0][1] + min_block_length],
                                       [block_location[0][0] + block_width, block_location[0][1] + min_block_length]]

                    check_point_inside_bot = check_point_inside_com(check_point_bot)

                    'Check whether all points of the point in block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                        block_location)

                'Determine the location after the while loop: Move the current origin by 1 block'
                current_origin[0] = block_location[0][0] + block_width + rmg_margin_parallel

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1] + block_length],
                                  [current_origin[0] + block_width, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether all points of the point in block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                    block_location)

            else:
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = True

            return current_origin, possible_placement, block_location, container_location, i, m