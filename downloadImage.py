from webptools import webplib as webp
import tkinter as tk
# sudo apt-get install python3-tk
from PIL import ImageTk, Image
import urllib.request
# from swiPy import *

# Global CONSTs
FileYesDir="./YES/"
FileNoDir="./NO/"
linkList=list()
linklistsize=0
# Globals
# def findCurrentFilename(directory):
#     pass
#
#
#
# currentYesName=findCurrentFilename(FileYesDir)
# currentNoName=findCurrentFilename(FileNoDir)

def download(link: str):
    if (link[-3:]=="ebp"):
        urllib.request.urlretrieve(link,"temp.webp")
        print(webp.dwebp("temp.webp", "picture.png", "-o"))
    else:
        urllib.request.urlretrieve(link,"temp.jpg")
        im1 = Image.open("temp.jpg")
        im1.save("picture.png")



# GUI stuff

def getNextLink():
    global linkList
    if(len(linkList)==0):
        return ""
    link=linkList.pop(0)
    print(link)
    return link

def setList(list):
    global linkList
    global linklistsize
    linkList=list
    linklistsize=len(linkList)
    return pictureBrowser()


def pictureBrowser():
    sum=0
    iter=0
    root= tk.Tk()
    root.title('TinderSwiPy- Do You like her? (AI learn)')

    def update_pic():
        next=getNextLink()
        global sum
        global iter
        if (next==""): return sum/iter
        download(getNextLink())
        global display
        global label
        display = ImageTk.PhotoImage(Image.open("picture.png"))
        label = tk.Label(root, image=display)
        label.grid(row=0, column=0, columnspan=3)

    update_pic()

    def swipeYes():
        global sum
        sum+=10
        global iter
        iter+=1
        update_pic()
    def swipeNo():
        global iter
        iter+=1
        update_pic()
    def useless():
        global sum
        sum+=5
        global iter
        iter+=1
        update_pic()

    # Buttons
    yesButton = tk.Button(root, text="Yes", padx=10, pady=5, fg="white", bg="#263D42", command=swipeYes)
    yesButton.grid(row=1,column=2)
    noButton = tk.Button(root, text="Nope", padx=10, pady=5, fg="white", bg="#263D42", command=swipeNo)
    noButton.grid(row=1,column=0)
    uselessButton = tk.Button(root, text="It's not a human", padx=10, pady=5, fg="white", bg="#263D42", command=useless)
    uselessButton.grid(row=1,column=1)
    # Keys input
    root.bind("<Down>", lambda e: useless())
    root.bind("<Right>", lambda e: swipeYes())
    root.bind("<Left>", lambda e: swipeNo())

    root.mainloop()
# driver = swiPy.Facebook_login()
# swiPy.real_user_stare()
# swiPy.Tinder_login(driver)
# swiPy.Close_popup(driver)
# swiPy.real_user_stare()
# swiPy.Swipe_it(driver)
download("")
pictureBrowser()