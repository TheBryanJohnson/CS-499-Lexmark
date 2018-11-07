# This is the GUI for CS499 Lexmark Team

from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog


master = Frame(height=300, width=600, bd=3, background="light blue")
master.pack()

preImg = Frame(master, height=200, width=200, bd=3, background="purple", relief=RAISED)
preImg.grid(column=0, row=0, columnspan=1, rowspan=1, padx=5, pady=5)

postImg = Frame(master, height=200, width=200, bd=3, background="purple", relief=RAISED)
postImg.grid(column=2, row=0, columnspan=1, rowspan=1, padx=5, pady=5)

menuFrame = Frame(master, height=200, width=100, bd=3, background="light blue", relief=RAISED)
menuFrame.grid(column=1, row=0, columnspan=1, rowspan=1, padx=5, pady=5)

controlFrame = Frame(master, height=100, width=100, bd=3, background="light blue", relief=RAISED)
controlFrame.grid(column=0, row=1, columnspan=3, rowspan=1, padx=50, pady=10)

restoreButton = Button(menuFrame, text = "RESTORE", command=lambda: print("restore pressed"))
restoreButton.grid(column=0, row=1, columnspan=2, padx=5, pady=25)

labelImg = 0

def getFileName():
    fileName = filedialog.askopenfilename()
    print(fileName)
    img1 = Image.open(fileName)
    img1.thumbnail((90,90), resample=3)
    global labelImg
    labelImg = ImageTk.PhotoImage(img1)
    preLabel = Label(preImg, image=labelImg).pack(side="right", expand=True)
    
#accepting jpeg and pdf
openButton = Button(controlFrame, text="OPEN", command = getFileName)
openButton.grid(column=0, row=0, padx=75, pady=5, sticky=W)


quitButton = Button(controlFrame, text="QUIT", fg="red", command=quit)
quitButton.grid(column=1, row=0, padx=75, pady=5, sticky=E)

#used for drop menu
tkvar = StringVar()

# Array with options
options = [ '100dpi','200dpi','300dpi']
tkvar.set('300dpi') # set the default option

dropMenu = OptionMenu(menuFrame, tkvar, *options)
Label(menuFrame, text="Restore to:").grid(row = 0, column = 0, padx=5, pady=5)
dropMenu.grid(row = 0, column =1)

# on change dropdown value
def change_dropdown(*args):
    print( tkvar.get() )

# link function to change dropdown
tkvar.trace('w', change_dropdown)


mainloop()