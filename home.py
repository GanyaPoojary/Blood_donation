from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow
import os

main = Tk()
main.geometry("1366x768")
main.title("BLOOD DONATION")
main.resizable(0, 0)

def Exit():
    sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=main)
    if sure:#close the window
        main.destroy()

main.protocol("WM_DELETE_WINDOW", Exit)
#user attempt to close the window
#exit function is triggered


def adm():
    main.withdraw()
    os.system("python adminsignin.py")
    main.deiconify()

def user():
    main.withdraw()
    os.system("python usersignin.py")
    main.deiconify()


# Load and resize the background image
background_image = Image.open("./b3.png")
background_image = background_image.resize((1366, 768), Image.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)#convert the image to format suitable for display in lbl
label1 = Label(main, image=background_photo)
label1.place(relx=0, rely=0, width=1366, height=768)

button1 = Button(main, text='Admin', font='bold',relief="flat", overrelief="flat", activebackground="black", cursor="hand2", foreground="black", background="White", borderwidth="0", command=adm)
button1.place(relx=0.316, rely=0.446, width=146, height=90)

button2 = Button(main, text='User',font='bold', relief="flat", overrelief="flat", activebackground="#ffffff", cursor="hand2", foreground="black", background="White", borderwidth="0", command=user)
button2.place(relx=0.566, rely=0.448, width=146, height=90)
#event loop will be started
main.mainloop()