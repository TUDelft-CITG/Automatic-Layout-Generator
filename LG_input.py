'(1) Define container dimension'
container_x = 6.1
container_y = 2.44

'(2) Define type of equipment'
equipment_type = input("Please enter the type of equipment in the stacking yard (RTG / RMG / SC / RS): ")

if equipment_type == "RTG" or equipment_type == "RMG" or equipment_type == "SC" or equipment_type == "RS":
    ans_equipment_type = True
else:
    ans_equipment_type = False

while ans_equipment_type is False:
    print("You have input an invalid equipment type.")
    equipment_type = input("Please enter the type of equipment in the stacking yard (RTG / RMG / SC / RS): ")

    if equipment_type == "RTG" or equipment_type == "RMG" or equipment_type == "SC" or equipment_type =="RS":
        ans_equipment_type = True
    else:
        ans_equipment_type = False

'(2) Define apron width'
if equipment_type == "SC":
    apron_width = 66
else:
    apron_width = 62

'(3) Define design rules'
'Define RTG design rules'
if equipment_type == "RTG":
    rtg_track = 1.9
    rtg_vehicle_track = 4.35
    rtg_traffic_lane = 12
    rtg_lightmast_lane = 2.8
    rtg_bypass_lane = 4.2
    rtg_margin_stack = 19.4/2

    rtg_gross_tgs_x = 6.45
    rtg_gross_tgs_y = 2.79

    max_block_length = 250
    min_block_length = 20 * rtg_gross_tgs_x

'Define RMG design rules'
if equipment_type == "RMG":
    rmg_margin_parallel_ori = 2
    rmg_margin_stack = 5
    rmg_track_width = 4
    rmg_length_buffer = 35
    rmg_traffic_lane = 12.9
    rmg_width_buffer = 2.9

    rmg_gross_tgs_x = 2.9
    rmg_gross_tgs_y = 6.7

    max_block_length = 255
    min_block_length = 2 * rmg_length_buffer + 20 * rmg_gross_tgs_y

'Define SC design rules'
if equipment_type == "SC":
    sc_traffic_lane = 20
    sc_margin_stack = 10

    sc_gross_tgs_x = 3.94
    sc_gross_tgs_y = 6.40

    max_block_length = 126
    min_block_length = 10 * sc_gross_tgs_y

    max_block_width = 210
    min_block_width = 20 * sc_gross_tgs_x

'Define RS design rules'
if equipment_type == "RS":
    rs_margin_stack = 6
    rs_traffic_lane = 16
    rs_operating_space = 16.3

    rs_gross_tgs_x = 6.45
    rs_gross_tgs_y = 2.79

    max_block_length = 220
    min_block_length = 20 * rs_gross_tgs_x

'(4) Define number of container row in one block'
if equipment_type == "RTG":
    number_of_container_row = int(input("Please enter the number of container row in a container block (for RTG, it is in range of 4-7): "))

    if number_of_container_row in range (4, 8):
        ans_number_of_container_row = True
    else:
        ans_number_of_container_row = False

    while ans_number_of_container_row is False:
        print("You have input an invalid number of container row in a container block.")
        number_of_container_row = int(input("Please enter the number of container row in a container block (for RTG, it is in range of 4-7): "))

        if number_of_container_row in range(4, 8):
            ans_number_of_container_row = True
        else:
            ans_number_of_container_row = False

if equipment_type == "RMG":
    number_of_container_row = int(input("Please enter the number of container row in a container block (for RMG, it is in range of 6-10): "))

    if number_of_container_row in range (6, 11):
        ans_number_of_container_row = True
    else:
        ans_number_of_container_row = False

    while ans_number_of_container_row is False:
        print("You have input an invalid number of container row in a container block.")
        number_of_container_row = int(input("Please enter the number of container row in a container block (for RMG, it is in range of 6-10): "))

        if number_of_container_row in range(6, 11):
            ans_number_of_container_row = True
        else:
            ans_number_of_container_row = False

if equipment_type == "RS":
    number_of_container_row = int(input("Please enter the number of container row in a container block (for RMG, it is in range of 2-4): "))

    if number_of_container_row in range (2, 5):
        ans_number_of_container_row = True
    else:
        ans_number_of_container_row = False

    while ans_number_of_container_row is False:
        print("You have input an invalid number of container row in a container block.")
        number_of_container_row = int(input("Please enter the number of container row in a container block (for RMG, it is in range of 2-4): "))

        if number_of_container_row in range(2, 5):
            ans_number_of_container_row = True
        else:
            ans_number_of_container_row = False

'(5) Terminal shape and dimensions'
'Define the terminal shape and diension coordinates'
# Rectangular
rectangular = [[0, 0],
          [0,800],
          [1200,800],
          [1200, 0],
          [0, 0]]

# Triangular
triangular = [[0,0],
          [0,900],
          [900,0],
          [0,0]]

# Reversed Triangular
triangular_rev = [[0,0],
          [900,900],
          [900,0],
          [0,0]]

# Small Trapezoidal
trapezoidal_s = [[0, 0],
          [0,300],
          [400,600],
          [800,600],
          [1200,300],
          [1200,0],
          [0,0]]

# Large Trapezoidal
trapezoidal_l = [[0, 0],
          [0,400],
          [600,800],
          [1200,800],
          [1800,400],
          [1800,0],
          [0,0]]

# Small Reverse Trapezoidal
trapezoidal_s_rev = [[0, 0],
          [-400,300],
          [-400,600],
          [800,600],
          [800,300],
          [400,0],
          [0,0]]

# Large  Reverse Trapezoidal
trapezoidal_l_rev = [[0, 0],
          [-600,400],
          [-600,800],
          [1200,800],
          [1200,400],
          [600,0],
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