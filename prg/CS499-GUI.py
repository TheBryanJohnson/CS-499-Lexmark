# This is the GUI for CS499 Lexmark Team

#TO DO:
#make instruction manual
#make restore work
#figue out how the options will work
#flags if user messes up

from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog


#master is a frame that holds the rest of the panels and buttons
master = Frame(height=300, width=670, bd=3, background="light blue")
master.grid_propagate(0)
master.pack()

#preImg is a frame that holds the users uploaded image
preImg = Frame(master, height=200, width=200, bd=3, background="purple", relief=RAISED)
preImg.grid_propagate(0)
preImg.grid(column=0, row=0, columnspan=1, rowspan=1, padx=5, pady=5)

#postImg is a frame that holds the new image that is produced from the machine learning model
postImg = Frame(master, height=200, width=200, bd=3, background="purple", relief=RAISED)
postImg.grid_propagate(0)
postImg.grid(column=2, row=0, columnspan=1, rowspan=1, padx=5, pady=5)

#menuFrame is a frame that holds the options for machine learning model
menuFrame = Frame(master, height=200, width=100, bd=3, background="light blue")
menuFrame.grid(column=1, row=0, columnspan=1, rowspan=1, padx=5, pady=5)

#controlFrame is a frame that holds various buttons for controlling the program
controlFrame = Frame(master, height=100, width=100, bd=3, background="light blue")
controlFrame.grid(column=0, row=1, columnspan=3, rowspan=1, padx=50, pady=10)

#global variable to disp imag, wont show up on GUI without it
labelImg1 = 0
img1 = 0
fileName = 0
preLabel = Label(preImg, height = 200, width = 200)

#getFileName opens the file browser and accepts a valid file type from the user
def getFileName():
    #call global variable so variables can be accessed outside the definition
    global labelImg1, img1, fileName, preLabel  
    #open file browser and request a file, also make sure that file is of the accepted type
    acceptedTypes = [("Image File", "*.jpg") , ("Image File", "*.gif") , ("Image File", "*.tiff"), ("Image File", "*.png")]
    fileName = filedialog.askopenfilename(filetypes = acceptedTypes)
    img1 = Image.open(fileName)
    #dont need the quality for GUI display so made a thumbnail
    img1.thumbnail((200,200), resample=3)
    #put the thumbnail in a label, put the label in the preImg frame
    labelImg1 = ImageTk.PhotoImage(img1)
    preLabel.configure(image = labelImg1)
    preLabel.image = labelImg1
    preLabel.pack(side="right", expand=True)

    
#openButton calls getFileName upon user click
openButton = Button(controlFrame, text="OPEN", command = getFileName)
openButton.grid(column=0, row=0, padx=50, pady=5, sticky=W)

#more global variables
labelImg2 = 0
img2 = 0
dummyFile = 0
saveFile = 0
postLabel = Label(postImg, width = 200, height = 200)

#restoreImg takes the input file, runs it through the machine learning model, and returns a new file to be saved
def restoreImg():
    global filename, labelImg2, img2, dummyFile, saveFile
    #receive the input file
    dummyFile = fileName
    #!!!!!!!!!!!!!!!!!!!get the option
    #!!!!!!!!!!!!!!!!!!!run the restore
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    saveFile = dummyFile # This needs to be changed to get the output image
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #return new image
    img2 = Image.open(dummyFile)
    img2.thumbnail((200,200),resample=3)
    labelImg2 = ImageTk.PhotoImage(img2)
    postLabel.configure(image = labelImg2)
    postLabel.image = labelImg2
    postLabel.pack(side="right", expand=True)    

#restoreButton calls the restoreImg function upon user click
restoreButton = Button(controlFrame, text = "RESTORE", command = restoreImg)
restoreButton.grid(column=3, row=0, columnspan=2, padx=100, pady=5, sticky=N)

this = 0
toSave = 0

#saveAs is a function that allows the user to get the newly made file and save it under a selected name and place
def saveAs():
    global this, img2
    #this opens the file dialog for saving
    this = filedialog.asksaveasfile(mode='w', defaultextension='.jpg')
    if this is None: #closed with cancel option
        return
    #save the new image uder the typed in name
    img2.save(this.name)
    
    
saveButton = Button(controlFrame, text="SAVE AS", command= saveAs)
saveButton.grid(column=6, row=0, padx=50, pady=5, sticky=E)

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
