import wiiboard
import pygame
import time
import liblo
import sys

# modified from wiiboard-simple
# Author : Sylvain Hanneton 2011
# 24 sept. 2011

def main():

    pygame.init()   
    board = wiiboard.Wiiboard()
    address = board.discover()
    board.connect(address) #The wii board must be in sync mode at this time
    
    # initializations
    time.sleep(0.1)
    board.setLight(True)
    done = False
    weight_threshold = 10
    
    try :
        target = liblo.Address(1234)
    except liblo.AddressError, err:
        print str(err)
        sys.exit()
            
    # Initialisation
    init_time = time.time()
        
    # MAIN LOOP
    while (not done):
        time.sleep(0.05)
        for event in pygame.event.get():
            if event.type == wiiboard.WIIBOARD_MASS:
                if (event.mass.totalWeight > weight_threshold):  
                    total = event.mass.totalWeight
                    x = ((event.mass.topRight + event.mass.bottomRight) - (event.mass.topLeft + event.mass.bottomLeft))/total
                    y = ((event.mass.topRight + event.mass.topLeft) - (event.mass.bottomRight + event.mass.bottomLeft))/total
                    t = (time.time()-init_time)
                    if ((event.mass.topRight==0) or (event.mass.topLeft==0) or (event.mass.bottomLeft==0) or (event.mass.bottomRight==0)) :
                        error = 1
                    else:
                        error = 0

                    liblo.send(target,"/wiiboard/weight",t,error,event.mass.totalWeight)
                    liblo.send(target,"/wiiboard/sensors",t,event.mass.topLeft,event.mass.topRight,event.mass.bottomLeft,event.mass.bottomRight)
                    liblo.send(target,"/wiiboard/XY",t,error,x,y)

            # The BUTTON event activates recording
            elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
                   print "Button pressed!"
                   board.disconnect()
                   done = True                      
                   pygame.quit()


            #elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
                    
            #Other event types:
            #wiiboard.WIIBOARD_CONNECTED
            #wiiboard.WIIBOARD_DISCONNECTED

    
    pygame.quit()

#Run the script if executed
if __name__ == "__main__":
    main()
