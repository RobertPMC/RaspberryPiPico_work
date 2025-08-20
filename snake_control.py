import tkinter as tk
from serial import Serial
from time import sleep


port = "COM3"
baudrate = 115200
serial_connection = Serial(port, baudrate)

direction = "W"

def caca(event):
    sleep(5)
    serial_connection.close()
    exit()

def move_forward(event):
    global direction
    direction = "W"
    tk.Label(window, text=direction).pack()
    serial_connection.write(direction.encode())

def move_to_the_left(event):
    global direction
    direction = "A"
    tk.Label(window, text=direction).pack()
    serial_connection.write(direction.encode())

def move_backwards(event):
    global direction
    direction = "S"
    tk.Label(window, text=direction).pack()
    serial_connection.write(direction.encode())

def move_to_the_right(event):
    global direction
    direction = "D"
    tk.Label(window, text=direction).pack()
    serial_connection.write(direction.encode())


window = tk.Tk()


window.bind("<W>", move_forward)
window.bind("<A>", move_to_the_left)
window.bind("<S>", move_backwards)
window.bind("<D>", move_to_the_right)
window.bind("<w>", move_forward)
window.bind("<a>", move_to_the_left)
window.bind("<s>", move_backwards)
window.bind("<d>", move_to_the_right)
window.bind("<q>", caca)

window.mainloop()

