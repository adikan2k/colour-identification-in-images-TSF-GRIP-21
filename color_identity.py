#IMPORT DEPENDANCIES
import cv2
import pandas as pd

#GLOBAL VARIABLES DECLARATION
global img,ret
clicked = False
r = g = b = x_pos = y_pos = 0

#declaring the mode of operation
#to detect the colour in the real time video change the mode in to 'video'

mode='video'

# READING THE CSV FILE WITH PANDAS
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# function to calculate minimum distance i.e. minimum difference from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

if mode=='video':
    cap=cv2.VideoCapture(0)
elif mode=='image':
    img=cv2.imread('colour_image.jpg')

while True:

    if mode=='video':

        ret, img = cap.read()
        img = cv2.flip(img, 1)

    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_function)


    cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

    # Creating text string to display( Color name and RGB values )
    text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

    #displaying the text on the image
    cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

    # For very light colours we will display text in black colour
    if r + g + b >= 600:
        cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)


    clicked = False

    cv2.imshow("image", img)
    # Break the loop when user hits 'esc' key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()