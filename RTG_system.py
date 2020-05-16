from RTG_parameters import *

'(1) Functions'
'Function for determining whether the block is inside or outside of the terminal'
def check_block_inside (block_location):

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

    'Check whether all points of the container block is inside the terminal'
    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

    """Algorithm for the case : There is possibility for : 
    A  container block can be placed in the space on the x- direction

    But, this is an exception for the first container block, because the algorithm should not be repeated
    This exception is indicated by the parameter : m"""

    'Generating blocks in bay direction'
    if point_0_inside is True and point_1_inside is True and point_2_inside is True and point_3_inside is True:
        'Define that it is possible to place on the next container block in bay direction'
        possible_placement = True

        if block_location[0][0] == starting_origin[0] and block_location[0][1] == starting_origin[1] and m == 0:

            m = m + 1

            'Define the points that needs to be checked'
            check_point = [[block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1]],
                           [block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1] + block_width]]

            'Check whether the check points is inside the terminal'
            check_point_inside = check_point_inside_com(check_point)

            'If the check points is INSIDE the terminal, then it is POSSIBLE to have a FULL container block in the space on x-direction'
            if check_point_inside is True:
                while check_point_inside is True:
                    'Define new current_origin location'
                    current_origin = [check_point[0][0], check_point[0][1]]

                    'Determine the new block location'
                    block_location[0] = [current_origin[0], current_origin[1]]
                    block_location[1] = [current_origin[0], current_origin[1] + block_width]
                    block_location[2] = [current_origin[0] + block_length, current_origin[1] + block_width]
                    block_location[3] = [current_origin[0] + block_length, current_origin[1]]
                    block_location[4] = [current_origin[0], current_origin[1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                    'Define the points that needs to be checked'
                    check_point = [[block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1]],
                                   [block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1] + block_width]]

                    'Check whether the check points is inside the terminal'
                    check_point_inside = check_point_inside_com(check_point)

                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                check_point = [[block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1]],
                               [block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1] + block_width]]

                check_point_inside = check_point_inside_com(check_point)

                if check_point_inside is True:
                    'Check whether it is possible to INCREASE the block length in x- direction'
                    'Algorithm for : Increasing the block length until it reaches the edge of the terminal in x- direction'
                    while point_0_inside is True and point_1_inside is True:
                        current_origin = [current_origin[0] - rtg_gross_tgs_x, current_origin[1]]

                        'Determine the new block location'
                        block_location[0] = [current_origin[0], current_origin[1]]
                        block_location[1] = [current_origin[0], current_origin[1] + block_width]
                        block_location[4] = [current_origin[0], current_origin[1]]

                        'Determine new all points of the container block'
                        block_location = [block_location[0],
                                          block_location[1],
                                          block_location[2],
                                          block_location[3],
                                          block_location[4]]

                        'Check whether all points of the container block is inside the terminal'
                        point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                    'Determine the location after the while loop: Move the current origin by 1 container'
                    current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                    'Determine the new block location'
                    block_location[0] = [current_origin[0], current_origin[1]]
                    block_location[1] = [current_origin[0], current_origin[1] + block_width]
                    block_location[2] = [block_location[2][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[2][1]]
                    block_location[3] = [block_location[3][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[3][1]]
                    block_location[4] = [current_origin[0], current_origin[1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                    return current_origin, possible_placement, block_location, container_location, i, m

                    'If it is NOT POSSIBLE to place a FULL container block on the further row ahead'

                    'If the check points is OUTSIDE the terminal, then it is NOT POSSIBLE to have a FULL container block in the space on x-direction'
            else:
                'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                check_point = [[block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1]],
                               [block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1] + block_width]]

                check_point_inside = check_point_inside_com(check_point)

                'If it is possible to place a container block that fulfill minimum block length requirement'
                if check_point_inside is True:

                    i = i + 1

                    'Check whether it is possible to INCREASE the block length in x- direction'
                    'Algorithm for : Increasing the block length until it reaches the edge of the terminal in x- direction'
                    while point_0_inside is True and point_1_inside is True:
                        current_origin = [current_origin[0] - rtg_gross_tgs_x, current_origin[1]]

                        'Determine the new block location'
                        block_location[0] = [current_origin[0], current_origin[1]]
                        block_location[1] = [current_origin[0], current_origin[1] + block_width]
                        block_location[4] = [current_origin[0], current_origin[1]]

                        'Determine new all points of the container block'
                        block_location = [block_location[0],
                                          block_location[1],
                                          block_location[2],
                                          block_location[3],
                                          block_location[4]]

                        'Check whether all points of the container block is inside the terminal'
                        point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                    'Determine the location after the while loop: Move the current origin by 1 container'
                    current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                    'Determine the new block location'
                    block_location[0] = [current_origin[0], current_origin[1]]
                    block_location[1] = [current_origin[0], current_origin[1] + block_width]
                    block_location[2] = [block_location[2][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[2][1]]
                    block_location[3] = [block_location[3][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[3][1]]
                    block_location[4] = [current_origin[0], current_origin[1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                    return current_origin, possible_placement, block_location, container_location, i, m

        'Draw the container block'
        if block_location[3][0] - block_location[0][0] > min_block_length:
            # Drawing rectangle for the representation of the blocks
            container_block = plt.Rectangle(block_location[0], block_location[3][0] - block_location[0][0], block_width, fc='white', ec="black")
            plt.gca().add_patch(container_block)

            'Calculates number of container in the container block on bay direction'
            number_of_container_bay = math.ceil((block_location[3][0] - block_location[0][0]) / rtg_gross_tgs_x)

            'Define clearance space for each container'
            container_clearance_x = ((block_location[3][0] - block_location[0][0]) - number_of_container_bay * container_x) / (number_of_container_bay - 1)
            container_clearance_y = rtg_gross_tgs_y - container_y

            'Define new current origin for the algorithm in drawing the TGS'
            container_current_origin = block_location[0][0], block_location[0][1] + rtg_track + rtg_vehicle_track + container_clearance_y / 2

            p = 0
            q = 0

            for p in range (0,number_of_container_row):
                for q in range (0, number_of_container_bay):
                    'Draw the container'
                    # container = plt.Rectangle(container_current_origin, container_x, container_y, fc = "white", ec = "black")
                    # plt.gca().add_patch(container)
                    # above are not active because takes a lot of computational to draw each containers, but it can be activated for visualization

                    'Determine the container location'
                    container_location[0] = [container_current_origin[0], container_current_origin[1]]
                    container_location[1] = [container_current_origin[0], container_current_origin[1] + container_y]
                    container_location[2] = [container_current_origin[0] + container_x, container_current_origin[1] + container_y]
                    container_location[3] = [container_current_origin[0],+ container_x, container_current_origin[1]]
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
                    container_current_origin = container_current_origin[0] + container_x + container_clearance_x, container_current_origin[1]

                'Move container to the next location'
                q = 0
                container_current_origin = block_location[0][0] , container_current_origin[1] + container_y + container_clearance_y

            'Add the current block location to the block_list'
            block_list.append(block_location)

        'Move the current origin to the next block in the bay direction'
        current_origin[0] = block_location[3][0] + rtg_traffic_lane + 2 * rtg_margin_stack

        'Determine all new points of the container block'
        block_location = [[current_origin[0], current_origin[1]],
                          [current_origin[0], current_origin[1] + block_width],
                          [current_origin[0] + block_length, current_origin[1] + block_width],
                          [current_origin[0] + block_length, current_origin[1]],
                          [current_origin[0], current_origin[1]]]

    else:
        """        
        Algorithm for the case : Container cannot place a new container block in bay direction, it moves the current_origin to the location of the new container block in row direction
        If block_location[1] and block_location[2] is outisde of the terminal --> for rectangular case'
        If block_location[1] and block_location [2] and block_location [3] is outisde of the terminal --> for triangular & trapezoidal case
        If block_location[0] and block location[2] and block_location[3] is outside of the terminal --> for reversed triangular & trapezoidal case
        """

        if (point_1_inside is False and point_2_inside is False) or (point_1_inside is False and point_2_inside is False and point_3_inside is False) or (point_0_inside is False and point_2_inside is False and point_3_inside is False):
            'Define that it is possible to place on the next container block in bay direction'
            possible_placement = False

            'Define new current_origin point to the next container block in row direction'
            current_origin = [block_list[i][0][0], current_origin[1] + block_width + rtg_bypass_lane]

            'Determine the new block location on the new row direction'
            block_location[0] = [block_list[i][0][0], current_origin[1]]
            block_location[1] = [block_list[i][1][0], current_origin[1] + block_width]
            block_location[2] = [block_list[i][2][0], current_origin[1] + block_width]
            block_location[3] = [block_list[i][3][0], current_origin[1]]
            block_location[4] = [block_list[i][0][0], current_origin[1]]

            'Determine new all points of the container block'
            block_location = [block_location[0],
                              block_location[1],
                              block_location[2],
                              block_location[3],
                              block_location[4]]

            'Check whether all pointsthe point in block is inside the terminal'
            point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            """The coding below this row, is the coding in determining the container block 
            after it moves to the new container block location in row direction
            
            The x-location of the new container block is the same as the previous row
            Therefore, it needs to be checked wether a container block can be placed in this location"""

            'If the container block cannot be placed at all at this location (block_location[0] and block_location[1] and block_location[2] is outside the terminal'
            if point_0_inside is False and point_1_inside is False and point_2_inside is False:

                'Define new current_origin on the next container block in bay direction'
                current_origin[0] = block_location[3][0] + rtg_traffic_lane + 2 * rtg_margin_stack

                'Define new value of i, to indicate the starting point for the algorithm in generating new container block in row direction'
                i = i + 1

                'Determine all new points of the container block'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_width],
                                  [current_origin[0] + block_length, current_origin[1] + block_width],
                                  [current_origin[0] + block_length, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether all points of the container block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                    block_location)

                """The algorithm for the case of moving current_origin to the next container block in bay direction ends here
                Next is the algorithm in defining container block location"""

            # Moving current origin to the left to check whether there is a space to place the block

            """Algorithm for the case : There is possibility for : 
            (a) A full container block (with full block length) can be placed in the space on the x-direction
            (b) The container block length can be INCREASED to the x-direction
            
            It happens if block_location[0] and block_location[1] is inside the terminal"""
            if point_0_inside is True and point_1_inside is True:

                'Check for possibility of (a)'
                'Define the points that needs to be checked'
                check_point = [[block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1]],
                               [block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1] + block_width]]

                'Check whether it is actually possible to place a full container block on the further row ahead'
                'A new container block might be possible to be placed in the space on x- direction'

                'If It is POSSIBLE to place a FULL container block on the further row ahead'
                if min(x) <= check_point[0][0]:
                    'Define the points that needs to be checked'
                    check_point = [[block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1]],
                                   [block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1] + block_width]]

                    'Check whether the check points is inside the terminal'
                    check_point_inside = check_point_inside_com(check_point)

                    'If the check points is INSIDE the terminal, then it is POSSIBLE to have a FULL container block in the space on x-direction'
                    if check_point_inside is True:
                        while check_point_inside is True:

                            'Define new current_origin location'
                            current_origin = [check_point[0][0], check_point[0][1]]

                            'Determine the new block location'
                            block_location[0] = [current_origin[0], current_origin[1]]
                            block_location[1] = [current_origin[0], current_origin[1] + block_width]
                            block_location[2] = [current_origin[0] + block_length, current_origin[1] + block_width]
                            block_location[3] = [current_origin[0] + block_length, current_origin[1]]
                            block_location[4] = [current_origin[0], current_origin[1]]

                            'Determine new all points of the container block'
                            block_location = [block_location[0],
                                              block_location[1],
                                              block_location[2],
                                              block_location[3],
                                              block_location[4]]

                            'Check whether all points of the container block is inside the terminal'
                            point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                            'Define the points that needs to be checked'
                            check_point = [[block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1]],
                                           [block_location[0][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[0][1] + block_width]]

                            'Check whether the check points is inside the terminal'
                            check_point_inside = check_point_inside_com(check_point)

                        'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                        check_point = [[block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1]],
                                       [block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1] + block_width]]

                        check_point_inside = check_point_inside_com(check_point)

                        if check_point_inside is True:
                            'Check whether it is possible to INCREASE the block length in x- direction'
                            'Algorithm for : Increasing the block length until it reaches the edge of the terminal in x- direction'
                            while point_0_inside is True and point_1_inside is True:
                                current_origin = [current_origin[0] - rtg_gross_tgs_x, current_origin[1]]

                                'Determine the new block location'
                                block_location[0] = [current_origin[0], current_origin[1]]
                                block_location[1] = [current_origin[0], current_origin[1] + block_width]
                                block_location[4] = [current_origin[0], current_origin[1]]

                                'Determine new all points of the container block'
                                block_location = [block_location[0],
                                                  block_location[1],
                                                  block_location[2],
                                                  block_location[3],
                                                  block_location[4]]

                                'Check whether all points of the container block is inside the terminal'
                                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                            'Determine the location after the while loop: Move the current origin by 1 container'
                            current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                            'Determine the new block location'
                            block_location[0] = [current_origin[0], current_origin[1]]
                            block_location[1] = [current_origin[0], current_origin[1] + block_width]
                            block_location[2] = [block_location[2][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[2][1]]
                            block_location[3] = [block_location[3][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[3][1]]
                            block_location[4] = [current_origin[0], current_origin[1]]

                            'Determine new all points of the container block'
                            block_location = [block_location[0],
                                              block_location[1],
                                              block_location[2],
                                              block_location[3],
                                              block_location[4]]

                            'Check whether all points of the container block is inside the terminal'
                            point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                            return current_origin, possible_placement, block_location, container_location, i, m

                            'If it is NOT POSSIBLE to place a FULL container block on the further row ahead'

                            'If the check points is OUTSIDE the terminal, then it is NOT POSSIBLE to have a FULL container block in the space on x-direction'
                    else:
                        'Check whether it is possible to place a container block that fulfill minimum block length requirement'
                        check_point = [[block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1]],
                                       [block_location[0][0] - rtg_traffic_lane - min_block_length, block_location[0][1] + block_width]]

                        check_point_inside = check_point_inside_com(check_point)

                        'If it is possible to place a container block that fulfill minimum block length requirement'
                        if check_point_inside is True:

                            'Check whether it is possible to INCREASE the block length in x- direction'
                            'Algorithm for : Increasing the block length until it reaches the edge of the terminal in x- direction'
                            while point_0_inside is True and point_1_inside is True:
                                current_origin = [current_origin[0] - rtg_gross_tgs_x, current_origin[1]]

                                'Determine the new block location'
                                block_location[0] = [current_origin[0], current_origin[1]]
                                block_location[1] = [current_origin[0], current_origin[1] + block_width]
                                block_location[4] = [current_origin[0], current_origin[1]]

                                'Determine new all points of the container block'
                                block_location = [block_location[0],
                                                  block_location[1],
                                                  block_location[2],
                                                  block_location[3],
                                                  block_location[4]]

                                'Check whether all points of the container block is inside the terminal'
                                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                            'Determine the location after the while loop: Move the current origin by 1 container'
                            current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                            'Determine the new block location'
                            block_location[0] = [current_origin[0], current_origin[1]]
                            block_location[1] = [current_origin[0], current_origin[1] + block_width]
                            block_location[2] = [block_location[2][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[2][1]]
                            block_location[3] = [block_location[3][0] - block_length - 2 * rtg_margin_stack - rtg_traffic_lane, block_location[3][1]]
                            block_location[4] = [current_origin[0], current_origin[1]]

                            'Determine new all points of the container block'
                            block_location = [block_location[0],
                                              block_location[1],
                                              block_location[2],
                                              block_location[3],
                                              block_location[4]]

                            'Check whether all points of the container block is inside the terminal'
                            point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                            return current_origin, possible_placement, block_location, container_location, i, m

                    'If it is NOT POSSIBLE to place a FULL container block on the further row ahead'
                else:
                    'Check whether it is possible to INCREASE the block length in x- direction'
                    'Algorithm for : Increasing the block length until it reaches the edge of the terminal in x- direction'

                    'Check whether the right side already fulfill the requirments for rtg_safety_clearance'
                    check_point = [[block_location[0][0] - rtg_margin_stack, block_location[0][1]],
                                   [block_location[0][0] - rtg_margin_stack, block_location[0][1] + block_width]]

                    check_point_inside = check_point_inside_com(check_point)

                    while point_0_inside is True and point_1_inside is True and check_point_inside is True:
                        current_origin = [current_origin[0] - rtg_gross_tgs_x, current_origin[1]]

                        'Determine the new block location'
                        block_location[0] = [current_origin[0], current_origin[1]]
                        block_location[1] = [current_origin[0], current_origin[1] + block_width]
                        block_location[2] = [block_list[i][2][0], current_origin[1] + block_width]
                        block_location[3] = [block_list[i][3][0], current_origin[1]]
                        block_location[4] = [current_origin[0], current_origin[1]]

                        'Determine new all points of the container block'
                        block_location = [block_location[0],
                                          block_location[1],
                                          block_location[2],
                                          block_location[3],
                                          block_location[4]]

                        'Check whether all points of the container block is inside the terminal'
                        point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                        'Check whether the right side already fulfill the requirments for rtg_safety_clearance'
                        check_point = [[block_location[0][0] - rtg_margin_stack, block_location[0][0]],
                                       [block_location[0][0] - rtg_margin_stack, block_location[0][0] + block_width]]

                        check_point_inside = check_point_inside_com(check_point)

                    'Determine the location after the while loop: Move the current origin by 1 container'
                    current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                    'Determine the new block location'
                    block_location[0] = [current_origin[0], current_origin[1]]
                    block_location[1] = [current_origin[0], current_origin[1] + block_width]
                    block_location[2] = [block_list[i][2][0], current_origin[1] + block_width]
                    block_location[3] = [block_list[i][3][0], current_origin[1]]
                    block_location[4] = [current_origin[0], current_origin[1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                    return current_origin, possible_placement, block_location, container_location, i, m

            'Algorithm for the case : Cannot place a new container block, because it already reaches outside of the terminal'
            if point_1_inside is False and point_2_inside is False:
                return current_origin, possible_placement, block_location, container_location, i, m

            """Algorithm for the case : There is possibility for : 
            (a) The container block length should be DECREASED to the x+ direction in order to place the container block
            (b) The decreasing container block starts on the LEFT side of the container block
            
            It happens if block_location[0] or block_location[1] is outside the terminal"""
            if point_0_inside is False or point_1_inside is False:

                'Algorithm for : Decreasing the block length until it reaches the edge of the terminal in x+ direction'
                while point_0_inside is False or point_1_inside is False:

                    current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                    'Determine the new block location'
                    block_location[0] = [current_origin[0], current_origin[1]]
                    block_location[1] = [current_origin[0], current_origin[1] + block_width]
                    block_location[2] = [block_list[i][2][0], current_origin[1] + block_width]
                    block_location[3] = [block_list[i][3][0], current_origin[1]]
                    block_location[4] = [current_origin[0], current_origin[1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

                return current_origin, possible_placement, block_location, container_location, i, m

        'Algorithm for anomaly condition where the block_location[3][0] is less than block_location[0][0]'
        if block_location[3][0] < block_location[0][0]:

            possible_placement = False

            current_origin[0] = block_location[3][0] + rtg_traffic_lane + 2 * rtg_margin_stack

            block_location = [[current_origin[0], current_origin[1]],
                              [current_origin[0], current_origin[1] + block_width],
                              [current_origin[0] + block_length, current_origin[1] + block_width],
                              [current_origin[0] + block_length, current_origin[1]],
                              [current_origin[0], current_origin[1]]]

            point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                block_location)

            i = i + 1

            if point_0_inside is False or point_1_inside is False:
                while point_0_inside is False or point_1_inside is False:
                    current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                    block_location = [[current_origin[0], current_origin[1]],
                                      [current_origin[0], current_origin[1] + block_width],
                                      [block_list[i][2][0], current_origin[1] + block_width],
                                      [block_list[i][3][0], current_origin[1]],
                                      [current_origin[0], current_origin[1]]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                        block_location)

            if point_1_inside is False and point_2_inside is False:
                possible_placement = False
                return current_origin, possible_placement, block_location, container_location, i, m

        """
            Algorithm for the (special) case : Reversed triangular
            If block_location[0] and block_location[1] is outside the terminal --> reversed triangular case
        """

        if point_0_inside is False or point_1_inside is False:
            while point_0_inside is False or point_1_inside is False:

                current_origin = [current_origin[0] + rtg_gross_tgs_x, current_origin[1]]

                'Determine the new block location'
                block_location[0] = [current_origin[0], current_origin[1]]
                block_location[1] = [current_origin[0], current_origin[1] + block_width]
                block_location[2] = block_location[2]
                block_location[3] = block_location[3]
                block_location[4] = [current_origin[0], current_origin[1]]

                'Determine new all points of the container block'
                block_location = [block_location[0],
                                  block_location[1],
                                  block_location[2],
                                  block_location[3],
                                  block_location[4]]

                'Check whether all points of the container block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(block_location)

            """The algorithm for the case of moving current_origin to the next container block in bay direction ends here
            Next is the algorithm in defining container block location"""

            possible_placement = True

            return current_origin, possible_placement, block_location, container_location, i, m

        if point_0_inside is True and point_1_inside is True and point_2_inside is True and point_3_inside is True:
            return current_origin, possible_placement, block_location, container_location, i, m

        else:
            """Algorithm for the case : There is possibility for : 
            (a) The container block length can be DECREASED to the x- direction in order to place the container block
            (b) The decreasing container block starts on the RIGHT side of the container block
            
            It happens if block_location[0] or block_location[1] is outside the terminal"""

            'Check whether it is possible to place a container block that fulfill minimum block length requirement'
            'If it is POSSIBLE to fulfill minimum block length requirement'
            if block_location[3][0] - block_location[0][0] > min_block_length:

                'Check whether the right side already fulfill the requirments for rtg_safety_clearance'
                check_point = [[block_location[3][0] + rtg_margin_stack, block_location[3][1]],
                               [block_location[3][0] + rtg_margin_stack, block_location[3][1] + block_width]]

                check_point_inside = check_point_inside_com(check_point)

                'Algorithm for : Decreasing the block length until it reaches the edge of the terminal in x- direction'
                while (point_2_inside is False or point_3_inside is False) and check_point_inside is False:

                    'Determine the new block location'
                    block_location[0] = [current_origin[0], current_origin[1]]
                    block_location[1] = [current_origin[0], current_origin[1] + block_width]
                    block_location[2] = [block_location[2][0] - rtg_gross_tgs_x, current_origin[1] + block_width]
                    block_location[3] = [block_location[3][0] - rtg_gross_tgs_x, current_origin[1]]
                    block_location[4] = [current_origin[0], current_origin[1]]

                    'Determine new all points of the container block'
                    block_location = [block_location[0],
                                      block_location[1],
                                      block_location[2],
                                      block_location[3],
                                      block_location[4]]

                    'Check whether all points of the container block is inside the terminal'
                    point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                        block_location)

                    'Check whether the right side already fulfill the requirments for rtg_safety_clearance'
                    check_point = [[block_location[3][0] + rtg_margin_stack, block_location[3][1]],
                                   [block_location[3][0] + rtg_margin_stack, block_location[3][1] + block_width]]

                    check_point_inside = check_point_inside_com(check_point)

            else:
                'If it is NOT POSSIBLE to fulfill minimum block length requirement'
                'Define that it is possible to place on the next container block in bay direction'
                possible_placement = False

                'Determine the new location for current_origin and block_location'
                current_origin [0] = block_location[3][0] + rtg_traffic_lane + 2 * rtg_margin_stack

                'Determine the new block location'
                block_location = [[current_origin[0], current_origin[1]],
                                  [current_origin[0], current_origin[1] + block_width],
                                  [current_origin[0] + block_length, current_origin[1] + block_width],
                                  [current_origin[0] + block_length, current_origin[1]],
                                  [current_origin[0], current_origin[1]]]

                'Check whether all points of the container block is inside the terminal'
                point_0_inside, point_1_inside, point_2_inside, point_3_inside, block_location = check_block_inside(
                    block_location)

                return current_origin, possible_placement, block_location, container_location, i, m

            if current_origin[0] == block_list[0][0][0] :
                possible_placement = True

            else :
                possible_placement = True

    return current_origin, possible_placement, block_location, container_location, i, m