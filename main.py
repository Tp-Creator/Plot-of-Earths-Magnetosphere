import os
from datetime import datetime
import json

import numpy as np
from geopack import geopack

import coordinate_system

# import matplotlib.pyplot as plt
# from concurrent import futures


# Enters the directory where the program is run
abspath = os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

dt_obj = datetime.strptime('2016-03-11 12:46:10', '%Y-%m-%d %H:%M:%S')

# The number of seconds since 1970-01-01 00:00:00
ut = dt_obj.timestamp()


geopack.recalc(ut, vxgse=-400, vygse=0, vzgse=0)

PARMOD = [
    5,   # solar wind pressure pdyn (nanopascals)
    0,   # dst (nanotesla)
    0,   # byimf (nanotesla)
    2,   # bzimf (nanotesla)
]



def isfloat(string:str) -> bool:
    """Checks if string can be converted to float.

    Args:
        string (str): string to be checked.

    Returns:
        bool: True: can be converted to float. 
    """
    
    return string.replace(".", "", 1).isnumeric()


def numericQuestion(msg, max=None, min=0, accept_float=False, accept_None=False, li=None, err=None):
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
        min = 0
        max = len(li)-1     # Kompenserar för len()
        for i in range(len(li)):
            alt += f"({i}) {li[i]}\n"       #   Ger varje alternativ ett index och skriver ut alternativet

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
            
        if isfloat(num):            
            if max is not None and (max < float(num) or min > float(num)):
                pass
            elif max is None and min > float(num):
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



#// TODO Flytta ut ritandet och returnera enbart listor med koordinaterna
# Draws [amount] field lines from diffrent places around the earth equaly far from each other
def field_line_group(amount:int, color:str="#000000"):

    # calcualtes differnet places around the earth in radians    
    radians = np.arange(0, np.pi*2, np.pi*2/amount)

    calculated_field_lines = []

    # calculates each field line using sin and cos of every angle in two axis
    for i, angle in enumerate(radians, 1):
        dir = 1 if np.sin(angle) > 0 else -1
        
        data = geopack.trace(xi=np.cos(angle),
                             yi=0,
                             zi=np.sin(angle),
                             dir=dir,
                             rlim=60,
                             r0=0.99,
                             parmod=PARMOD,
                             exname="t96",
                             inname="igrf",
                             maxloop=4000)

        # The data is stored in separate variables. Each variable is a list of all coordinates in that axis.
        # They are functions of the list index. x[i], y[i] and z[i] are one position on the field line.
        x, y, z = data[3:6]
        
        # Saves the calculated field line to be returned
        calculated_field_lines.append({"pos": [list(x), list(y), list(z)], "color": color})

        #* Debug - prints the angle just calculated and amount of coordinates.
        print(angle, ":\n", len(data[3]), ":\n")
        print(f"{i} / {amount}")
        
    return calculated_field_lines


# TODO will be for adding a new field line to the plot
def new_calculation():
    # window = coordinate_system.setup_environment(
    #     xscale=20,
    #     yscale=20,
    #     win_xwidth=1.0,
    #     win_ywidth=0.9,
    #     canvas_xwidth=12000,
    #     canvas_ywidth=3000
    # )

    # XZ = coordinate_system.Coordinate_system(window=window, x=-115, y=0, xmin=-50, xmax=20, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="x_GSM (Re)", vertical_name="z_GSM (Re)")
    # XY = coordinate_system.Coordinate_system(window=window, x=20, y=0, xmin=-50, xmax=20, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="x_GSM (Re)", vertical_name="y_GSM (Re)")
    # YZ = coordinate_system.Coordinate_system(window=window, x=115, y=0, xmin=-25, xmax=25, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="y_GSM (Re)", vertical_name="z_GSM (Re)")

    # XZ.prepare_workspace()
    # XY.prepare_workspace()
    # YZ.prepare_workspace()

    # field_lines = field_line_group(36, XZ, XY, YZ)
    # print("all drawn!\n")
    
    ### Temporary ###        ######         #####
    data = geopack.trace(xi=0.14,
                             yi=0.04,
                             zi=1.12,
                             dir=1,
                             rlim=60,
                             r0=0.99,
                             parmod=PARMOD,
                             exname="t96",
                             inname="igrf",
                             maxloop=4000)

    # The data is stored in separate variables. Each variable is a list of all coordinates in that axis.
    # They are functions of the list index. x[i], y[i] and z[i] are one position on the field line.
    x, y, z = data[3:6]

    return {"pos": [list(x), list(y), list(z)], "color": color}

    # Draws the field lines
    XZ.draw_field_line(x, z, "#aa0000")
    XY.draw_field_line(x, y, "#aa0000")
    YZ.draw_field_line(y, z, "#aa0000")
    #######             ######              #####
    

def save_to_file(field_lines):
    # Saves the field lines to file
    with open(f"saved_field_lines/{str(datetime.now()).replace(':', '_')}.json", "w") as file:
        json.dump(field_lines, file, indent=3)


def load_from_file():
    saves = os.listdir("saved_field_lines")
    choice = numericQuestion("Which file do you want to load?", li=saves)
    
    chosen_file = f"saved_field_lines/{saves[choice]}"
    
    with open(chosen_file, "r") as file:
        field_lines = json.load(file)
        
        return field_lines
    
    
def change_window_settings(window_settings):
    print("Change the settings for the windows. Type the same value to keep it.")
    for key in window_settings:
        if type(window_settings[key]) is float:
            pass
        else:
            temp = numericQuestion(f"{key}, current: {window_settings[key]}: ", accept_None=True)
            
            if temp is not None:
                window_settings[key] = temp
        
    print("These are the new settings:")
    for key in window_settings:
        print(f"{key}: {window_settings[key]}")
        # window.key = window_settings[key]
        
        
    return window_settings
    
    
def create_coordinate_systems(window):

    # if Daniel or Joel in computer_users:
    #    if windows == True:
    #        del(system32)

    # Create coordinate system objects
    XZ = coordinate_system.Coordinate_system(
        window=window,
        x=-115,
        y=0,
        xmin=-50,
        xmax=20,
        ymin=-25,
        ymax=25,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="x_GSM (Re)",
        vertical_name="z_GSM (Re)"
    )
    
    XY = coordinate_system.Coordinate_system(
        window=window,
        x=20,
        y=0,
        xmin=-50,
        xmax=20,
        ymin=-25,
        ymax=25,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="x_GSM (Re)",
        vertical_name="y_GSM (Re)"
    )
    
    YZ = coordinate_system.Coordinate_system(
        window=window,
        x=115,
        y=0, 
        xmin=-25,
        xmax=25,
        ymin=-25,
        ymax=25,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="y_GSM (Re)",
        vertical_name="z_GSM (Re)"
    )
    
    return XZ, XY, YZ
    

#// TODO flytta ned skapandet av variabler
#// TODO Ta bort main() för det finns inget egentligt syfte med den
#// TODO Gör så att man kan rita om med hjälp av de gamla värdena.
# TODO Lägg till möjlighet att rita ut ytterligare fältlinjer (för satellit)
    # TODO Om man laddar in från fil, så ska man hämta parametrarna för det tillfället
        # TODO Spara parametrarna till fil.
        # TODO Ladda parametrar från fil.
#// TODO Tillåt att man sparar ned beräknade värden till fil
#// TODO Tillåt att man kan rita fältlinjer sparade i fil istället för att beräkna nya.

#// TODO Lägg till mindre linjer mellan de större i koordinat systemet.
#// TODO FLytta titeln på axlarna till att vara utanför rektanglarna. (vertikal text för vertikal axel)
# TODO Implementera möjligheten att vända på axlarna så att de går åt andra håll
# TODO färglägg nattsidan av Jorden för att indikera var solen är.

### Default Values for the window
window_settings = {
    "xscale": 7,
    "yscale": 7,
    "win_xwidth": 1.0,
    "win_ywidth": 0.9,
    "canvas_xwidth": 12000,
    "canvas_ywidth": 3000
}
###


# Select what to do
option = numericQuestion(
    "What do you want to do?",
    li=[
        "Quit and exit program",
        "Load old calculation from file",
        "New Calculation"]
)

if option == 0:
    exit()
elif option == 1:
    field_lines = load_from_file()
elif option == 2:
    field_lines = field_line_group(numericQuestion("how many field lines?"))
    # break
else:
    print("Something went wrong with choosing option!")

# Create drawing space
window = coordinate_system.setup_environment(**window_settings)

while True:
    
    # Create and Draw coordinatesystems (prapare for drawing the plot)
    # print(window_settings)

    # Creates the the coordinate system objects
    print(window)
    XZ, XY, YZ = create_coordinate_systems(window)

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
        
    # coordinate_system.update_screen()
    
    
    if option not in [1, 4, 5] and input("Do you want to save the calculated field lines for future rendering? (Y/n)") not in ["n", "N"]:
        print("saving... (to be implemented)")
        save_to_file(field_lines)
    
    option = numericQuestion(
        "What to do next?",
        li=[
            "Quit and exit program",
            "Change coordinate system scale",
            "Add field line",
            "New Calculation",
            "Load old calculation from file",
            "Save calculations to file (if you forgot to do it)"]
    )

    if option == 0:
        break
        field_lines = field_line_group(numericQuestion("how many field lines?", max=100))
    elif option == 1:
        # window_settings = change_window_settings(window_settings)
        # window = change_window_settings(window, window_settings)
        window_settings = change_window_settings(window_settings)
        window = coordinate_system.modify_environment(window, window_settings)
    elif option == 2:
        field_line = new_calculation()
        # break
    else:
        print("Something went wrong with choosing option!")

    window.clear()
    window.tracer(0, 0)     # Is needed since when to update is also cleared 
    # print("cleard screen")
    

    # Kill the window before either creating a new or quitting the program 
    # try:
    #     window.bye()
    # except:
    #     print("Turtle window was already killed!")


# Kill the window before quitting the program 
try:
    window.bye()
except:
    print("Turtle window was already killed!")

exit()