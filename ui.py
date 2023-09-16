import tkinter
from time import sleep

root = tkinter.Tk()

s = tkinter.Canvas(root, width=1000, height=1000)
s.pack()

while True:
  for i in range( 100 ): #blueAmt 0, 1, 2, 3...., 254, 255
      ball = s.create_oval(i, i-10, i-10, i, fill = '#000')
      
      s.update()
      sleep(0.03)
      
      s.delete(ball)
      s.update()