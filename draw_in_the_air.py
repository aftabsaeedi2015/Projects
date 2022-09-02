import numpy as np
import cv2
import keyboard
import tkinter as tk
from tkinter import ttk
import pyautogui

#moving the mouse according to the coordinates x,y
def move_mouse(x_position,y_position):
    pyautogui.moveTo(x_position,y_position,duration=0.05)
#this function contains all the functionality and is called when the button is clicked
def drawingApp (pointer_or_draw, obj_color, brush_color):
    flag=None
    x_prev = 0
    y_prev = 0
    new_x = 0
    new_y = 0
    color_choosen = 0

    def callback(x):
        print("")

    cv2.namedWindow("detect colors", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("detect colors", 500, 500)

    cv2.createTrackbar("Upper Hue", "detect colors", 180, 180, callback)
    cv2.createTrackbar("Upper Saturation", "detect colors", 255, 255, callback)
    cv2.createTrackbar("Upper Value", "detect colors", 255, 255, callback)
    cv2.createTrackbar("Lower Hue", "detect colors", 0, 180, callback)
    cv2.createTrackbar("Lower Saturation", "detect colors", 0, 255, callback)
    cv2.createTrackbar("Lower Value", "detect colors", 0, 255, callback)

    kernel = np.ones((5, 5), np.uint8)

    # canvas setup
    canvas = np.zeros((720, 1600, 3)) + 0
    cap = cv2.VideoCapture(0)
    #so when the point_or_draw is point we change the screen resolution and put the flat=0 so we can use it in pen color
    if pointer_or_draw.get()== 'point':
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        flag=0
    else:
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
    low_hsv =np.array([])
    upp_hsv = np.array([])

    # Keep looping
    while True:
        # Reading the frame from the camera
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if obj_color.get()=='my_own':
            upper_hue = cv2.getTrackbarPos("Upper Hue", "detect colors")
            upper_saturation = cv2.getTrackbarPos("Upper Saturation", "detect colors")
            upper_value = cv2.getTrackbarPos("Upper Value", "detect colors")
            lower_hue = cv2.getTrackbarPos("Lower Hue", "detect colors")
            lower_saturation = cv2.getTrackbarPos("Lower Saturation", "detect colors")
            lower_value = cv2.getTrackbarPos("Lower Value", "detect colors")
            upp_hsv = np.array([upper_hue, upper_saturation, upper_value])
            low_hsv = np.array([lower_hue, lower_saturation, lower_value])
        # if the color of the object is red
        elif obj_color.get()=="red" or keyboard.is_pressed('1'):
           cv2.setTrackbarPos("Upper Hue", "detect colors",180)
           cv2.setTrackbarPos("Upper Saturation", "detect colors",255)
           cv2.setTrackbarPos("Upper Value", "detect colors",255)
           cv2.setTrackbarPos("Lower Hue", "detect colors",0)
           cv2.setTrackbarPos("Lower Saturation", "detect colors",168)
           cv2.setTrackbarPos("Lower Value", "detect colors",65)
           upper_hue =        180
           upper_saturation = 255
           upper_value =      255
           lower_hue   =      0
           lower_saturation = 166
           lower_value  =     38
           upp_hsv = np.array([upper_hue, upper_saturation, upper_value])
           low_hsv = np.array([lower_hue, lower_saturation, lower_value])
           # if the color of the object is green
        elif obj_color.get()=="green" or keyboard.is_pressed('2'):
           cv2.setTrackbarPos("Upper Hue", "detect colors",126)
           cv2.setTrackbarPos("Upper Saturation", "detect colors",255)
           cv2.setTrackbarPos("Upper Value", "detect colors",255)
           cv2.setTrackbarPos("Lower Hue", "detect colors",51)
           cv2.setTrackbarPos("Lower Saturation", "detect colors",162)
           cv2.setTrackbarPos("Lower Value", "detect colors",81)
           upper_hue =        154
           upper_saturation = 255
           upper_value =      255
           lower_hue   =      51
           lower_saturation = 162
           lower_value  =     81
           upp_hsv = np.array([upper_hue, upper_saturation, upper_value])
           low_hsv = np.array([lower_hue, lower_saturation, lower_value])
        # if the color of the object is blue
        elif obj_color.get()=='blue' or keyboard.is_pressed('3'):
           cv2.setTrackbarPos("Upper Hue", "detect colors",180)
           cv2.setTrackbarPos("Upper Saturation", "detect colors",255)
           cv2.setTrackbarPos("Upper Value", "detect colors",255)
           cv2.setTrackbarPos("Lower Hue", "detect colors",90)
           cv2.setTrackbarPos("Lower Saturation", "detect colors",101)
           cv2.setTrackbarPos("Lower Value", "detect colors",107)
           upper_hue =        155
           upper_saturation = 255
           upper_value =      255
           lower_hue   =      99
           lower_saturation = 70
           lower_value  =     107
           upp_hsv = np.array([upper_hue, upper_saturation, upper_value])
           low_hsv = np.array([lower_hue, lower_saturation, lower_value])

        # in case user wants to select different favorite color then he can use the trackbar  he may use the trackbar

        mask = cv2.inRange(hsv, low_hsv, upp_hsv)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.dilate(mask, kernel, iterations=1)

        #finding the contours
        all_cnts, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        # If the contours are formed
        if len(all_cnts) > 0:
            # finding biggest contour
            max_cnt = sorted(all_cnts, key=cv2.contourArea, reverse=True)[0]
            # Getting the radius of the circle around
            ((x, y), radius) = cv2.minEnclosingCircle(max_cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 170, 255), 2)
            # Calculating the center of the detected contour
            M = cv2.moments(max_cnt)
            new_x = int(M['m10'] / M['m00'])
            new_y = int(M['m01'] / M['m00'])
            if brush_color.get()== 'red':
                color_choosen =  0, 0, 255
            elif brush_color.get()== 'green':
                color_choosen= 0, 255, 0
            elif brush_color.get()== 'blue':
                color_choosen= 255, 0, 0
            elif brush_color.get()== 'yellow':
                color_choosen= 0, 255, 255
            if keyboard.is_pressed('c') :
                canvas = np.zeros((720, 1600, 3)) + 0
            if flag==0 and keyboard.is_pressed('4'):
                pyautogui.click(x,y)
            elif flag==0 and keyboard.is_pressed('5'):
                pyautogui.doubleClick(x,y)


            #when the point_or_draw is point this will be extecuted
            if str(pointer_or_draw.get()) == "point":
                move_mouse(x,y)
            # If there were no previous points then save the detected put x_new and y_new in x1 and y1
            # This is true when we writing for the first time or when writing
            #if the value of the point_or_draw is draw this will be executed
            else:
                # Draw the line on the canvas
                canvas = cv2.line(canvas, (x_prev, y_prev), (new_x, new_y), color_choosen, 6)

            # After the line is drawn the new points become the previous points.
            x_prev, y_prev = new_x, new_y
            new_x = 0
            nwe_y = 0

            #displaying the windows
        if pointer_or_draw.get()=='draw':
            cv2.imshow('paint', canvas)
        # if obj_color.get()=='my_own':
            cv2.imshow('mask', mask)
        if obj_color.get()=='my_own':
            obj_detected = cv2.bitwise_and(frame,frame,mask=mask)
            # cv2.imshow('obj_detected',obj_detected)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()
    #end of the drawing app loop

# building the graphical user interface of the program
p_container = tk.Tk()
p_container.title("point or draw")
p_container.geometry('900x500')

# canvas1 = tk.Canvas(p_container, width = 700, height = 700)
# canvas1.pack()
# selecting the point or draw
label1 = ttk.Label(p_container, text ="choose pointer or draw : ", font = ("Times New Roman", 25)).grid(row = 3, column = 1, padx = 10, pady = 30)
choice1 = tk.StringVar()
dropdown1 = ttk.Combobox(p_container, width = 10, textvariable = choice1, font = ("Times New Roman", 25))
dropdown1['values'] = ('point', 'draw')
dropdown1.grid(column=2, row=3, padx = 100)
dropdown1.current(0)

#selecting the color of the object

label2 = ttk.Label(p_container,text = "color of object : ",font = ("Times New Roman", 25)).grid(row = 6,column = 1,padx = 20,pady = 30)
choice2 = tk.StringVar()
drowpdown2 = ttk.Combobox(p_container, width = 10, textvariable = choice2, font = ("Times New Roman", 25))
drowpdown2['values'] = ('red', 'green', 'blue','my_own')

drowpdown2.grid(column=2, row=6, padx = 10, pady=20)
drowpdown2.current(0)
print(choice1.get())

#selecting the color of the pencil
label3 = ttk.Label(p_container,text = "color of the brush : ",font = ("Times New Roman", 25)).grid(row = 8,column = 1,padx = 20,pady = 30)
choice3 = tk.StringVar()
dropdown3 = ttk.Combobox(p_container, width = 10, textvariable = choice3, font = ("Times New Roman", 25))
dropdown3['values'] = ('red', 'green', 'blue', 'yellow')

dropdown3.grid(column=2, row=8, padx = 10, pady=20)
dropdown3.current(0)
print(choice3.get())

#button we pass three params to the drawingApp function they are the choices the user made from the drop down menus
button = tk.Button(p_container,text="Run",height = 2,width=10,font = ("Times New Roman", 15),command= lambda : drawingApp(choice1,choice2,choice3)).place(x=330,y=350)
print(str(choice3))
p_container.mainloop()