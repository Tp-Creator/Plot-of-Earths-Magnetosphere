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


def numericQuestion(msg, max=None, min=0, accept_float=False, li=None, err=None):
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
    while not isfloat(num) or float(num) < min or float(num) > max:      # .isnumeric() kollar om det är en integer eller inte
        # if quit is True and num.lower() == "q":
        #     return False
        # clear()
        print(errMsg)
        num = input(msg+alt)

    # Skall alltid returnera int
    if li != None:
        return int(num)
    else:
        return float(num)



# TODO Flytta ut ritandet och returnera enbart listor med koordinaterna
# Draws [amount] field lines from diffrent places around the earth equaly far from each other
def draw_field_lines(amount, XZ, XY, YZ):

    # calcualtes differnet places around the earth in radians    
    radians = np.arange(0, np.pi*2, np.pi*2/amount)

    calculated_field_lines = []

    # calculates each field line using sin and cos of every angle in two axis
    for angle in radians:
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
        calculated_field_lines.append({"pos": [list(x), list(y), list(z)], "color": "#000000"})

        #* Debug - prints the angle just calculated and amount of coordinates.
        print(angle, ":\n", len(data[3]), ":\n")

        # Draws the field lines
        XZ.draw_field_line(x, z)
        XY.draw_field_line(x, y)
        YZ.draw_field_line(y, z)
        
        # Update the screen
        coordinate_system.update_screen()
        
        print("Field line drawn!")
        
    return calculated_field_lines

def new_calculation():
    window = coordinate_system.setup_environment(
        xscale=20,
        yscale=20,
        win_xwidth=1.0,
        win_ywidth=0.9,
        canvas_xwidth=12000,
        canvas_ywidth=3000
    )

    XZ = coordinate_system.Coordinate_system(window=window, x=-115, y=0, xmin=-50, xmax=20, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="x_GSM (Re)", vertical_name="z_GSM (Re)")
    XY = coordinate_system.Coordinate_system(window=window, x=20, y=0, xmin=-50, xmax=20, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="x_GSM (Re)", vertical_name="y_GSM (Re)")
    YZ = coordinate_system.Coordinate_system(window=window, x=115, y=0, xmin=-25, xmax=25, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="y_GSM (Re)", vertical_name="z_GSM (Re)")

    XZ.prepare_workspace()
    XY.prepare_workspace()
    YZ.prepare_workspace()

    field_lines = draw_field_lines(36, XZ, XY, YZ)
    print("all drawn!\n")
    
    # ### Temporary ###
    # data = geopack.trace(xi=0.14,
    #                          yi=0.04,
    #                          zi=1.12,
    #                          dir=1,
    #                          rlim=60,
    #                          r0=0.99,
    #                          parmod=PARMOD,
    #                          exname="t96",
    #                          inname="igrf",
    #                          maxloop=4000)
    
    # # The data is stored in separate variables. Each variable is a list of all coordinates in that axis.
    # # They are functions of the list index. x[i], y[i] and z[i] are one position on the field line.
    # x, y, z = data[3:6]
    
    # # Draws the field lines
    # XZ.draw_field_line(x, z, "#aa0000")
    # XY.draw_field_line(x, y, "#aa0000")
    # YZ.draw_field_line(y, z, "#aa0000")
    
    if input("Do you want to save the calculated field lines for future rendering? (Y/n)") not in ["n", "N"]:
        print("saving... (to be implemented)")
        
        # Saves the field lines to file
        with open(f"saved_field_lines/{str(datetime.now()).replace(':', '_')}.json", "w") as file:
            json.dump(field_lines, file, indent=3)

    coordinate_system.wait_until_window_is_closed(window)


def load_from_file():
    
        
    
    window = coordinate_system.setup_environment(
        xscale=20,
        yscale=20,
        win_xwidth=1.0,
        win_ywidth=0.9,
        canvas_xwidth=12000,
        canvas_ywidth=3000
    )

    XZ = coordinate_system.Coordinate_system(window=window, x=-115, y=0, xmin=-50, xmax=20, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="x_GSM (Re)", vertical_name="z_GSM (Re)")
    XY = coordinate_system.Coordinate_system(window=window, x=20, y=0, xmin=-50, xmax=20, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="x_GSM (Re)", vertical_name="y_GSM (Re)")
    YZ = coordinate_system.Coordinate_system(window=window, x=115, y=0, xmin=-25, xmax=25, ymin=-25, ymax=25, grid_density=5, small_grid_density=1, horizontal_name="y_GSM (Re)", vertical_name="z_GSM (Re)")

    XZ.prepare_workspace()
    XY.prepare_workspace()
    YZ.prepare_workspace()
    
    saves = os.listdir("saved_field_lines")
    choice = numericQuestion("Which file do you want to load?", li=saves)
    
    chosen_file = f"saved_field_lines/{saves[choice]}"
    
    with open(chosen_file, "r") as file:
        field_lines = json.load(file)
        
        for field_line in field_lines:
            x = field_line[0]
            y = field_line[1]
            z = field_line[2]
                
            # Draws the field lines
            XZ.draw_field_line(x, z)
            XY.draw_field_line(x, y)
            YZ.draw_field_line(y, z)
    

#// TODO flytta ned skapandet av variabler
#// TODO Ta bort main() för det finns inget egentligt syfte med den
# TODO Gör så att man kan rita om med hjälp av de gamla värdena.
# TODO Lägg till möjlighet att rita ut ytterligare fältlinjer (för satellit)
#// TODO Tillåt att man sparar ned beräknade värden till fil
# TODO Tillåt att man kan rita fältlinjer sparade i fil istället för att beräkna nya.

#// TODO Lägg till mindre linjer mellan de större i koordinat systemet.
#// TODO FLytta titeln på axlarna till att vara utanför rektanglarna. (vertikal text för vertikal axel)
# TODO Implementera möjligheten att vända på axlarna så att de går åt andra håll
# TODO färglägg nattsidan av Jorden för att indikera var solen är.

while True:
    
    option = numericQuestion(
        "What do you want to do?",
        li=[
            "New Calculation",
            "Load old calculation from file",
            "Quit and exit program"]
    )

    if option == 0:
        new_calculation()
    elif option == 1:
        load_from_file()
    elif option == 2:
        break
    else:
        print("Something went wrong with choosing option!")
        

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

    # draw_field_lines(36, XZ, XY, YZ)
    # print("all drawn!\n")
    # input("what ")

# XZ.draw_field_line(x, z)
# XY.draw_field_line(x, y)
# YZ.draw_field_line(y, z)

    # coordinate_system.update_screen()

    # coordinate_system.wait_until_window_is_closed(window)
    
    option = numericQuestion(
        "What to do next?",
        li=[
            "Quit and exit program",
            "Change coordinate system scale",
            "Add field line",
            "New Calculation",
            "Load old calculation from file",
            "Save calculations to file"]
    )