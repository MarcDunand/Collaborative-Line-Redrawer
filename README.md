# Collaborative Line Redrawer
 Original version of my collaborative drawer. Instead of drawing directly onto a hand draw line, it detects a hand drawn line from an image, and redraws that line plus doodles onto a new sheet of paper.




This project turns hand-drawn line into an axidraw-ready SVG of a landscape whos terrain is defined by the hand-drawn line.

1: Draw your line, it must be a function
2: Take a picture of your line such that:
	a: the line clips of both ends of the image
	b: the image is brightly lit with no shadows
	c: the proportions of the image closely resembly 8.5x11
3: Open ./lineFinder/sketch_240205a
	a: change the read path such that it is retrieving the image you saved on your hard drive
	b: change the size of the canvas so that it matches the pixels of your image
4: Make sure that you have vpype and vsketch installed
	a: input 'vsk run collaborativeLineRedrawer'
	b: vpype viewer should open
5: Open the DoodleAdder (not needed unless you want to change the behavior of the doodle adder)
6: You can click randomize in the vpype viewer to change the seed
7: Once you are satisfied you can click 'LIKE!' and a SVG will be saved in the output folder of HW4
8: Navigate to the output folder of HW4
9: Enter 'vpype read *INPUT*.svg linemerge --tolerance 0.1mm linesort crop 0.1in 0.1in 10.9in 8.4in write *OUTPUT*.svg'
	a: this connects svg line endpoints that are on top of each other and adds a margin. You can change the margin by changing the inch numbers.
10: This will make a new inkscape ready SVG that will plot on 8.5x11 paper.
11: Plot the output!