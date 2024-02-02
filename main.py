import os
from datetime import datetime
import json

import numpy as np
from geopack import geopack

import coordinate_system


# Enters the directory where the program is run
abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))


# Function to clear the console
clear = lambda: os.system('cls')


def remove_chars(string:str, chars:str):
    for char in chars:
        string = string.replace(char, "")
        
    return string
    

def isfloat(string:str) -> bool:
    """Checks if string can be converted to float.

    Args:
        string (str): string to be checked.

    Returns:
        bool: True: can be converted to float. 
    """
    
    # if the number is negative - isnumeric doesn't handle negative numbers
    if len(string) > 0 and string[0] == "-":
        string = string[1:]
    
    return string.replace(".", "", 1).isnumeric()


def choose_color(default):
    color = input("\nWhat color do you want your field_line to be in? (ex format: #ff00aa)\nIf invalid format red will be used.\ncolor: ")
    
    # test if color is valid
    if len(color) == 7 and color[0] == "#" and remove_chars(color, "0123456789abcdefABCDEF ") == "#":
        print("Color was valid.")
        return color
    
    else:
        print("Color was invalid, changing to default...")
        return default
        

def numericQuestion(msg, max=None, min=0, accept_float=False, accept_None=False, unacceptable=[], li=None, err=None):
    """En input som bara accepterar att man skriver in integers alternativt float mellan max och min
    Om man lägger till li som argument skrivs max och min över och vi skriver
    ut alla alternativen som finns i listan istället, och utgår ifrån det för max och min
    Man kan även lägga till felmeddelande om användaren skrev fel (annars default)
    Msg är frågan användaren får

    Args:
        msg (_type_): Question to be propted to the user.
        max (_type_, optional): The highest float the user can answer. Defaults to None.
        min (int, optional): The lowest float a user can answer. Defaults to 0.
        accept_float (bool): If true the function can return floats between max and min.
        li (list): If set the function will use every element in the list as the alternatives for the user to choose from. Defaults to None.
        err (str): Error message to the user if the answer is not accepted. Defaults to None.

    Returns:
        int | float: returns the value chosen by the user.
    """
    alt = "\n"      #   Alternativ - \n för att jag skriver ut hela frågan i en input

    if li != None:  # När vi fått en lista som argument vill vi använda den som alternativ
        if min == None:
            min = 0
        max = len(li)-1+min     # Kompenserar för len()
        for i in range(len(li)):
            alt += f"({i+min}) {li[i]}\n"       #   Ger varje alternativ ett index och skriver ut alternativet

    # Kollar om vi fått ett error message som argument
    if err is not None:
        errMsg = err
    else:
        errMsg = f"You have to type a numeric value between {min} and {max}"


    num = input("\n"+msg+alt)
    # När jag lägger en condition före de andra så kommer den att kolla det först, och om det inte stämmer
    # Koller den inte en de andra. Detta gör att jag med säkerhet kan köra
    # int(num) utan att få runtime error
    # while not isfloat(num) or float(num) < min or (max != None or float(num) > max):
    while True:      # isfloat() kollar om det är en integer eller inte
        if accept_None is True:
            if num == "":
                break
            else:
                pass
            
        if isfloat(num) and int(float(num)) not in unacceptable:
            if max is not None and (max < float(num) or min > float(num)):
                pass
            elif max is None and min > float(num):
                print("max is None: ", max is None)
                print("min > float(num): ", min > float(num))
                pass
            else:
                break
            
        # ask question again
        print(errMsg)
        num = input(msg+alt)
    
    # enbart om accept_None == True
    if num == "":
        if accept_None is True:
            return None
        else:   # should never happen
            print("Something went wrong choosing number, accepted string...")
            return numericQuestion(msg, max=max, min=min, accept_float=accept_float, accept_None=accept_None, li=accept_None, err=accept_None)

    elif li != None or accept_float is False:
        return int(float(num))
    else:
        return float(num)


# Draws a group of field lines from diffrent places around the earth equaly far from each other
def field_line_group(parmod):

    amount = numericQuestion("how many field lines?")
    maxloop = numericQuestion("MaxLoop (How long field line should we make (amount of itterations))?", 10000)
    color = choose_color("#000000")

    # calcualtes differnet places around the earth in radians    
    radians = np.arange(0, np.pi*2, np.pi*2/amount)

    calculated_field_lines = []

    # calculates each field line using sin and cos of every angle in two axis
    for i, angle in enumerate(radians, 1):
        clear()
        print(f"Calculating field line... \n{i} / {amount}")        # prints out how far we've come in calculating
        dir = 1 if np.sin(angle) > 0 else -1

        data = geopack.trace(xi=np.cos(angle),
                             yi=0,
                             zi=np.sin(angle),
                             dir=dir,
                             rlim=60,
                             r0=0.99,
                             parmod=parmod,
                             exname="t96",
                             inname="igrf",
                             maxloop=maxloop)

        # The data is stored in separate variables. Each variable is a list of all coordinates in that axis.
        # They are functions of the list index. x[i], y[i] and z[i] are one position on the field line.
        x, y, z = data[3:6]
        
        # Saves the calculated field line to be returned
        calculated_field_lines.append({"pos": [list(x), list(y), list(z)], "color": color})
        
    return calculated_field_lines


def add_specific_field_line(parmod):
    
    choice = numericQuestion("In what coordinate system format do you want to input the coordinates?", li=["MLT-CGLat", "GSM"], min=1)
    
    if choice == 1:
        mlt = numericQuestion("What is the MLT?", min=0, max=24, accept_float=True)
        CGLat = numericQuestion("What is the MLat?", min=0, max=180, accept_float=True)
        xi, yi, zi = MLT_MLat_to_GSM(mlt, CGLat)
    elif choice == 2:
        xi = numericQuestion("What will be the start X coordinate?", min=-100, accept_float=True)
        yi = numericQuestion("What will be the start Y coordinate?", min=-100, accept_float=True)
        zi = numericQuestion("What will be the start Z coordinate?", min=-100, accept_float=True)
    else:
        print("Something went wrong!")
        
    dir = numericQuestion("In what direction should we calcualte? (1 (north to south (z>0)) or -1 (south to north (z<0)))", 1, -1, unacceptable=[0], err="Only 1 and -1 are accepted")
    maxloop = numericQuestion("MaxLoop (How long field line should we make (amount of itterations))?", 10000)
    color = choose_color("#ff0000")
    
    print("\nCalculating...")
    
    # A satellite
    # xi=0.14,
    # yi=0.04,
    # zi=1.12,
    # dir = 1
    
    data = geopack.trace(xi=xi,
                         yi=yi,
                         zi=zi,
                         dir=dir,
                         rlim=60,
                         r0=0.99,
                         parmod=parmod,
                         exname="t96",
                         inname="igrf",
                         maxloop=maxloop)

    # The data is stored in separate variables. Each variable is a list of all coordinates in that axis.
    # They are functions of the list index. x[i], y[i] and z[i] are one position on the field line.
    x, y, z = data[3:6]

    return {"pos": [list(x), list(y), list(z)], "color": color}
    

def save_to_file(field_lines, parmod, recalc):
    # Saves the field lines to file
    
    data = {
        "parameters": {
            "parmod": parmod,
            "recalc": recalc
        },
        
        "coordinates": field_lines
    }
    
    with open(f"saved_field_lines/{str(datetime.now()).replace(':', '_')}.json", "w") as file:
        json.dump(data, file, indent=3)


def load_from_file(parmod, recalc_values):
    saves = os.listdir("saved_field_lines")
    choice = numericQuestion("Which file do you want to load?", li=saves, min=1)
    
    chosen_file = f"saved_field_lines/{saves[choice-1]}"
    
    with open(chosen_file, "r") as file:
        data = json.load(file)
        
        field_lines = data["coordinates"]
        parmod = data["parameters"]["parmod"]
        recalc_values = data["parameters"]["recalc"]
        
        # recalculate the model according to the time of the loaded data.
        geopack.recalc(**recalc_values)
        
        return field_lines, parmod, recalc_values
    
    
def change_window_settings(window_settings):
    print("Change the settings for the windows. Type the same value to keep it.")
    for key in window_settings:
        # if type(window_settings[key]) is float:
        if key in ["win_xwidth", "win_ywidth"]:
            pass
        else:
            temp = numericQuestion(f"{key}, current: {window_settings[key]}: ", accept_None=True)
            
            if temp is not None:
                window_settings[key] = temp

    print("These are the new settings:")
    for key in window_settings:
        if key in ["win_xwidth", "win_ywidth"]:
            continue
        print(f"{key}: {window_settings[key]}")
        # window.key = window_settings[key]
        
        
    return window_settings
    
    
def create_coordinate_systems(window):
    # Create coordinate system objects
    XZ = coordinate_system.Coordinate_system(
        window=window,
        x=-120,
        y=0,
        xmin=-60,
        xmax=20,
        ymin=-30,
        ymax=30,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="x_GSM (Re)",
        vertical_name="z_GSM (Re)",
        horizontal_dir=-1
    )
    
    XY = coordinate_system.Coordinate_system(
        window=window,
        x=0,
        y=0,
        xmin=-60,
        xmax=20,
        ymin=-30,
        ymax=30,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="x_GSM (Re)",
        vertical_name="y_GSM (Re)",
        horizontal_dir=-1,
        vertical_dir=-1
    )
    
    YZ = coordinate_system.Coordinate_system(
        window=window,
        x=100,
        y=0, 
        xmin=-30,
        xmax=30,
        ymin=-30,
        ymax=30,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="y_GSM (Re)",
        vertical_name="z_GSM (Re)"
    )

    return XZ, XY, YZ


# Converts MLT and (M)Latitude to GSM coordinates
def MLT_MLat_to_GSM(MLT, MLat, r=1):
    # Converts MLat in deg to theta in rad
    theta = (90 - MLat) * (np.pi/180)

    # Converts MLT time to Longitud in rad 24h = 2pi = one lap around the earth.
    phi = ((MLT-12) * 15.0) * (np.pi/180)
    
    # spherical to cartesian
    xsm, ysm, zsm = geopack.sphcar(r, theta, phi, j=1)
    
    # convert sm to gsm
    xgsm, ygsm, zgsm = geopack.smgsm(xsm, ysm, zsm, 1)    
    print("gsm:", xgsm, ygsm, zgsm)
    
    return xgsm, ygsm, zgsm



#? TODO färglägg nattsidan av Jorden för att indikera var solen är.
### Default variable values

    # For the geopack.recalc() function
    # calculates the number of seconds from 1970-01-01 00:00:00 to the datetime below

ut = datetime.strptime('2016-03-11 12:30:00', '%Y-%m-%d %H:%M:%S').timestamp()
# ut = datetime.strptime('2016--1 12:46:40', '%Y--%j %H:%M:%S').timestamp()
print("datetime:", datetime.fromtimestamp(ut))
recalc_values = {
    "ut": ut,
    "vxgse": -376.1,         # Endast "ut" krävs för att köra funktionen geopack.recalc(recalc_values)
    "vygse": -19.0,         # Dessa tre gör ingenting, varför?
    "vzgse": -5.5
}

# res = datetime.strptime(year + "-" + day_num, "%Y-%j").strftime("%m-%d-%Y")

    # Solvind data
parmod = [
    8.99,   # solar wind pressure pdyn (nanopascals)
    12,   # dst (nanotesla)
    -13.25,   # byimf (nanotesla)
    19.3,   # bzimf (nanotesla)
]

geopack.recalc(**recalc_values)


window_settings = {
    "xscale": 7,
    "yscale": 7,
    "win_xwidth": 1.0,
    "win_ywidth": 0.9,
    "canvas_xwidth": 12000,
    "canvas_ywidth": 3000
}

###

# Potensiella fel:
    # När man laddar in så får man inte rätt parmod och recalc_values
        # Recalc_values laddas inte in
    #


# Select what to do
option = numericQuestion(
    "What do you want to do?",
    li=[
        "Quit and exit program",
        "Load old calculation from file",
        "New group calculation"]
)

if option == 0:
    exit()
elif option == 1:
    field_lines, parmod, recalc_values = load_from_file(parmod, recalc_values)
elif option == 2:
    field_lines = field_line_group(parmod)
else:
    print("Something went wrong with choosing option!")

# Create turtle window
window = coordinate_system.setup_environment(**window_settings)


while True:
    # Creates the the coordinate system objects
    XZ, XY, YZ = create_coordinate_systems(window)

    # Draws the coordinatesystems
    XZ.prepare_workspace()
    XY.prepare_workspace()
    YZ.prepare_workspace()

    # Draw the field lines
    # Structure:
    # {
    #     "pos": [list(x), list(y), list(z)], 
    #     "color": "#000000"
    #  }
    for field_line in field_lines:
        x = field_line["pos"][0]
        y = field_line["pos"][1]
        z = field_line["pos"][2]
        color = field_line["color"]

        # Draws the field lines
        XZ.draw_field_line(x, z, color)
        XY.draw_field_line(x, y, color)
        YZ.draw_field_line(y, z, color)


    if option not in [1, 4, 5] and input("Do you want to save the calculated field lines for future rendering? (Y/n)") not in ["n", "N"]:
        print("saving...")
        save_to_file(field_lines, parmod, recalc_values)

    option = numericQuestion(
        "What to do next?",
        li=[
            "Quit and exit program",
            "Change coordinate system scale",
            "Add a specific field line",
            "New group calculation",
            "Load old calculation from file",
            "Save calculations to file (if you forgot to do it)"]
    )

    # Quit and exit program
    if option == 0:
        break
    
    # Change coordinate system scale
    elif option == 1:
        window_settings = change_window_settings(window_settings)
        try:
            window = coordinate_system.modify_environment(window, window_settings)
        except:
            # if the window was closed
            window = coordinate_system.setup_environment(**window_settings)
    
    # Add a specific field line
    elif option == 2:
        field_line = add_specific_field_line(parmod)
        print("adding new field line.")
        field_lines.append(field_line)
    
    # New group calculation
    elif option == 3:
        field_lines = field_line_group(parmod)
        
    # Load old calculation from file
    elif option == 4:
        field_lines, parmod, recalc_values = load_from_file(parmod, recalc_values)
    
    # Save calculations to file (if you forgot to do it)
    elif option == 5:
        save_to_file(field_lines, parmod, recalc_values)
    
    else:
        print("Something went wrong with choosing option!")

    # Cleaning up for new rendering
    try:
        window.clear()          # will fail if the window is closed
        window.tracer(0, 0)     # Is needed since when to update is also cleared 
    except:
        window = coordinate_system.setup_environment(**window_settings)


# Kill the window before quitting the program 
try:
    window.bye()
except:
    print("Turtle window was already killed!")

exit()