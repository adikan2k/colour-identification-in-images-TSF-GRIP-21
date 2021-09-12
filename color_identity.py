# IMPORT DEPENDANCIES

import cv2
import pandas as pd

# SETTING THE IMAGE AND CSV FILE PATH

img_path = "imagesample.jpg"
csv_path = 'colors.csv'

# READING THE CSV FILE

index = ['color', 'color_name', 'hex', 'R', 'G', 'B']   #column names for the csv file
df = pd.read_csv(csv_path, names=index, header=None)

# READING IMAGE

img = cv2.imread(img_path)
img = cv2.resize(img, (800,600))

# DECLARATION OF GLOBAL VARIABLES

clicked = False  #initial value
r = g = b = x_pos = y_pos = 0  #mouse pointer position

# FUNCTION TO CALCULATE MIN. DISTANCE FROM ALL COLOURS AND GET THE MATCHING COLOR

def get_color_name(R,G,B):
	minimum = 1000
	for i in range(len(df)):
		d = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
		if d <= minimum:
			minimum = d
			cname = df.loc[i, 'color_name']

	return cname

# FUNCTION TO GET THE X,Y CO-ORDINATES FROM MOUSE DOUBLE CLICK

def draw_function(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global b, g, r, xpos, ypos, clicked
		clicked = True
		xpos = x
		ypos = y
		b,g,r = img[y,x]
		b = int(b)
		g = int(g)
		r = int(r)

# CREATING THE IMAGE WINDOW

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:
	cv2.imshow('image', img)
	if clicked:
		#cv2.rectangle(image, startpoint, endpoint, color, thickness)-1 fills entire rectangle
		cv2.rectangle(img, (20,20), (600,60), (b,g,r), -1)

		#Creating text string to display( Color name and RGB values )
		text = get_color_name(r,g,b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)
		#cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
		cv2.putText(img, text, (50,50), 2,0.8, (255,255,255),2,cv2.LINE_AA)

		#For very light colours we will display text in black colour
		if r+g+b >=600:
			cv2.putText(img, text, (50,50), 2,0.8, (0,0,0),2,cv2.LINE_AA)

	if cv2.waitKey(20) & 0xFF == 27:
		break

cv2.destroyAllWindows()