from geopack import geopack
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from concurrent import futures
import coordinate_system

dt_obj = datetime.strptime('2015-09-23 08:21:00', '%Y-%m-%d %H:%M:%S')

# The number of seconds since 1970-01-01 00:00:00
ut = dt_obj.timestamp()


geopack.recalc(ut, vxgse=-400, vygse=0, vzgse=0)

PARMOD = [
    5,   # solar wind pressure pdyn (nanopascals)
    0,   # dst (nanotesla)
    0,   # byimf (nanotesla)
    2,   # bzimf (nanotesla)
]

# Checks if string can be converted to float
def isfloat(string:str) -> bool:
    return string.replace(".", "", 1).isnumeric()

# En input som bara accepterar att man skriver in integers alternativt float mellan max och min
# Om man lägger till li som argument skrivs max och min över och vi skriver
# ut alla alternativen som finns i listan istället, och utgår ifrån det för max och min
# Man kan även lägga till felmeddelande om användaren skrev fel (annars default)
# Msg är frågan användaren får
def numericQuestion(msg, max=None, min=0, li=None, err=None):
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
    if li == None:
        return int(num)
    else:
        return float(num)


#! This function should not be called
def trace_middlehand(angle):
    dir = 1 if np.sin(angle) > 0 else -1
        
    print("yyyyyyeeeeeeezzz")
    return geopack.trace(xi=np.cos(angle),
                            yi=0,
                            zi=np.sin(angle),
                            dir=dir,
                            rlim=60,
                            r0=0.99,
                            parmod=PARMOD,
                            exname="t96",
                            inname="igrf",
                            maxloop=500
    )

# TODO Flytta ut ritandet och returnera enbart listor med koordinaterna
# Draws [amount] field lines from diffrent places around the earth equaly far from each other
def draw_field_lines(amount, XZ, XY, YZ):
    # calcualtes differnet places around the earth in radians
    # radians = []
    
    radians = np.arange(0, np.pi*2, np.pi*2/amount)
        
    # for i in range(amount):
    #     radians.append(np.pi*2 * i / amount)
        
    
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
                             maxloop=500)
        # data = geopack.trace(xi=0, yi=0, zi=1.0, dir=1, rlim=60, r0=1, parmod=parmod, exname="t96", inname="igrf", maxloop=4000)

        # the data is stored in separate variables. Each variable is a list of all coordinates in that axis.
        # They are functions of the list index. x[i], y[i] and z[i] are one position on the field line.
        x, y, z = data[3:6]

        print(angle, ":\n", len(data[3]), ":\n")

        XZ.draw_field_line(x, z, "#990000")
        XY.draw_field_line(x, y)
        YZ.draw_field_line(y, z)
        
        # XZ.draw_field_line([np.cos(angle), np.cos(angle)*10], [np.sin(angle), np.sin(angle)*10])

        coordinate_system.update_screen()
        
        print("Field line drawn!")
# re = []
# for i in range(13):
#     re.append((np.pi*i)/6)
    
# print(re)


# a = geopack.trace(xi=0, yi=0, zi=1, dir=1, rlim=60, r0=1, parmod=parmod, exname="t96", inname="igrf", maxloop=10000)
# a = geopack.trace(xi=0, yi=np.cos(re[2]), zi=np.sin(re[2]), dir=1, rlim=60, r0=1, parmod=parmod, exname="t96", inname="igrf", maxloop=10000)

# Write to file
# def write_to_file(path, content):
#     with open(path, "a", encoding="utf-8") as file:
#         file.write(str(content))
#     return True



# print(a)

# # The coordinates of the field line separated into three different lists
# x = a[3]
# y = a[4]
# z = a[5]

# print(a[3])
# for b in a[3]:
#     print(b)
#     write_to_file("hej.txt", str(b)+"\n")
# print("\n\nhejejeje\n\n")
# for b in a[4]:
#     write_to_file("hej.txt", str(b)+"\n")
# print("\n\nmememem\n\n")
# for b in a[5]:
#     print(b)
#     write_to_file("hej.txt", str(b)+"\n\n")
# print("c")

# print("Calculations done. Drawing!")

def main():
    
    # TODO flytta ned skapandet av variabler
    # TODO Ta bort main() för det finns inget egentligt syfte med den
    # TODO Gör så att man kan rita om med hjälp av de gamla värdena.
    # TODO Lägg till möjlighet att rita ut ytterligare fältlinjer (för satellit)
    # TODO Tillåt att man sparar ned beräknade värden till fil
    # TODO Tillåt att man kan rita fältlinjer sparade i fil istället för att beräkna nya.
    
    # TODO Lägg till mindre linjer mellan de större i koordinat systemet.
    # TODO FLytta titeln på axlarna till att vara utanför rektanglarna. (vertikal text för vertikal axel)
    # TODO Implementera möjligheten att vända på axlarna så att de går åt andra håll
    # TODO färglägg nattsidan av Jorden för att indikera var solen är.
    
    while True:
        
        option = numericQuestion(
            "What to do next?",
            li=[
                "Change coordinate system settings",
                "Add new field line",
                "Quit and exit program"]
        )

        if option == 0:
            pass
        elif option == 1:
            pass
        elif option == 2:
            break
        else:
            print("Something went wrong with choosing option!")
            

        window = coordinate_system.setup_environment(
            xscale=30,
            yscale=30,
            win_xwidth=1.0,
            win_ywidth=0.9,
            canvas_xwidth=12000,
            canvas_ywidth=3000
        )

        XZ = coordinate_system.Coordinate_system(window=window, x=-115, y=0, xmin=-70, xmax=30, ymin=-30, ymax=30, grid_density=2, horizontal_name="Bx (Re) GSM", vertical_name="Bz (Re) GSM")
        XY = coordinate_system.Coordinate_system(window=window, x=20, y=0, xmin=-70, xmax=30, ymin=-30, ymax=30, grid_density=2, horizontal_name="Bx (Re) GSM", vertical_name="By (Re) GSM")
        YZ = coordinate_system.Coordinate_system(window=window, x=115, y=0, xmin=-30, xmax=30, ymin=-30, ymax=30, grid_density=2, horizontal_name="By (Re) GSM", vertical_name="Bz (Re) GSM")

        XZ.prepare_workspace()
        XY.prepare_workspace()
        YZ.prepare_workspace()

        draw_field_lines(12, XZ, XY, YZ)
        print("all drawn!\n")
        # input("what ")

    # XZ.draw_field_line(x, z)
    # XY.draw_field_line(x, y)
    # YZ.draw_field_line(y, z)

        coordinate_system.update_screen()

        coordinate_system.wait_until_window_is_closed(window)
        input()

main()

