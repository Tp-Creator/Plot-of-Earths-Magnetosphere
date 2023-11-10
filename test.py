import turtle

t = turtle.Turtle()


print(vars(t._screen.cv._canvas))

t.forward(100)
# t._screen.cv._canvas.create_text(100,100,text="rotate text", justify="center", font=('Times new Roman', 14, 'normal'), angle=90)
t._screen.cv._canvas.create_text(0,0,text="rotate text", justify="left", font=('Arial', 30, 'normal'), angle=0)

input()

# t.write("bruh", align='center', font=('Arial', 14, 'normal'))
# t.tilt(33)
# t.write("yes!", align='center', font=('Arial', 14, 'normal'))

# input()