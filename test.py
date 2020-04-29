from tkinter import *
import tkinter.ttk as ttk
import time, threading
root = Tk()

pb = ttk.Progressbar(root, orient = HORIZONTAL, length = 200, mode = 'determinate') 
pb.pack()

def progress():
    for i in range(2000):
        pb['value'] += 0.1
        time.sleep(.3)

threading.Thread(target=progress).start()
root.mainloop()