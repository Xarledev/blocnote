from ast import main
from cgitb import text
from cmath import e
from ctypes.wintypes import SIZE
from distutils import text_file
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *
from turtle import color, st
from tkinter import font
from unicodedata import name
from tkinter import colorchooser
import os, sys
import win32print
import win32api


fenetre = Tk(className='Nouveau text')
fenetre.geometry("1200x680")
fenetre.iconbitmap(r"C:\Users\Utilisateur\Desktop\Projet LibNote\img\logo.ico")
fenetre.configure(bg='#ffffff')

basicfont = font.Font(fenetre, ("Trajan Pro", 16))

global open_status_name
open_status_name = False

global selected
selected = False

def new_file():
    textbox.delete("1.0", END)
    fenetre.title("nouveau fichier")
    status_bar.config(text="nouveau fichier     ")
    global open_status_name
    open_status_name = False

def open_file():
    textbox.delete("1.0", END)
    text_file = filedialog.askopenfilename(initialdir="C:/", title="Ouvrir un fichier", filetypes=(("Text Files","*.txt"),("HTML Files",".html"),("PYTHON Files","*.py"),("ALL FILE","*.*")))
    if text_file:
        global open_status_name
        open_status_name = text_file
    name = text_file
    status_bar.config(text=f"{name}")
    name = name.replace("C:/","" )
    fenetre.title(f"{name} note")
    text_file = open(text_file, 'r')
    stuff = text_file.read()
    textbox.insert(END, stuff)
    text_file.close()

def save_as_file():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/", title="Enregister le fichier", filetypes=(("Text Files","*.txt"),("HTML Files",".html"),("PYTHON Files","*.py"),("ALL FILE","*.*") ))
    if text_file:
        name = text_file
        status_bar.config(text="nouveau fichier     ")
        name.replace("C:/", "")
        fenetre.title(f"{name} note")

        text_file = open(text_file, 'w')
        text_file.write(textbox.get(1.0, END))
        text_file.close

def save_file():
    global open_status_name
    if open_status_name :
        text_file = open(open_status_name, 'w')
        text_file.write(textbox.get(1.0, END))
        text_file.close

        status_bar.config(text="enregistrer     ")
    else:
        save_as_file()

mainframe = Frame(fenetre)
mainframe.pack(pady=5,)

toolbarr_frame = Frame(fenetre)
toolbarr_frame.pack(fill=X)

text_scroll =  Scrollbar(mainframe)
text_scroll.pack(side=RIGHT, fill=Y)

hor_scroll = Scrollbar(mainframe, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)
textbox = Text(mainframe, width=97, height=25, font=basicfont,undo=True,yscrollcommand=text_scroll.set, wrap='none', xscrollcommand=hor_scroll.set)
textbox.pack()

text_scroll.config(command=textbox.yview)
hor_scroll.config(command=textbox.xview)

def alert():
    showinfo("alerte", "Voulez vous enregister les modifications ?")

def cut_text(e):
    global selected
    if e:
        selected = fenetre.clipboard_get()
    else:
        if textbox.selection_get():
         selected = textbox.selection_get()
         textbox.delete("sel.first","sel.last")
        fenetre.clipboard_clear()
        fenetre.clipboard_append(selected)


def copy_text(e):
    global selected
    if e:
        selected = fenetre.clipboard_get()

    if textbox.selection_get():
        selected = textbox.selection_get()
        fenetre.clipboard_clear()
        fenetre.clipboard_append(selected)


def past_text(e):
    global selected
    if e:
        selected = fenetre.clipboard_get()
    else:
      if selected:
         position = textbox.index(INSERT)
         textbox.insert(position, selected)

def bold_it():
    bold_font = font.Font(textbox, textbox.cget("font"))
    bold_font.configure(weight="bold")
    textbox.tag_configure("bold", font=bold_font)
    current_tags = textbox.tag_names("sel.first")

    if "bold" in current_tags:
        textbox.tag_remove("bold", "sel.first", "sel.last")
    else: 
        textbox.tag_add("bold", "sel.first", "sel.last")
    
def italics_it():
    italics_font = font.Font(textbox, textbox.cget("font"))
    italics_font.configure(slant="italic")
    textbox.tag_configure("italic", font=italics_font)
    current_tags = textbox.tag_names("sel.first")

    if "italic" in current_tags:
        textbox.tag_remove("italic", "sel.first", "sel.last")
    else: 
        textbox.tag_add("italic", "sel.first", "sel.last")

def text_color():
    textcolor = colorchooser.askcolor()[1]
    if textcolor:
        color_font = font.Font(textbox, textbox.cget("font"))
        textbox.tag_configure("colored", font=color_font, foreground=textcolor)
        current_tags = textbox.tag_names("sel.first")

        if "colored" in current_tags:
            textbox.tag_remove("colored", "sel.first", "sel.last")
        else: 
            textbox.tag_add("colored", "sel.first", "sel.last")

def background_color():
    textcolor = colorchooser.askcolor()[1]
    if textcolor:
        textbox.config(bg=textcolor)


def all_text_color():
    textcolor = colorchooser.askcolor()[1]
    if textcolor:
        textbox.config(fg=textcolor)

def print_file():
    printer_name = win32print.GetDefaultPrinter()
    status_bar.config(text=printer_name)
    file_to_print = filedialog.askopenfilename(initialdir="C:/", title="Ouvrir un fichier", filetypes=(("Text Files","*.txt"),("HTML Files",".html"),("PYTHON Files","*.py"),("ALL FILE","*.*")))
    if file_to_print:
        win32api.ShellExecute(0,"print", file_to_print, None,".", 0)

def select_all():
    textbox.tag_add('sel', '1.0', 'end')

def clear():
    textbox.delete(1.0,END)

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=new_file)
menu1.add_command(label="Ouvrir", command=open_file)
menu1.add_command(label="Enregistrer", command=save_file)
menu1.add_command(label="Enregistrer sous", command=save_as_file)
menu1.add_separator()
menu1.add_command(label="Imprimer", command=print_file)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper", command= lambda: cut_text(False))
menu2.add_command(label="Copier", command= lambda: copy_text(False))
menu2.add_command(label="Coller", command= lambda: past_text(False))
menu2.add_command(label="Annuler", command=textbox.edit_undo)
menu2.add_command(label="Refaire", command=textbox.edit_redo)
menu2.add_separator()
menu2.add_command(label="Tout sélectionner", command= lambda: select_all(True))
menu2.add_command(label="Nettoyer", command=clear)
menubar.add_cascade(label="Editer", menu=menu2)

menu_color = Menu(menubar, tearoff=0)
menu_color.add_command(label="Couleur", command=text_color)
menu_color.add_command(label="Arrière plan",command=background_color)
menu_color.add_command(label="Couleur de texte", command=all_text_color)
menubar.add_cascade(label="Couleur", menu=menu_color)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="A propos", command=alert)
menubar.add_cascade(label="Aide", menu=menu3)

fenetre.config(menu=menubar)

status_bar = Label(fenetre, text='prêt  ',anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

fenetre.bind('<Control-Key-x>', cut_text)
fenetre.bind('<Control-Key-c>', copy_text)
fenetre.bind('<Control-Key-v>', past_text)
fenetre.bind('<Control-Key-a>', select_all)
fenetre.bind('<Control-Key-A>', select_all)
fenetre.bind('<Control-Key-Delete>', clear)


bold_button = Button(toolbarr_frame, text="Gras", command=bold_it)
bold_button.grid(row=0, column=0, sticky=W, padx=2)

italics_button = Button(toolbarr_frame, text="Italique", command=italics_it)
italics_button.grid(row=0, column=1, padx=2)

color_button = Button(toolbarr_frame, text="Couleur", command=text_color)
color_button.grid(row=0, column=3, padx=2)

fenetre.mainloop()