# This is the GUI for CS499 Lexmark Team

#TO DO:
#make instruction manual
#make restore dummy function until full restore is made
#figue out how the options will work
#Save As Funtion
#flags if user messes up

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

#global variable to disp imag, wont show up on GUI without it
labelImg1 = 0
img1 = 0
fileName = 0

def getFileName():
    #call global variable so variables can be accessed outside the definition
    global labelImg1, img1, fileName    
    #open file browser and request a file
    fileName = filedialog.askopenfilename()
    print("fileName = " + fileName)
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! add in file verification
    img1 = Image.open(fileName)
    #dont need the quality for GUI display so made a thumbnail
    img1.thumbnail((90,90), resample=3)
    
    #put the thumbnail in a label, put the label in the preImg frame
    labelImg1 = ImageTk.PhotoImage(img1)
    preLabel = Label(preImg, image=labelImg1).pack(side="right", expand=True)
    
#accepting jpeg and pdf
openButton = Button(controlFrame, text="OPEN", command = getFileName)
openButton.grid(column=0, row=0, padx=75, pady=5, sticky=W)

labelImg2 = 0
img2 = 0
dummyFile = 0
saveFile = 0
def restoreImg():
    global filename, labelImg2, img2, dummyFile, saveFile
    #receive the input file
    dummyFile = fileName
    print("dummyFile = " + dummyFile)
    #!!!!!!!!!!!!!!!!!!!get the option
    #!!!!!!!!!!!!!!!!!!!run the restore
    saveFile = dummyFile
    print ("saveFile = " + saveFile)
    #return new image
    img2 = Image.open(dummyFile)
    print(img2)
    img2.thumbnail((90,90),resample=3)
    print(img2)
    labelImg2 = ImageTk.PhotoImage(img2)
    postLabel = Label(postImg, image=labelImg2).pack(side="right",expand=True)

restoreButton = Button(menuFrame, text = "RESTORE", command = restoreImg)
restoreButton.grid(column=0, row=1, columnspan=2, padx=5, pady=25)

this = 0
toSave = 0
def saveAs():
    print("Save As clicked")
    global this, img2
    #this opens the file dialog for saving
    this = filedialog.asksaveasfile(mode='w', defaultextension='.jpg')
    if this is None: #closed with cancel option
        return
    #save the new image uder the typed in name
    img2.save(this.name)
    
    
saveButton = Button(controlFrame, text="SAVE AS", command= saveAs)
saveButton.grid(column=1, row=0, padx=75, pady=5, sticky=E)

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
