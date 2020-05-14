import tkinter as tk
import urllib.request

from PIL import ImageTk, Image
from webptools import webplib as webp


def download(link: str):
    if link[-3:] == "ebp":
        urllib.request.urlretrieve(link, "./temp.webp")
        print(webp.dwebp("temp.webp", "picture.png", "-o"))
    else:
        urllib.request.urlretrieve(link, "./temp.jpg")
        im1 = Image.open("./temp.jpg")
        im1.save("picture.png")


class Viewer:
    def __init__(self, picture_url_list: list):
        self.root = tk.Tk()
        self.linkList = picture_url_list
        self.sum = 0
        self.iter = 0

    # GUI stuff
    def getNextLink(self):
        if len(self.linkList) == 0:
            return ""
        link = self.linkList.pop(0)
        return link

    def setList(self, listOfUrls):
        self.linkList = listOfUrls
        self.sum = 0
        self.iter = 0

    def isPersonFaceless(self):
        if (len(self.linkList) == 1) & (self.linkList[0].find("unknown.jpg") != -1):  # wyrzyca ludzi bez mordy
            return True

    def pictureBrowser(self):
        if self.isPersonFaceless():
            return 0
        display = ""
        label = ""
        self.root.title('TinderSwiPy- Do You like her? (AI learn)')

        def update_pic():
            next_pic = self.getNextLink()
            if next_pic == "":
                self.root.quit()
            else:
                download(next_pic)
                nonlocal display
                nonlocal label
                display = ImageTk.PhotoImage(Image.open("./picture.png"))
                label = tk.Label(self.root, image=display)
                label.grid(row=0, column=0, columnspan=3)

        update_pic()

        def swipeYes():
            self.sum += 1
            self.iter += 1
            update_pic()

        def swipeNo():
            self.iter += 1
            update_pic()

        def useless():
            self.sum += 0.5
            self.iter += 1
            update_pic()

        # Buttons
        yes_button = tk.Button(self.root, text="Yes", padx=10, pady=5, fg="white", bg="#263D42", command=swipeYes).grid(
            row=1, column=2)
        no_button = tk.Button(self.root, text="Nope", padx=10, pady=5, fg="white", bg="#263D42", command=swipeNo).grid(
            row=1, column=0)
        useless_button = tk.Button(self.root, text="It's not a human", padx=10, pady=5, fg="white", bg="#263D42",
                                   command=useless).grid(row=1, column=1)
        # Keys input
        self.root.bind("<Down>", lambda e: useless())
        self.root.bind("<Right>", lambda e: swipeYes())
        self.root.bind("<Left>", lambda e: swipeNo())
        self.root.mainloop()
        return self.sum / self.iter if self.iter != 0 else 0
