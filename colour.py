from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os, shutil
from PIL import Image, ImageTk
import cv2  
import pandas as pd  # quick calculation
import argparse

class Root(Tk):
    def __init__(self):
        super(Root,self).__init__()
        self.title("COLOUR DETECTION")
        self.minsize(1280,730)
        self.img = Image.open("background.png")
        self.test = ImageTk.PhotoImage(self.img)
        self.labelimg = Label(self, image=self.test)
        self.labelimg.place(x=0, y=0)

        self.title = Label(self, text = "COLOUR DETECTION", font =("Times",24),fg = "black")
        self.title.place(x = 10, y = 10)
        self.button = Button(self, text="Select Image",font =("Times",12),bg = "black",fg = "white", command=self.fileDailog)
        self.button.place(x=50, y = 70,  width = 100, height = 30)

        self.button1 = Button(self, text="Select Image2",font =("Times",12),bg = "black",fg = "white", command=self.fileDailog2)
        self.button1.place(x=50, y = 120,  width = 100, height = 30)

        self.button2 = Button(self, text="Show Result",font =("Times",12),bg = "black",fg = "white",command = self.showResult)
        self.button2.place(x=50, y = 170,  width = 100, height = 30)
        #clicked = False
        r = g = b = xpos = ypos = 0
        index = ["color", "color_name", "hex", "R", "G", "B"]
        self.csv = pd.read_csv("colors.csv", names=index, header=None)
        self.cr = {1:[],2:[],3:[], 4:[],5:[],6:[]}
        
    def getColorName(self, R, G, B):
        minimum = self.max_distance
        for i in range(len(self.csv)):
            d = (
                abs(R - int(self.csv.loc[i, "R"]))
                + abs(G - int(self.csv.loc[i, "G"]))
                + abs(B - int(self.csv.loc[i, "B"]))
            )
            if d <= minimum:
                minimum = d
                cname = self.csv.loc[i, "color_name"]
        return cname


# function to get x,y coordinates of mouse double click
    def draw_function(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            global b, g, r, xpos, ypos, clicked
            clicked = True
            xpos = x
            ypos = y
            b, g, r = self.img[y, x]
            b = int(b)
            g = int(g)
            r = int(r)

    def fileDailog(self):
        
        self.fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File",filetype=(("jpeg","*.jpg"),("png","*.png")))
        self.img = cv2.imread(self.fileName)
        global clicked
        clicked = False

        height, width, _ = self.img.shape
        self.max_distance = height * width
        cv2.namedWindow("Photo")
        cv2.setMouseCallback("Photo", self.draw_function)
        
        while True:
            cv2.imshow("Photo", self.img)
            keyCode = cv2.waitKey(1)
            if clicked:
                cv2.rectangle(self.img, (20, 20), (750, 60), (b, g, r), -1)
                colorName = self.getColorName(r, g, b) + " R=" + str(r) + " G=" + str(g) + " B=" + str(b)
                #print(r,g,b)
                cv2.putText(self.img, colorName, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                if r + g + b >= 600:
                    cv2.putText(self.img, colorName, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

                clicked = False
            if cv2.getWindowProperty("Photo", cv2.WND_PROP_VISIBLE) <1: 
                R = r
                G = g 
                B = b
                self.cr[1].append(R)
                self.cr[2].append(G)
                self.cr[3].append(B)
                print(self.cr)
                break
        cv2.destroyAllWindows()


    def fileDailog2(self):
        self.fileName = filedialog.askopenfilename(initialdir = "/", title="Select A File",filetype=(("jpeg","*.jpg"),("png","*.png")))
        self.img = cv2.imread(self.fileName)
        global clicked
        clicked = False

        height, width, _ = self.img.shape
        self.max_distance = height * width
        cv2.namedWindow("Photo")
        cv2.setMouseCallback("Photo", self.draw_function)
        while True:
            cv2.imshow("Photo", self.img)
            keyCode = cv2.waitKey(1)
            if clicked:
                cv2.rectangle(self.img, (20, 20), (750, 60), (b, g, r), -1)
                colorName = self.getColorName(r, g, b) + " R=" + str(r) + " G=" + str(g) + " B=" + str(b)
                #print(r,g,b)
                cv2.putText(self.img, colorName, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

                if r + g + b >= 600:
                    cv2.putText(self.img, colorName, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

                clicked = False
            if cv2.getWindowProperty("Photo", cv2.WND_PROP_VISIBLE) <1:        
                R1 = r
                G1 = g 
                B1 = b
                self.cr[4].append(R1)
                self.cr[5].append(G1)
                self.cr[6].append(B1)
                
                print(self.cr)
                break
        cv2.destroyAllWindows()

    def showResult(self):
        label = Label(self, text=self.cr,font =("Times",12),bg = "black",fg = "white")
        label.place(x=470, y=310)
        if self.cr[1][0] > self.cr[4][0]:
            final_R1 = (self.cr[1][0] - self.cr[4][0])*100/self.cr[1][0]
        else:
            final_R1 = (self.cr[4][0] - self.cr[1][0]) * 100 / self.cr[4][0]

        final="{:.2f}".format(100-final_R1)
        label = Label(self, text=final + "%", font=("Times", 12), bg="black", fg="white")
        label.place(x=510, y=370)
        if self.cr[2][0] > self.cr[5][0]:
            final_R1 = (self.cr[2][0] - self.cr[5][0])*100/self.cr[2][0]
        else:
            final_R1 = (self.cr[5][0] - self.cr[2][0]) * 100 / self.cr[5][0]

        final="{:.2f}".format(100-final_R1)
        label = Label(self, text=final + "%", font=("Times", 12), bg="black", fg="white")
        label.place(x=510, y=400)
        if self.cr[3][0] > self.cr[6][0]:
            final_R1 = (self.cr[3][0] - self.cr[6][0])*100/self.cr[3][0]
        else:
            final_R1 = (self.cr[6][0] - self.cr[3][0]) * 100 / self.cr[6][0]

        final="{:.2f}".format(100-final_R1)
        label = Label(self, text=final + "%", font=("Times", 12), bg="black", fg="white")
        label.place(x=510, y=430)

        label = Label(self, text="Match Percent:", font=("Times", 12), bg="black", fg="white")
        label.place(x=470, y=340)
        label = Label(self, text="R: ", font=("Times", 12), bg="black", fg="white")
        label.place(x=470, y=370)
        label = Label(self, text="G: ", font=("Times", 12), bg="black", fg="white")
        label.place(x=470, y=400)
        label = Label(self, text="B: ", font=("Times", 12), bg="black", fg="white")
        label.place(x=470, y=430)


        

if __name__ == '__main__':
    root = Root()
    root.mainloop()