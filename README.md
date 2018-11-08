# stage_2A
The purpose of this project is to make a hyperscanningtool from the following elements:

- 2 wiifit balance board 
- 2 linux computer it can be 2 raspberry pi for example. 
- 1 computer to manage all calculations (better if it work on unix)

This project uses the following technologies: Python network programming, Processing(Java), Puredata 

On raspberry pi must be run with python2.7 the following scripts: stabilowii_*.py. Stabilowii scripts use a wiiboard.py script to manage the connection and reception of data from the boards. 

It is necessary to first launch servers 1 and 2 on the computer to receive the data extract by the 2 raspberry pi.  

Also, you have to launch puredata to obtain the sound feedback (sound_distorsion_com.pd) and processing to obtain the visual feedback (sketch_sphere_lisse_communication.pde). 

Finally, you must launch wii_visual.py which allows you to display the graphs. The latter uses pyqtgraph on python3.6

When all the script are setup you can push button on each board and go on it.  You will see all the scripts working together. 



######## 
Several areas for improvement can be considered, such as standardizing the languages used (all in Python) and moving to object programming for greater efficiency and readability.
