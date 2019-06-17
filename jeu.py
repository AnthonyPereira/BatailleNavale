from tkinter import *
from tkinter import messagebox


def clicked1():
    root.destroy()
    import jeu1

def clicked2():
    root.destroy()
    import jeu2


root=Tk()

root.config(width=500, height=500)
#  centrage de la fenêtre sur l'écran
rootWidth = root.winfo_reqwidth()
rootHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - rootWidth / 2)
positionDown = int(root.winfo_screenheight() / 2 - rootHeight / 2)
root.geometry("+{}+{}".format(positionRight, positionDown))


root.title("Bienvenue dans Fort Boyard")

rootLabel= Label(root,text="Choisir contre qui jouer")
rootLabel.pack()

btn1=Button(root, text="IA 1", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=lambda: (clicked1()))
btn1.pack()
btn2=Button(root, text="IA 2", bg="white", fg="Black", width=8, height=4, font=('Helvetica', '20'), command=lambda: (clicked2()))
btn2.pack()

root.mainloop()