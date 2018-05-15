import wiiboard
import pygame
import time
import curses

# modified from wiiboard-simple
# Author : Sylvain Hanneton 2011
# 24 sept. 2011

def main():
	board = wiiboard.Wiiboard()

	pygame.init()
	
	address = board.discover()
	board.connect(address) #The wii board must be in sync mode at this time
	
	# initializations
	time.sleep(0.1)
	board.setLight(True)
	done = False
	time_limit = 40
	weight_threshold = 3
	recording = False
	screen = curses.initscr()
	
	# MAIN LOOP
	while (not done):
		time.sleep(0.05)
		for event in pygame.event.get():
			if event.type == wiiboard.WIIBOARD_MASS:
				if (event.mass.totalWeight > weight_threshold):  
					if recording : 
						total = event.mass.totalWeight
						x = ((event.mass.topRight + event.mass.bottomRight) - (event.mass.topLeft + event.mass.bottomLeft))/total
 						y = ((event.mass.topRight + event.mass.topLeft) - (event.mass.bottomRight + event.mass.bottomLeft))/total
						output_file.write(`time.time()-init_time`+'\t')
						output_file.write(`event.mass.totalWeight`+'\t')
						output_file.write(`event.mass.topLeft`+'\t')
						output_file.write(`event.mass.topRight`+'\t')
						output_file.write(`event.mass.bottomLeft`+'\t')
						output_file.write(`event.mass.bottomRight`+'\t')
						output_file.write(`x`+'\t')
						output_file.write(`y`+'\n')
						output_file.flush() 

						# End of recording ?
						if ((time.time()-init_time)>time_limit):
							recording = False 
							print "End of recording"
							output_file.close()
							curses.beep()

			# The BUTTON event activates recording
			elif event.type == wiiboard.WIIBOARD_BUTTON_PRESS:
				print "Button pressed!"

			elif event.type == wiiboard.WIIBOARD_BUTTON_RELEASE:
				if not recording :
					print "Button released -> recording...."
					curses.beep()
					output_filename = 'stab_' + time.asctime() + '.txt'
					print "Save data in " + output_filename		
					output_file = open(output_filename,'wt')
					output_file.write("Time\tWeight\tC_tl\tC_tr\tC_bl\tC_br\tX\tY\n") 
					init_time = time.time() 
					recording = True 
			
			# Press any key on the computer keyboard to quit
			elif event.type == pygame.QUIT:
				print "Quit !"
				output_file.close()
				done = True
			
			#Other event types:
			#wiiboard.WIIBOARD_CONNECTED
			#wiiboard.WIIBOARD_DISCONNECTED

	board.disconnect()
	pygame.quit()

#Run the script if executed
if __name__ == "__main__":
	main()
