#   Name: Efi Pecani
#   ID: 307765230


from tkinter import *         #import all of this stuff in order to wor kwith tkinter methods
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk, messagebox
from PIL import ImageTk
from PIL import Image
import os, sys
import tkinter.font as tkFont

from image_processing import *   #my processing file and functions

#______________________________________________
#______________________________________________

def loadDirectory(path): # gets the list of imges and loads to a listbox
    try:
        imgList.delete(0,END)
        if (type(path))== str:
            picDir = os.listdir(path)
            countFile=0                 #initial value
            for fileName in picDir:
                if fileName[-4:] == ".gif" or fileName[-4:] == ".bmp" or fileName[-4:] == ".jpg" or fileName[-4:] == ".JPG" or fileName[-4:] == ".png":# or fileName[-5:] == ".tiff" :or
                    imgList.insert("end", fileName)
                    countFile += 1
            if countFile == 0:          #in case the firectory is empty
                noPics()                #notify the user
        else:
            global adress
            adress= pathEntry.get()
            loadDirectory(adress)
    except:
        emptyDir()   #notify the user
    return ()
        
#______________________________________________
def createPhoto():          #creates a pic frame and prepers it for the users choise 
    global photoframe                           
    global photo_canvas
    photoframe = Frame(imageZone)
    photo_canvas = Canvas(imageZone,height= 300, width= 400)
    photo_canvas.create_rectangle(300, 400, 0, 0)
    photoframe.grid()
    photoframe.place(x=400, y=40)
    return()
#______________________________________________
def clearBox(): # gets the list of imges and loads to a listbox
    try:
        pathEntry.delete(0,END) #clearing entries
        saveEntry.delete(0,END)
        
        imgList.delete(0,END) #delets boxlist
        photoLable.grid_remove()
        
        photoframe.destroy() #removes pic frame
        photo_canvas.destroy() 
        createPhoto()
        thershZone.destroy()#threshold related widgets
        root.mainloop()
    except:
        field_been_cleared()
#_______________________________________
def deletUpper(event):
    pathEntry.delete(0,END)
#_______________________________________
def deletLower(event):
    saveEntry.delete(0,END)
#_______________________________________
def previewPic(name,adress):
    global picFile
    picFile = Image.open(adress+"/"+name)  # gets the full path of the file
    dim = picFile.size      # get the dimntions
    height = dim[0]
    width = dim[1]                             # Calculate the img size to 372x234
    new_height = (372/float(height))*float(height)
    new_width = (234/float(width))*float(width)
    size = (int(new_height), int(new_width))
    picFile= picFile.resize(size)             # Change the size of the img
    photo = ImageTk.PhotoImage(picFile)
    global photoLable
    photoLable = Label(photoframe, image=photo)      
    photoLable.image = photo
    
    photoLable.grid(row=0, column=1)
#______________________________________________
def previewProcessed(photo_file):
    dim = photo_file.size      # get the dimentions
    width = dim[0] 
    height = dim[1]                            # Calculate the img size to 372x234
    new_height =(372/float(height))*float(height) # (240/float(height))*float(height)
    new_width = (234/float(width))*float(width) #(180/float(width))*float(width)
    size = (int(new_height), int(new_width))
    photo_file= photo_file.resize(size)             # Change the size of the img
    photo = ImageTk.PhotoImage(photo_file)
    photoLable2 = Label(photoframe, image=photo)      
    photoLable2.image = photo
    photoLable2.grid(row=5, column=1)
#______________________________________________
def getPic(event):   # Show the img in a new window
    try:
        try:
            dirc = os.listdir(adress)
        except:
            adress= pathEntry.get()
            tikia = os.listdir(adress)
        global fileList
        fileList = []
        items_num = imgList.curselection()
        first_item = imgList.get("active")
        for file in tikia:   # If the file is not from this list it will not add it to the list
            if file[-4:] == ".gif" or file[-4:] == ".bmp" or file[-4:] == ".jpg" or file[-4:] == ".JPG" or file[-4:] == ".png":
                fileList.append(file)
        global fileName
        fileName = fileList[items_num[0]]
        return previewPic(fileName,adress)
    except FileNotFoundError:
        noCanDo()

    
#______________________________________________
def openFile():   #opens file from directory
    global adress
    adress = filedialog.askdirectory()
    pathEntry.insert(0,adress)
    loadDirectory(adress)
    
#______________________________________________    
def closeWin():
    root.destroy()  #quits the program if user hits "yes"
#______________________________________________    
def questionQuit():
    result= messagebox.askyesno("Close Window", "Are you sure you want to exit?")
    if result == True: #checks for yousers response
        closeWin()
#______________________________________________ 
def browseSave():
    saveEntry.delete(0,END)
    savePath = filedialog.askdirectory()#mode='w', defaultextension=".jpg")
    sPath=savePath  #in order not loosing save path after inserted
    saveEntry.insert(0,sPath)   
#______________________________________________
def getProcess(event):
    try:
        proc_num = opList.curselection()
        proc = opList.get("active")
        global procNum
        procNum=proc_num[0]
        if procNum==3 :
            createThreshold()    #opens a thershelod textbox
            
        selctedProcess(savePath)
    except ValueError:  #to solve problem with some file formats 
        PicformatError()
    except TypeError:
        PicformatError()  #to solve problem with some file formats 
    except IndexError:
        processError()  #to solve problem when no process is selcted and prewviw beeing hit anyway
#______________________________________________
def saveFile():     #saves the modified image
    try:
        proc_num = opList.curselection()
        procNum=proc_num[0]
        savePath= saveEntry.get()
        filesWanted = []
        for place in imgList.curselection():
            savedPicCount=0
            filesWanted.append(fileList[place])
            for pic in filesWanted:  # For each file from selected
                if procNum == 0:
                    rotatePicture((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #0 rotate
                    savedPicCount+=1
                elif procNum == 1:
                    mirrorPicture((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #1 mirror
                    savedPicCount+=1
                elif procNum==2:
                    resizePicture((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #2 resize
                    savedPicCount+=1
                elif procNum==3:
                   # print("thUser:" +str(thUser))
                    #try:
                    thUser=thEntry.get()
                    if thUser != "" and int(thUser)<200 and int(thUser)>0  :     #checks if the user inserted a value
                        edge((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:],int(thUser)) #3 edges -"kavei mitaar"
                        savedPicCount+=1
                    else:
                        noTH() #in case no threshold was not inserted correctly
                    #except:
#                        noTH ()  
#                        thershZone.destroy()
                elif procNum==4:
                    MyAlgorithm1((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #4 primary colors
                    savedPicCount+=1
                elif procNum==5:
                    MyAlgorithm2((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #5 half-tone gray
                    savedPicCount+=1
                elif procNum==6:
                    gaussBlur((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #6 blur
                    savedPicCount+=1
                elif procNum==7:
                    minFilter((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #7 min filter
                    savedPicCount+=1
                elif procNum==8:
                    sharpen((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #8 sharpen
                    savedPicCount+=1
                elif procNum==9:
                    contour((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #9 contour
                    savedPicCount+=1
                elif procNum==10:
                    detail((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #10 detail
                    savedPicCount+=1
                elif procNum==11:
                    edgeEnhanceMore((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #11 edge enhance more
                    savedPicCount+=1
                elif procNum==12:
                    emboss((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #12 emboss
                    savedPicCount+=1
                elif procNum==13:
                    kernelSmooth((adress+"/"+pic),savePath+"/"+pic[:-4]+"_processed"+pic[-4:]) #13 smooth more
                    savedPicCount+=1
        if savedPicCount!=0:                   
            PicSaved(savedPicCount)
        else:
            savingError()
    except PermissionError:
        emptyDir()
    except ValueError:
        PicformatError()
    except TypeError:
        PicformatError()
    except NameError:
        processError()
    except IndexError:
        processError()
#______________________________________________
def loadProName():
    global procList
    procList=[]      #list of processes
    procList=["Rotate 180 ⤵ ",#0
              "Mirror image ⇹",#1
              "Resize ⇱ ⇲",#2
              "Edge recognition",#3
              "Primary colors",#4 my algorith
              "Half-Tone", #5 and some extra
              "Blur",#6 and some extra
              "Min Filter",#7
              "Sharpen",#8
              "Contour",#9
              "Detail",#10
              "Edge Enhance+",#11
              "Emboss Filter",#12
              "Kernel Smooth + ",]  #13
    for i in range(len(procList)):                          
        opList.insert("end", procList[i])                   #puts them in the widget
    return()
#______________________________________________
def callAgainWithTH(): #calls the function again with the new parameter assigned by user
    thUser=thEntry.get() #takes the parameter
    procNum=3
    selctedProcess(savePath) #goes back to function
#______________________________________________    
def createThreshold():   #creates a text box for threshold value fron user
    global thLable
    global thEntry
    global thershZone
    thershZone = Frame(imageZone) #creates new frame for threshold procedure
    thershZone.configure(bg = lsb4)
    thershZone.grid(row = 12, column=0 )#, columnspan=3)
    
    thLable=Label(thershZone, text="Threshold:" ,bg=nw4,fg="khaki1" ,padx=10)
    thLable.grid(row=12, column = 0,sticky=W)
    thEntry=Entry(thershZone,bg = nw4,fg="khaki1",selectbackground ="turquoise4")
    thEntry.grid(row=12, column = 1,sticky=E)
    thEntry.bind("<Button-1>", createThButton)  #click on the textbox creates the button
    
def createThButton(event):  #creates a button for processing edges when user clicks on textbox
    global thButton
    thButton=Button(thershZone, text="Process!" ,command=callAgainWithTH)  
    thButton.grid(row=12, column = 1,sticky=E) #positiong of button

#______________________________________________
def selctedProcess(savePath):   #calls selcted process from "img process" and displayes preview
    if procNum==0:
        newPic=rotatePicture((adress+"/"+fileName),savePath) #0 rotate
        previewProcessed(newPic)
    if procNum==1:
        newPic=mirrorPicture((adress+"/"+fileName),savePath) #1 mirror
        previewProcessed(newPic) 
    if procNum==2:
        newPic=resizePicture((adress+"/"+fileName),savePath) #2 resize smaller
        previewProcessed(newPic)
    if procNum==3:
        try:
            thUser=thEntry.get()
            if thUser != "" and int(thUser)<200 and int(thUser)>0  :     #checks if the user inserted a value
                    newPic=edge((adress+"/"+fileName),savePath,int(thUser)) #3 edges
                    previewProcessed(newPic)
            else:
                noTH()
                thEntry.delete(0,END)
        except:
                noTH()  #in case no threshold was not inserted correctly
                thEntry.delete(0,END)
    if procNum==4:
        newPic=MyAlgorithm1((adress+"/"+fileName),savePath) #4 primary
        previewProcessed(newPic)
    if procNum==5:
        newPic=MyAlgorithm2((adress+"/"+fileName),savePath) #5 half-tone gray  
        previewProcessed(newPic)
    if procNum==6:
        newPic=gaussBlur((adress+"/"+fileName),savePath) #6 blur
        previewProcessed(newPic)
    if procNum==7:
        newPic=minFilter((adress+"/"+fileName),savePath) #7 min filter 
        previewProcessed(newPic)
    if procNum==8:
        newPic=sharpen((adress+"/"+fileName),savePath) #8 sharpen
        previewProcessed(newPic)
    if procNum==9:
        newPic=contour((adress+"/"+fileName),savePath) #9 contour 
        previewProcessed(newPic)
    if procNum==10:
        newPic=detail((adress+"/"+fileName),savePath) #10 detail 
        previewProcessed(newPic)
    if procNum==11:
        newPic=edgeEnhanceMore((adress+"/"+fileName),savePath) #11 edge Enhance More 
        previewProcessed(newPic)
    if procNum==12:
        newPic=emboss((adress+"/"+fileName),savePath) #12 emboss 
        previewProcessed(newPic)
    if procNum==13:
        newPic=kernelSmooth((adress+"/"+fileName),savePath) #13 SMOOTH_MORE 
        previewProcessed(newPic)
#_____________________________MESSEEGES TO USER_________________________________
        
def emptyDir(): #incase a directory path is empty displays an error lable near it
    messagebox.showinfo("Error", "The Folder doesn't contain any photo files.")
def field_been_cleared(): #incaes a button is pressed in vain
    messagebox.showinfo("Clear", "Fields been cleared \nInsert a valid directory path if you wish to continue editing.")
#______________________________________________
def emptyDir(): #incase a directory path is empty displays an error lable near it
    messagebox.showerror("Error", "Empty Directory \nPlease insert a correct directory adress.")
#______________________________________________
def noCanDo():  #general error
    messagebox.showerror("Error", "General Error \nTry pressing the 'Clear' button first and try again. ")
    
def theFilesSaved():  #general error
    messagebox.showinfo("Save Preformed", "Image Processing completed Sucessfully \n Pictures saved in designated folder.")
#______________________________________________
def PicformatError():  #format error that is common with gifs
    messagebox.showinfo("Oops Something Went Wrong", "Image can not be processed \ntry changing pic format or using diffrent filter." )
def noTH():  #format error that is common with gifs
   messagebox.showinfo("Threshold wasn't inserted", "Please insert a value between 0 and 200 and try again!")
def processError():
    messagebox.showerror("Process Selection Required", "Please select a process and hit 'Preview ➩' try again!")
def PicSaved(piCounter):
    messagebox.showinfo("Process Completed", str(piCounter)+" Images were Saved! \nPlease check folder!")
def savingError():
    messagebox.showerror("Attention!", "NOT all Images were Saved! \nPlease check folder! and try again")
#_____________________ END OF SECONDERY FUNCTIONS______________________________________________________

''' %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% '''

#______________________BEGINING OF MAIN FUNCTION WITH WIDGETS _________________________________________

def mainWin():
    
    global intro
    global imageZone
    global savingZone
    global pathEntry
    global imgList
    global opList
    global savePath
    global saveEntry
    global thUser
    thUser="" #initail value for threshold
    savePath=""  #initial value for a save
    
    #frames defined
    intro = Frame(root)
    imageZone = Frame(root)
    imageZone.configure(bg = lsb4)
    savingZone = Frame(root)
    savingZone.configure(bg = lsb4)

    #order of frames
    intro.grid(row = 0, columnspan = 4, )
    imageZone.grid(rowspan=9, row = 1, column = 0, ipadx=50)
    savingZone.grid(row = 10,columnspan = 3, ipadx=50)

    # choosing image area

    header = Label(intro,padx = 200, pady = 10, text=" Welcome to Efi's Editor ", font=root.customFont, bg="khaki1",fg="gray25")
    pathLabel = Label(imageZone, text="   Please enter image directory path:",bg=nw4,fg="khaki1")
    pathEntry = Entry(imageZone,bg = nw4,fg="khaki1",selectbackground ="turquoise4")
    pathEntry.bind_class("Entry","<Return>", loadDirectory)
    pathEntry.bind("<Button-1>",deletUpper)
    goButton = Button(imageZone, text="Go")
    goButton.bind("<Button-1>", loadDirectory)
    clearButton = Button(imageZone, text="Clear", command=clearBox) #clears all
    listLabel = Label(imageZone, text="   The folder containes the folowing images:",bg=nw4,fg="khaki1")
    opendir= Button(imageZone, text=" Open Directory... ", fg="navy", command=openFile)

    # pic list area
    scrollbar1 = Scrollbar(imageZone, orient="vertical")
    imgList = Listbox(imageZone, selectmode=MULTIPLE,  yscrollcommand=scrollbar1.set, width=27,selectbackground =nw4,bg = "khaki1",fg="gray25",exportselection=0) #first list
    scrollbar1.config(command=imgList.yview)
    choosePics = Button(imageZone ,text=" Choose  ➩ ")
    choosePics.bind("<Button-1>", getPic)

    # operation command
    processLabel = Label(imageZone, text="Process your image with:", bg=nw4,fg="khaki1")
    scrollbar2 = Scrollbar(imageZone, orient="vertical")
    opList = Listbox(imageZone, selectmode=SINGLE,  yscrollcommand=scrollbar2.set, width=27,selectbackground =nw4,bg = "khaki1",fg="gray25",exportselection=0)
    scrollbar2.config(command=opList.yview)
    processPics = Button(imageZone ,text=" Preview  ➩ ")
    processPics.bind("<Button-1>", getProcess)
    
    # save zone area
    savedPath = Label(savingZone,text="   Please enter processed image path:           ", bg=nw4,fg="khaki1")
    saveEntry = Entry(savingZone ,bg = nw4,fg="khaki1",selectbackground ="turquoise4")
    saveEntry.bind("<Button-1>",deletLower)
    browseSaveButton = Button(savingZone, text="Browse Saving Directory...",command=browseSave)
    saveButton = Button(savingZone, text="Save",command=saveFile)
    quitbutton = Button(root, text="Quit", command=questionQuit)

    #+++++++++++++++++++++++ Grid Positioning:  +++++++++++++++++++++++++++++

    # browse area grid

    header.grid(row=0, ipadx=100)#columnspan=20)  # the welcome title

    pathLabel.grid(row=1, column=0, sticky=W)  # image path lable "please enter.."
    pathEntry.grid(row=1, column = 1, ipadx=50 )
    goButton.grid(row=1, column=2, sticky=W)
    clearButton.grid(row=1, column=4, sticky=W)
    opendir.grid(row=1, column=3, sticky=W)
    listLabel.grid(row=3, sticky=N)
    choosePics.grid(row=6, column=0,sticky=E)                       #1st button
 # choosePics.place(x=290, y=120)


    createPhoto() # photo zone

    # listbox for img
    scrollbar1.grid(row=5, column=0,sticky=E, ipady=72)
    imgList.grid(row=5, column=0)                 
    imgList.columnconfigure(0, weight=1)

    #listbox for processing
    processLabel.grid(row=9 ,column=0)  #process your image..."
    scrollbar2.grid(row=10, column=0,sticky=E, ipady=72)
    opList.grid(row=10 ,column=0 )
    loadProName()
    processPics.grid(row=11, column=0,sticky=E)                     #2nd button
 #   processPics.place(x=290, y=320)
    
    #emptyLable = Label(imageZone, text="            ", bg=lsb4)
    #emptyLable.grid(row=12 ,column=0,pady=45)  #for spacing it up

    # save area grid
    savedPath.grid(row=1, column=0, sticky= W)       #please enter processed.."
    saveEntry.grid(row=1, column=1, ipadx=50, pady=20)   
    browseSaveButton.grid(row=1, column=2, sticky= E,ipadx = 20)   #  "save as..."
    saveButton.grid(row=1, column=3, sticky= E)  #when ready to save
    quitbutton.grid(row=10, column=0,sticky= E)#, sticky= S+E)#row=1, column=5, sticky= E)
 #   createThreshold()
    root.mainloop()

'''$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ ACTUAL PROGRAM $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'''


# Root/window container definition

root = tk.Tk()
lsb4="LightSteelBlue4"
nw4="NavajoWhite4"
root.geometry("950x700")   #windos size
root.configure(bg=lsb4)
root.title("Efi's Editor")
root.customFont = tkFont.Font(family="Verdana", size=25, weight=tkFont.BOLD, underline = True)

mainWin()

#adress for self checking: /Users/EfiPaka/Pictures/
