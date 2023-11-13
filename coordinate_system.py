import turtle as t
# from time import sleep
from math import sqrt
import numpy as np



class Coordinate_system():
    def __init__(
            self, 
            window, 
            x: int | float,
            y: int | float,
            xmin: int | float,
            xmax: int | float,
            ymin: int | float,
            ymax: int | float,
            grid_density: float,
            small_grid_density: float | None,
            horizontal_name: str,
            vertical_name: str):
        
        self.window = window
        self.x = x
        self.y = y
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.grid_density = grid_density
        self.small_grid_density = small_grid_density
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
        
        
        ###############
        # draw HORIZONTAL AXIS
                
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
        
        
        # horizontal axis grid
         # int(self.xmin/self.density)*self.density avrundar nedåt till närmsta koordinat kongruent med self.density.
        for xpos in np.arange(int(self.xmin/self.grid_density)*self.grid_density, self.xmax, self.grid_density):
            t.penup()
            # write grid value number 
            if xpos != 0:
                t.goto(xpos+self.x, self.y-2.5)
                t.write(f"{xpos}", align='center', font=('Arial', int(self.window.xscale), 'normal'))
            # Draw the line
            t.goto(xpos+self.x, self.y-0.5)
            t.pendown()
            t.goto(xpos+self.x, self.y+0.5)
        
        # horizontal small grid - small grid density
        for xpos in np.arange(int(self.xmin/self.small_grid_density)*self.small_grid_density, self.xmax, self.small_grid_density):
            if (1 < xpos or xpos < -1) and xpos % self.grid_density != 0:
                t.penup()
                t.goto(xpos+self.x, self.y-0.2)
                t.pendown()
                t.goto(xpos+self.x, self.y+0.2)
        
               
        ###############
        # draw VERTICAL AXIS         
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
        
        # vertical grid - grid densisty
         # int(self.ymin/self.density)*self.density är kongruent med self.density vilket gör att en av punkterna blir 0
        for ypos in np.arange(int(self.ymin/self.grid_density)*self.grid_density, self.ymax, self.grid_density):
            t.penup()
            if ypos != 0:
                t.goto(self.x-1, self.y+ypos-0.7)
                t.write(f"{ypos}", align='right', font=('Arial', int(self.window.xscale), 'normal'))
            t.goto(self.x-0.5, ypos+self.y)
            t.pendown()
            t.goto(self.x+0.5, ypos+self.y)
        
        # vertical small grid - small grid density
        for ypos in np.arange(int(self.ymin/self.small_grid_density)*self.small_grid_density, self.ymax, self.small_grid_density):
            if (1 < ypos or ypos < -1) and ypos % self.grid_density != 0:                
                t.penup()
                t.goto(self.x-0.2, ypos+self.y)
                t.pendown()
                t.goto(self.x+0.2, ypos+self.y)


    def draw_earth(self):
        t = self.turtle
        
        t.penup()
        t.goto(self.x, self.y-1)
        t.pendown()
        t.circle(1, steps=180)
     
    def draw_box(self):
        # Formulas to calculate the sides
        left = self.x + self.xmin-40/self.window.xscale - 1
        right = self.x + self.xmax+40/self.window.xscale + 1
        top = self.y + self.ymax+40/self.window.yscale + 1
        bottom = self.y + self.ymin-40/self.window.yscale - 1
        
        text_size = 18
        
        t = self.turtle
        t.color("#000000")
        
        # Draw box
        t.penup()
        t.goto(left, top)   
        t.pendown()
        t.goto(right, top)   
        t.goto(right, bottom)   
        t.goto(left, bottom)   
        t.goto(left, top)
        t.penup()
        
        # Horizontal axis name
        t.goto((left+right) / 2, bottom-30/self.window.yscale)
        t.write(f"{self.horizontal_name}", align='center', font=('Arial', text_size, 'normal'))
        
        # vertical axis name
         # in pure turtle it is not possible to rotate text.
         # Becuase of this tkinter is used here, since we want to rotate the text
         # Since turtle is based on tkinter, the main function could be found in the turtle library
        t._screen.cv._canvas.create_text(
            (left*self.window.xscale-20, (top+bottom)*self.window.yscale / 2),
            text=self.vertical_name,
            justify="center",
            font=('Arial', text_size, 'normal'),
            angle=90
        )


    # Function that draws out all things that are known how to be displayed without further arguments.
    def prepare_workspace(self):
        self.draw_coordinate_system()
        self.draw_earth()
        self.draw_box() 
        
    def draw_field_line(self, horizontal_coords:list, vertical_coords:list, color="#000000"):
        if not len(horizontal_coords) == len(vertical_coords):
            print("The lists of coordinates are not equaly long!")

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
    
    # Makes the window fullscreen (1.00 % of the screen), startx and y is where on the screen the window should be created
    window.setup(width=win_xwidth, height=win_ywidth, startx=-1, starty=0)

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
    
        

if __name__ == "__main__":
    
    print("hallå?")
    
    window = setup_environment(
        xscale=30,
        yscale=30,
        win_xwidth=1.0,
        win_ywidth=0.9,
        canvas_xwidth=120000,
        canvas_ywidth=30000
    )
    
    
    XZ = Coordinate_system(window=window, x=-115, y=0, xmin=-70, xmax=30, ymin=-30, ymax=30, grid_density=5, small_grid_density=1, horizontal_name="x (Re) solvind bl bla bla", vertical_name="pls work better now!")
    XY = Coordinate_system(window=window, x=20, y=0, xmin=-70, xmax=30, ymin=-30, ymax=30, grid_density=5, small_grid_density=1, horizontal_name="x", vertical_name="idk what is happening")
    YZ = Coordinate_system(window=window, x=115, y=0, xmin=-30, xmax=30, ymin=-30, ymax=30, grid_density=5, small_grid_density=1, horizontal_name="y", vertical_name="Yees")

    XZ.prepare_workspace()
    XY.prepare_workspace()
    YZ.prepare_workspace()


    x = [1, 2, 3, 3.54, 3.66, 3.72, 3.73, 3.74, 3.81, 4.010001, 4.4567, 4.6789, 4.9876, 5.3, 5.1, 4.9, 4.7, 4.5, 4.3, 4.1, 3.9, 3.5, 3.0, 2.2, 1.2, 0.1, -0.32, -10]
    y = [1, 2, 3, 3.54, 3.66, 3.72, 3.73, 3.74, 3.81, 4.010001, 4.4567, 4.6789, 4.9876, 5.3, 5.1, 4.9, 4.7, 4.5, 4.3, 4.1, 3.9, 3.5, 3.0, 2.2, 1.2, 0.1, -0.32]
    y.reverse()
    XZ.draw_field_line(x, y, "#5598ee")

    # updates the screen when everything is drawn
    t.update()
    t.mainloop()

    h = window.window_height()
    w = window.window_width()
    print(h, w)


    # Wait for mouse click on exit
    window.exitonclick()