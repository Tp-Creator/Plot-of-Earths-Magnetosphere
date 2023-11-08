import turtle as t
from time import sleep
from math import sqrt
import numpy as np



class Coordinate_system():
    def __init__(self, window, x, y, xmin, xmax, ymin, ymax, grid_density, horizontal_name, vertical_name):
        self.window = window
        self.x = x
        self.y = y
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.density = grid_density
        self.horizontal_name = horizontal_name
        self.vertical_name = vertical_name
        self.turtle = t.Turtle()
        
        # Remove visibility of turtle
        self.turtle.hideturtle()
        self.turtle.speed(0)        
    
    def home(self):
        self.turtle.goto(self.x, self.y)
        
    def draw_coordinate_system(self):
        t = self.turtle
        t.pencolor('#5e5e5e')
        t.pencolor('#a8a8a8')
        t.pencolor('#808080')

        # Calculating the size of the arrow in relation to the window size, x and y
        arrow_length = sqrt(self.window.window_width()**2 + self.window.window_height()**2) / 100
        arrow_length_x = arrow_length/self.window.xscale
        arrow_length_y = arrow_length/self.window.yscale
        
        
       # draw horizontal axis        
        t.penup()
        t.goto(self.x+self.xmin, self.y)
        t.pendown()
        t.goto(self.x+self.xmax, self.y)
        
        # horizontal axis arrow
        t.goto(self.x+self.xmax-arrow_length_x, self.y-arrow_length_y)
        t.penup()
        t.goto(self.x+self.xmax, self.y)
        t.pendown()
        t.goto(self.x+self.xmax-arrow_length_x, self.y+arrow_length_y)
        
        # horizontal axis name
        t.penup()
        t.goto(self.x + self.xmax+22/self.window.xscale, self.y-10/self.window.yscale)
        t.pencolor('#5e5e5e')
        t.write(f"{self.horizontal_name}", align='center', font=('Arial', 14, 'normal'))
        t.pencolor('#808080')
        
        # horizontal axis gradering
         # int(self.xmin/self.density)*self.density avrundar nedåt till närmsta koordinat kongruent med self.density.
        for xpos in np.arange(int(self.xmin/self.density)*self.density, self.xmax, self.density):
            t.penup()
            if xpos != 0:
                t.goto(xpos+self.x, self.y-20/self.window.yscale)
                t.write(f"{xpos}", align='center', font=('Arial', 8, 'normal'))
            t.goto(xpos+self.x, self.y-5/self.window.yscale)
            t.pendown()
            t.goto(xpos+self.x, self.y+5/self.window.yscale)
        

       # draw vertical axis        
        t.penup()
        t.goto(self.x, self.y+self.ymin)
        t.pendown()
        t.goto(self.x, self.y+self.ymax)
        
        # vertical axis arrow
        t.goto(self.x-arrow_length_x, self.y+self.ymax-arrow_length_y)
        t.penup()
        t.goto(self.x, self.y+self.ymax)
        t.pendown()
        t.goto(self.x+arrow_length_x, self.y+self.ymax-arrow_length_y)
        
        # vertical axis name
        t.penup()
        t.goto(self.x, self.y + self.ymax+20/self.window.yscale)
        t.pencolor('#5e5e5e')
        t.write(f"{self.vertical_name}", align='center', font=('Arial', 14, 'normal'))
        t.pencolor('#808080')
        
        # vertical axis gradering
         # int(self.ymin/self.density)*self.density är kongruent med self.density vilket gör att en av punkterna blir 0
        for ypos in np.arange(int(self.ymin/self.density)*self.density, self.ymax, self.density):
            t.penup()
            if ypos != 0:
                t.goto(self.x-15/self.window.xscale, ypos-7/self.window.yscale+self.y)
                t.write(f"{ypos}", align='center', font=('Arial', 8, 'normal'))
            t.goto(self.x-5/self.window.xscale, ypos+self.y)
            t.pendown()
            t.goto(self.x+5/self.window.xscale, ypos+self.y)

    def draw_earth(self):
        t = self.turtle
        
        t.penup()
        t.goto(self.x, self.y-1)
        t.pendown()
        t.circle(1, steps=180)
     
    def draw_box(self):
        t = self.turtle
        t.color("#000000")
        
        t.penup()
        t.goto(self.x + self.xmin-20/self.window.xscale, self.y + self.ymax+40/self.window.yscale)   
        t.pendown()
        t.goto(self.x + self.xmax+30/self.window.xscale, self.y + self.ymax+40/self.window.yscale)   
        t.goto(self.x + self.xmax+30/self.window.xscale, self.y + self.ymin-20/self.window.yscale)   
        t.goto(self.x + self.xmin-20/self.window.xscale, self.y + self.ymin-20/self.window.yscale)   
        t.goto(self.x + self.xmin-20/self.window.xscale, self.y + self.ymax+40/self.window.yscale)
        
    # Function that draws out all things that are known how to be displayed without further arguments.
    def prepare_workspace(self):
        self.draw_coordinate_system()
        self.draw_earth()
        self.draw_box() 
        
    def draw_field_line(self, horizontal_coords:list, vertical_coords:list, color="#000000"):
        if not len(horizontal_coords) == len(vertical_coords):
            print("The lists are not equaly long!")

        # Prepare for drawing        
        t = self.turtle
        t.color(color)
        
        t.penup()
        t.goto(self.x + horizontal_coords[0], self.y + vertical_coords[0])
        t.pendown()
        for x, y in zip(horizontal_coords, vertical_coords):
            t.goto(self.x + x, self.y + y)
        
        
def setup_environment(xscale=5, yscale=5, win_xwidth=1.0, win_ywidth=0.9, canvas_xwidth=5000, canvas_ywidth=2000):    
    # disables the update function built in to turtle for quicker drawing
    t.tracer(0, 0)
    
    # object of the displaying screen
    window = t.Screen()
    
    # Makes the window fullscreen (1.00 % of the screen)
    window.setup(win_xwidth, win_ywidth)

    # 1px in turtle = [scale]px on screen in x respective y
    window.xscale = xscale
    window.yscale = yscale
    
    # Increases the size of the canvas. (Adds scrolling)
    window.screensize(canvas_xwidth, canvas_ywidth)
    
    return window
    
# updates the screen
def update_screen():
    t.update()
    
# goes into a whileloop until the window is exited
def wait_until_window_is_closed(window):
    # Wait for mouse click on exit
    window.exitonclick()
    
        

if __name__ == "main":
    
    # disables the update function built in to turtle for quicker drawing
    t.tracer(0, 0)
    # object of the displaying screen
    window = t.Screen()
    # Makes the window fullscreen (1.00 % of the screen)
    window.setup(1.0, 0.9)

    # 1px in turtle = 10px on screen 
    window.xscale = 10
    window.yscale = 10
    
    XZ = Coordinate_system(x=-115, y=10, xmin=-70, xmax=30, ymin=-30, ymax=30, grid_density=5, horizontal_name="x", vertical_name="z")
    XY = Coordinate_system(x=20, y=0, xmin=-70, xmax=30, ymin=-30, ymax=30, grid_density=5, horizontal_name="x", vertical_name="y")
    YZ = Coordinate_system(x=115, y=-10, xmin=-30, xmax=30, ymin=-30, ymax=30, grid_density=5, horizontal_name="y", vertical_name="z")

    XZ.prepare_workspace()
    XY.prepare_workspace()
    YZ.prepare_workspace()

    # XZ.draw_coordinate_system()
    # XY.draw_coordinate_system()
    # YZ.draw_coordinate_system()

    # XZ.draw_earth()
    # XY.draw_earth()
    # YZ.draw_earth()

    # XZ.draw_box()
    # XY.draw_box()
    # YZ.draw_box()

    x = [1, 2, 3, 3.54, 3.66, 3.72, 3.73, 3.74, 3.81, 4.010001, 4.4567, 4.6789, 4.9876, 5.3, 5.1, 4.9, 4.7, 4.5, 4.3, 4.1, 3.9, 3.5, 3.0, 2.2, 1.2, 0.1, -0.32, -10]
    y = [1, 2, 3, 3.54, 3.66, 3.72, 3.73, 3.74, 3.81, 4.010001, 4.4567, 4.6789, 4.9876, 5.3, 5.1, 4.9, 4.7, 4.5, 4.3, 4.1, 3.9, 3.5, 3.0, 2.2, 1.2, 0.1, -0.32]
    y.reverse()
    XZ.draw_field_line(x, y, "#5598ee")

    # updates the screen when everything is drawn
    t.update()
    # To increase the size of the canvas. Adds scrolling
    window.screensize(5000, 2000)


    # def draw_coordinat_system(start_x, start_y, dim_x, dim_y):
    #     t.penup()
    #     t.goto(start_x, start_y)

    # print(x, y)

    h = window.window_height()
    w = window.window_width()
    print(h, w)


    # Wait for mouse click on exit
    window.exitonclick()