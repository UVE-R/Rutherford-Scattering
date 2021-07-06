# Multiframe TKINTER app for the GUI
import tkinter as tk
from PIL import ImageTk, Image
from simulation import Run

#Window dimensions
sWidth = 1024
sHeight = 768

#Base frame class
#Allows us to switch between frames
class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(MenuPage)
        
        self.resizable(width=False, height=False) #Stop the window from being resized
        self.title("The Atomic Model")       
        
    #Handles switching from the old frame to a new frame 
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

#Class for the main menu
class MenuPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        
        self.configure(width = sWidth, height = sHeight,bg = "#000000")        
        
        #Add title to the screen
        title = tk.Label(self, text = "The Atomic Models", height = 2, width = 17, bg= "#000000", fg = "#FFFFFF")
        title.config(font=("Courier", 35))
        title.place(x=275, y=25)       
    
        #Create buttons for start, help, sources and quitting
        btnStart = tk.Button(self, text = "Start", command = lambda: master.switch_frame(StartPage))   
        btnSettings = tk.Button(self, text = "Help", command = lambda: master.switch_frame(HelpPage))    
        btnSources = tk.Button(self, text = "Sources", command = lambda: master.switch_frame(SourcePage))    
        btnQuit = tk.Button(self, text = "Quit", command = master.destroy)    
        buttons = [btnStart,btnSettings, btnSources, btnQuit]
    
        #Configure buttons and add to the screen
        start_y = 170    
        for btn in buttons:
            btn.config(font=("Courier", 30), bg= "#FFFFFF",  height = 1, width = 8) 
            btn.place(x=420, y = start_y)
            start_y += 110    
    
        self.loadGif("img/Atomic Model.gif") #Load the gif    
        
        #Add name
        name = tk.Label(self, text = "By Nikil Patel", height = 2, width = 16, bg = "#000000", fg = "#FFFFFF")
        name.config(font=("Courier", 20))
        name.place(x=700, y = 600)
        
        #Add image of rutherford
        self.img = ImageTk.PhotoImage(Image.open("img/rutherford.png"))
        panel = tk.Label(self, image = self.img, borderwidth = 0)
        panel.place(x=700, y = 230)
        
       
    #Load a gif for the model    
    def loadGif(self, file):
        frameCnt = 35 #Number of frames of the gif
        frames = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frameCnt)] #Store each frame of the gif
        
        #Update the window for each frame
        def update(ind):
            frame = frames[ind]
            ind += 1
            if ind == frameCnt:
                ind = 0
            
            label.configure(image = frame)
            self.after(75, update, ind)
        
        label = tk.Label(self, image = frames[0], borderwidth=0)
        label.place(x=40,y=200)    
        self.after(0, update, 0)
        

#Class for the start page
class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)        
        self.configure(width = sWidth, height = sHeight,bg = "#000000")
        
        #Add titles for each option               
        tk.Label(self, text="Simulation", height = 2, width = 17, bg= "#000000", fg = "#FFFFFF", font=("Courier", 30)).place(x= 75, y = 100)           
        tk.Label(self, text="Derivation", height = 2, width = 17, bg= "#000000", fg = "#FFFFFF", font=("Courier", 30)).place(x= 550, y = 100)
                
        #Destroy all frames and load the pygame window.
        #Once the window is exited, reload the GUI.
        def Simulation():
            master.destroy()
            Run()
            main()
        
        #Add image 
        self.img = ImageTk.PhotoImage(Image.open("img/bulletandpaper.png"))
        #Button to start the simulation
        tk.Button(self, text="Simulate", command=lambda: Simulation(), image = self.img).place(x = 75, y = 270)        
              
        #Button to start the derivation
        self.img2 = ImageTk.PhotoImage(Image.open("img/derivationimg.jpg"))
        tk.Button(self, text="Derivation",image = self.img2, command=lambda: master.switch_frame(DerivationPage)).place(x = 600, y = 240)       
        
        #Button to return to the start page
        self.btn = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(MenuPage))
        self.btn.config(font=("Courier", 15), bg= "#FFFFFF",  height = 1, width = 20) 
        self.btn.place(x = 100, y = 650)

#Class for the page displaying sources
class SourcePage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(width = sWidth, height = sHeight,bg = "#000000")
        
        #Add title to the screen
        self.title = tk.Label(self, text = "Sources Page", height = 2, width = 17, bg= "#000000", fg = "#FFFFFF")
        self.title.config(font=("Courier", 40))
        self.title.place(x=240, y=25)  
        
        #Read in file contents 
        file = open("text/sources.txt", "r")        
        sources = file.read()        
        file.close()

        #Add text box with sources
        self.source_box = tk.Text(self, width = 80, height = 18, padx = 20, pady = 20, font=("Courier", 12))
        self.source_box.insert(5.0, sources)  
        self.source_box.tag_configure("center", justify = "center") #Centre align
        self.source_box.tag_add("center", 1.0, "end")
        self.source_box.config(state="disabled")  #Stop from being editted  
        self.source_box.place(x = 100, y= 150)
        
        
        #Add button to return to main menu
        self.btn = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(MenuPage))
        self.btn.config(font=("Courier", 15), bg= "#FFFFFF",  height = 1, width = 20) 
        self.btn.place(x = 100, y = 650)
                        

#Class for the page displaying help instructions                       
class HelpPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(width = sWidth, height = sHeight,bg = "#000000")
        
        #Add title to the screen
        self.title = tk.Label(self, text = "Help Page", height = 2, width = 17, bg= "#000000", fg = "#FFFFFF")
        self.title.config(font=("Courier", 40))
        self.title.place(x=240, y=25)  
        
        #Read in file contents 
        file = open("text/help.txt", "r")        
        sources = file.read()        
        file.close()

        #Add text box with sources
        self.source_box = tk.Text(self, width = 90, height = 18, padx = 20, pady = 20, font=("Courier", 13))
        self.source_box.insert(5.0, sources)  
        self.source_box.config(state="disabled")  #Stop from being editted  
        self.source_box.place(x = 50, y= 150)
        
        
        #Add button to return to main menu
        self.btn = tk.Button(self, text="Return to start page", command=lambda: master.switch_frame(MenuPage))
        self.btn.config(font=("Courier", 15), bg= "#FFFFFF",  height = 1, width = 21) 
        self.btn.place(x = 100, y = 650) 
        

#Class for displaying the derivation steps                
class DerivationPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.configure(width = sWidth, height = sHeight,bg = "#000000")       
           
        self.slide = 1 #Holds the current slide number
        self.totalImgs = 14 #Holds the number of the last slide to reset slide count
        
        #Add button to go to previous slide
        self.btn = tk.Button(self, text="Previous", command= lambda:self.previousPanel())
        self.btn.config(font=("Courier", 15), bg= "#FFFFFF",  height = 1, width = 21) 
        self.btn.place(x = 20, y = 690)   
        
        #Add button to go to next slide
        self.btn = tk.Button(self, text="Next", command= lambda: self.nextPanel())
        self.btn.config(font=("Courier", 15), bg= "#FFFFFF",  height = 1, width = 21) 
        self.btn.place(x = 700, y = 690)  

        #Add button to return to the start page
        self.btn = tk.Button(self, text="Exit", command=lambda: master.switch_frame(StartPage))
        self.btn.config(font=("Courier", 15), bg= "#FFFFFF",  height = 1, width = 21) 
        self.btn.place(x = 20, y = 10) 
        
        #Display the image of each slide 
        self.img = ImageTk.PhotoImage(Image.open("img/page" + str(self.slide) + ".jpg"))
        self.panel = tk.Label(self, image = self.img, borderwidth = 0)
        self.panel.place(x= 20, y = 50)
     
    #Change to the next slide
    def nextPanel(self):        
        if self.slide < self.totalImgs: #Only update if there is a next slide
            self.slide += 1
        else:
            self.slide = 1 #Reset the slide count
            
        #Display the slide
        self.img = ImageTk.PhotoImage(Image.open("img/page" + str(self.slide) + ".jpg"))
        self.panel.config(image = self.img)
    
    def previousPanel(self):        
        if self.slide != 1:
            self.slide -= 1
        else:
            self.slide = self.totalImgs #Return to the last slide when on the first slide 
         
        #Display the slide
        self.img = ImageTk.PhotoImage(Image.open("img/page" + str(self.slide) + ".jpg"))
        self.panel.config(image = self.img)
    
#Main 
def main():
    app = GUI()
    app.mainloop()
    
main()