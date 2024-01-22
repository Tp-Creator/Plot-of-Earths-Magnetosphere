from datetime import datetime

import numpy as np
from geopack import geopack

import coordinate_system

geopack.recalc(ut = datetime.strptime('2016--71 12:46:40', '%Y--%j %H:%M:%S').timestamp())

def MLT_CGlat(MLT, CGlat, r=1):
    
    # MLT = 18    # o'clock
    # CGlat = 70  # degrees
    
    
    # MLT and CGlat to gsm coordinates
    # TODO
    MLT
    colat = CGlat # ?
    
    
    theta = CGlat * (np.pi/180)
    
    # theta = smlat = 90.0 - ((colat * 180.0) / np.pi)
    # smlat + colat*180.0/np.pi = 90.0
    # colat*180.0/np.pi = 90.0 - smlat
    # colat*180.0 = np.pi * (90.0 - smlat)
    # colat = (np.pi/180.0) * (90.0 - smlat)
    
    # mlt=12+smlon/15.0
    # mlt-12 = smlon/15.0
    phi = smlon = ((MLT-12) * 15.0) * (np.pi/180)

    print("")
    print("theta:", theta)
    print("phi:", phi)

    # smlon=xlon*180.0/np.pi
    # xlon = (smlon*np.pi)/180.0
    # kanske r?
    
    # spherical to cartesian
    xsm, ysm, zsm = geopack.sphcar(r, theta, phi, j=1)
    
    # convert sm to gsm
    xgsm, ygsm, zgsm = geopack.smgsm(xsm, ysm, zsm, 1)
    
    # print("gsm:", xgsm, ygsm, zgsm)
    
    return xgsm, ygsm, zgsm

def create_coordinate_systems(window):
    # Create coordinate system objects
    XZ = coordinate_system.Coordinate_system(
        window=window,
        x=-120,
        y=0,
        xmin=-20,
        xmax=20,
        ymin=-20,
        ymax=20,
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
        xmin=-20,
        xmax=20,
        ymin=-20,
        ymax=20,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="x_GSM (Re)",
        vertical_name="y_GSM (Re)",
        horizontal_dir=-1
    )
    
    YZ = coordinate_system.Coordinate_system(
        window=window,
        x=100,
        y=0, 
        xmin=-20,
        xmax=20,
        ymin=-20,
        ymax=20,
        grid_density=5,
        small_grid_density=1,
        horizontal_name="y_GSM (Re)",
        vertical_name="z_GSM (Re)"
    )

    return XZ, XY, YZ

##################################
window_settings = {
    "xscale": 10,
    "yscale": 10,
    "win_xwidth": 1.0,
    "win_ywidth": 0.9,
    "canvas_xwidth": 12000,
    "canvas_ywidth": 3000
}

# Create turtle window
window = coordinate_system.setup_environment(**window_settings)
##################################

XZ, XY, YZ = create_coordinate_systems(window)

# Draws the coordinatesystems
XZ.prepare_workspace()
XY.prepare_workspace()
YZ.prepare_workspace()
 
# # Draws the field lines
# XZ.draw_field_line(x, z)
# XY.draw_field_line(x, y)
# YZ.draw_field_line(y, z)


mlt = 6
lat = 60
x, y, z = MLT_CGlat(mlt, lat)

print(x, y, z)

xx= [0, x*20]
yy= [0, y*20]
zz= [0, z*20]
color = "#ff0000"

# Draws the field lines
XZ.draw_field_line(xx, zz, color)
XY.draw_field_line(xx, yy, color)
YZ.draw_field_line(yy, zz, color)

window.tracer(0, 0)
window.update()

input()

# for mlt in range(11, 14):
#     print(f"-------\nMLT: {mlt}\n-------")
#     for lat in range(-90, 90, 10):
#         # print(lat)
#         print(lat, ":", MLT_CGlat(mlt, lat))