import pygame
import random
import math

#Constants
WIDTH = 1280
HEIGHT = 960
FPS = 30
SCALE = 0.3 #Use to scale the nucleus and alpha particle dimensions together

#Colours
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN  = (0,255,0)
GREY = (128,128,128)
YELLOW = (255,255,0)
BLACK = (0,0,0)
ORANGE = (255, 69, 0)

pygame.init()

winHeight= pygame.display.Info().current_h #Get the current height
winWidth = int( 4 * (winHeight / 3)) #Get the corresponding width in 4:3
SCALEX = winWidth/1440 #Scales x coordinates to the correct ratio
SCALEY = winHeight/1080 #Scales y coordinates to the correct ratio

#Load in sprites
particleSprite = pygame.image.load("img/alphaparticle.png")
particleSprite = pygame.transform.scale(particleSprite,(int(103 * SCALE * (SCALEX)), int(102 * SCALE * (SCALEY))))

nucleusSprite = pygame.image.load("img/goldnucleus.png")
nucleusSprite = pygame.transform.scale(nucleusSprite, (int(288 * SCALE * (SCALEX)),int(277 * SCALE * (SCALEY))))

#Class for nucleus of foil atoms
class Nucleus:
    def __init__(self,x,y):
        self.x = x 
        self.y = y 
        self.field = 160  * (SCALEX * SCALEY) #Radius of the nucelus hitbox
        self.width = int(288 *SCALE * (SCALEX) )
        self.height = int(277 *SCALE * (SCALEY) )
        self.centre = [int(self.x + (0.5* self.width)), int(self.y + (0.5* self.height))] #Centre of the nucleus
    
    #Draw nucleus particles with a hitbox    
    def draw(self, win):        
        #pygame.draw.circle(win,BLUE, (int(self.x + (0.5 * self.width)), int(self.y + (0.5*self.height))), self.field, 3) #Draw hitbox
        #Draw sprite        
        win.blit(nucleusSprite,(self.x,self.y))
            

#Class for alpha particles
class Particle:
    def __init__(self,x,y):
        #x,y position
        self.x = x
        self.y = y
        
        #Components of velocity
        self.velx = 0 
        self.vely = -4 
        
        self.field = int(16*(SCALEX)) #Radius of the particle hitbox
        
        #Dimensions of the sprite
        self.width = int(103 *SCALE *SCALEX)
        self.height = int(102 *SCALE *SCALEY)
        
        self.centre = [self.x + (0.5* self.width), self.y + (0.5* self.height)] #Centre of the alpha particle
        
        #self.colour = YELLOW #Default hitbox colour
        
        self.collide = False #True if the alpha particle has collided
        #x,y coordinates of the nucelus it collided with 
        self.collidex = 0
        self.collidey = 0
                
        self.stopcollide = False #Stores if we should stop scattering (i.e. no longer change the components of velocity)        

        self.trail = [] #Holds previous (x,y) positions for drawing a trail
        self.trailcol = GREEN #Default colour for the trail, green if not collided, orange if collided
    
    #Draw alpha particles with a hitbox    
    def draw(self, win):
        
        #pygame.draw.circle(win,YELLOW, (int(self.centre[0]), int(self.centre[1])), self.field , 4) #Draw hitbox
        
        #Change x,y coordinates
        if movePart:
            self.move()

        #Update the position of the centre
        self.centre[0] = self.x + (0.5* self.width)
        self.centre[1] = self.y + (0.5* self.height)
        
        #Show to trail left behind by the particle
        if showTrail:
            for trail in self.trail:
                pygame.draw.circle(win, self.trailcol, trail, 3)
        
        #Display the sprite
        win.blit(particleSprite,(self.x ,self.y))       

    
    #Movement of particles
    def move(self):      
        
        #If the particle has collided and its velcity has not been changed
        if self.collide and not self.stopcollide:
            self.collision()
            self.trailcol = ORANGE #Change the trail colour when scattered
          
        #Update x,y
        self.x += self.velx 
        self.y += self.vely
        
        #Add the previous position to display a trail left behind
        self.trail.append((int(self.centre[0]), int(self.centre[1])))
        
    #Changes the components of velocity of the particle when it is scattered
    #Works by reading in predefined scattering angles from "angles.txt" to update the components of 
    #Velocity so that the particle moves along the angle 
    
    #The angles in "angles.txt" correspond to incident angles going up in multiples of 5
    #e.g. the second angle in the file corresponds to the scattering angle when the particle is incident at 5 degrees    
    
    def collision(self):
        
        #Read the file
        file = open("text/angles.txt", "r")
        lines = file.readlines()
        file.close()
        
        #Calculate the x and y distances from the nucleus and alpha particle centres
        dx = abs(self.centre[0] - self.collidex)
        dy = abs(self.centre[1] - self.collidey)
        
        #Calculate incident angle in radians
        incidentAngle = math.atan(dx/dy)
        
        #Identify the index of the scattering angle by converting from radians to degrees and storing the quotient when divided by 5
        index = ((180/math.pi) * incidentAngle) // 5
        
        #Convert the scatttering angle to radians
        scatteringAngle =  (math.pi / 180) *  int(lines[int(index)]) 
        
        #Calculate the new components of velocity
        #If the alpha particle is incident to the left of the nucleus' centre then it will deflect to the left
        #Therefore the x velocity must be negative
        if self.x < self.collidex:
            self.velx = -5 * math.sin(scatteringAngle) 
            self.vely = 5* math.cos(scatteringAngle) 
        else:
            self.velx = 5 * math.sin(scatteringAngle) 
            self.vely = 5 * math.cos(scatteringAngle) 
        
        #No longer change the velocities
        self.stopcollide = True          

        
#Updates the window each tick
def redrawWindow(win, particles, nuclei, screen, buttons):    
    
    win.fill((0, 0, 0))
    
    #Draw the bounding rectangle
    pygame.draw.rect(win, WHITE, (250,0, winWidth - 251 , winHeight), 2)   
    
    #Draw all particles
    for particle in particles:       
        particle.draw(win)
                      
    #Draw all nuclei, change the hitbox depending on the foil used
    for nucleus in nuclei:
        if goldFoil: 
            if micaSheets == 0:
                nucleus.field = 160 
            elif micaSheets == 1:
                nucleus.field = 180
            else:
                nucleus.field = 200
                
        if silverFoil:
            if micaSheets == 0:
                nucleus.field = 95
            elif micaSheets == 1:
                nucleus.field = 106
            else:
                nucleus.field = 119
                
        nucleus.field = int(nucleus.field *(SCALEX))
        nucleus.draw(win)       
  
    #Add Text and buttons
    myfont = pygame.font.SysFont('Courier', int(30 * SCALEY))
    text = ["Start","Reset", "Trail", "Gold", "Silver", "Zero", "One", "Two"]
    
    #Change the text of the start button depending on if it has been pressed
    if movePart:
        text[0] = "Pause"
    else:
        text[0] = "Start" 
        
    #Display text    
    textsurface = myfont.render("Select Foil", True, WHITE)    
    win.blit(textsurface,(30 * SCALEX, 450 * SCALEY))
    
    textsurface = myfont.render("Mica Sheets", True, WHITE)    
    win.blit(textsurface,(12 * SCALEX, 690 * SCALEY))
    
    #Change the colour of the buttons to grey if they are selected
    for i in range(len(buttons)):        
        if i== 2 and showTrail:
            pygame.draw.rect(win, GREY, buttons[i])
        elif i== 3 and goldFoil:
            pygame.draw.rect(win, GREY, buttons[i])
        elif i== 4 and silverFoil:
            pygame.draw.rect(win, GREY, buttons[i])                
        elif micaSheets == 0 and i == 5:
            pygame.draw.rect(win, GREY, buttons[i])
        elif micaSheets == 1 and i == 6:
            pygame.draw.rect(win, GREY, buttons[i])
        elif micaSheets == 2 and i == 7:
            pygame.draw.rect(win, GREY, buttons[i])
        else:
            pygame.draw.rect(win, WHITE, buttons[i])          
        
        #Add text to buttons
        textsurface = myfont.render(text[i], True, BLACK)    
        win.blit(textsurface,(buttons[i].left + (0.25 * buttons[i].w), buttons[i].top + (0.25 * buttons[i].h)))  
     
    #Scale the screen to fit with the resolution of the current screen
    resized_screen = pygame.transform.scale(win, (winWidth, winHeight)) 
    
    screen.blit(resized_screen, (0, 0))
    
    pygame.display.update()       


#Add particles and nuclei
def addObjects():
    particles = []
    
    """ #FOR TESTING
    for i in range(55):
        particles.append(Particle(550 + 10*i, 700))
    """
    
    #Add nuclei
    nuclei = []
    nuclei.append(Nucleus( 250 + int((winWidth-250)/2) , int(winHeight/2) - 100) )
   
    return particles, nuclei

#Detect if the particle in in range of the nucleus, returns true if collided
def detectCollision(particle, nucleus):
    
    #Calculate euclidean distance
    dist = math.sqrt( (particle.centre[0] - nucleus.centre[0])**2 + (particle.centre[1] - nucleus.centre[1])**2 )
    
    #Colour the hitbox red if it has collided
    if dist < particle.field + nucleus.field:
        return True
    else:
        return False      

#Add buttons to the buttons list
def addButtons(win):
    buttons = []
    buttons.append(pygame.Rect((30, 50 * SCALEY, 250 - 60, 75 * SCALEY))) #Start/Pause button
    buttons.append(pygame.Rect((30, 200 * SCALEY, 250-60, 75 * SCALEY))) #Reset button
    buttons.append(pygame.Rect((30, 350 * SCALEY, 250-60, 75 * SCALEY))) #Traces button
    buttons.append(pygame.Rect((30, 500 * SCALEY, 250-60, 75 * SCALEY))) #Gold Nuclei
    buttons.append(pygame.Rect((30, 585 * SCALEY, 250-60, 75 * SCALEY))) #Silver Nucleu
    buttons.append(pygame.Rect((30, 740 * SCALEY, 250-60, 75 * SCALEY))) #Mica windows 1 
    buttons.append(pygame.Rect((30, 825 * SCALEY, 250-60, 75 * SCALEY))) #Mica windows 2
    buttons.append(pygame.Rect((30, 910 * SCALEY, 250-60, 75 * SCALEY))) #Mica windows 3
 
    return buttons
    
       
#Main Simulation
def Run():

    #Global variables
    global winHeight , winWidth  #Actual width and height of the screen
    global movePart  #Uses for starting and pausing, if true then start the sim
    global showTrail  #True if the alpha particle trail is to be displayed
    global goldFoil, silverFoil  #True if using the selected foil
    global micaSheets  #Current number of selected mica sheets
    
    movePart = False
    showTrail = False
    goldFoil = True
    silverFoil = False

    WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #WIN is the surface we add to
    SCREEN = pygame.display.set_mode((winWidth, winHeight)) #SCREEN is the surface which displays a scaled version of WIN
    pygame.display.set_caption("Rutherford's Scattering Experiment") #Title
    
    run = True
    clock = pygame.time.Clock()
    
    particles, nuclei = addObjects() #Add particles and nuclei
    
    buttons = addButtons(WIN) #Add buttons
    
    micaSheets = 0 #Currently selected mica sheets
    tempSheets = 0 #Previously selected mica sheets 

    changeVel = True #Stores if the velocity must be changed when selecting the number of mica sheets 
    
    timer = 0 #Stores after how many iterations should more particles be added
    
    #Main game loop
    while run:
        clock.tick(FPS)
              
        #Event handling
        for event in pygame.event.get(): #Quittung
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: 
                mouse_pos = event.pos
                
                for i in range(len(buttons)):
                    if buttons[i].collidepoint(mouse_pos):#Detect collision
                        
                        if i==0: #Start/Pause Simulation
                            movePart = not movePart
                                
                        if i == 1: #Restart Simulation                            
                            particles.clear()
                            nuclei.clear()
                            particles, nuclei = addObjects()
                        
                        if i==2: #Show trail
                           showTrail = not showTrail 
                           
                        if i == 3 and not movePart: #Select gold foil
                            goldFoil = True
                            silverFoil = False
                        
                        if i == 4 and not movePart: #Select silver foil
                            goldFoil = False
                            silverFoil = True
                        
                        if i == 5 and not movePart: #Select 0 mica sheet
                            tempSheets = micaSheets
                            micaSheets = 0
                            changeVel = True
                        
                        if i ==6 and not movePart: #Select 1 mica sheet
                            tempSheets = micaSheets
                            micaSheets = 1
                            changeVel = True
                        if i == 7 and not movePart: #Select 2 mica sheet
                            tempSheets = micaSheets
                            micaSheets = 2
                            changeVel = True
                                    
        #Add alpha particles
        if movePart:
            if (timer % 50) == 0:
                pos = [0]
                for i in range(random.randint(1,5)): #Generate 1 to 4 particles 
                    posx = random.randint(350, winWidth - 150) #Generate random x position
                    posy = posx % 10
                    
                    while posx in pos: #Generate a new x coordinate if the same one has already been used 
                        posx = random.randint(350, winWidth - 150)
                    
                    particles.append(Particle(posx, winHeight - (10 + posy))) #Add particles to list
                    
                timer = 0 
        
                                
                
        #Remove particles which are off the screen
        for particle in particles:            
            if (particle.x > winWidth) or (particle.x < 250) or (particle.y <0) or (particle.y>winHeight):
                particles.pop(particles.index(particle))
             
        #Check for collisions of particles and nucleus           
        for particle in particles:
            for nucleus in nuclei:
                collide = detectCollision(particle, nucleus)                
                if(collide):
                    #particle.colour = RED #Change hitbox colour to red
                    particle.collide = True
                    particle.collidex = nucleus.centre[0] 
                    particle.collidey = nucleus.centre[1]
                    break
                else:
                    #particle.colour = YELLOW #Change hitbox colour to yellow
                    particle.collide = False
         
        #If a new mica sheet has been selected
        if changeVel:
            for particle in particles:             
                if int(particle.vely) != -4: #Reset the velocities to their previous values                            
                    particle.velx /= (1- (0.1 * tempSheets))
                    particle.vely /= (1- (0.1 * tempSheets))
                
                #Calculate the new velocities
                particle.velx *= (1- (0.1 * micaSheets))
                particle.vely *= (1- (0.1 * micaSheets))
                
                #Dont change the velocity until a new sheet is selected
                changeVel = False

                
        timer += 1     
        #Redraw the window
        redrawWindow(WIN, particles, nuclei, SCREEN, buttons)

    pygame.quit()
    
#REMOVE WHEN FINISHED TESTING 
#Run()