#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Practica 1 de FSO-2020/21
# Autors: M.Àngels Moncusí
# Data: 26 feb 2021
# Versio: v1

# imports tipics/generics
import os   # os.path, os.stat, os.remove ...
import subprocess
from sys import stderr
from stat import filemode


# imports pel GUI
from tkinter import *   # GUI
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox	# per a mostrar missatges a l’usuari
# https://docs.python.org/3.9/library/tkinter.messagebox.html

# imports auxilliars/secundaris
import gzip                 # per si el tar esta comprimit 
import spwd                 # para /etc/shadow
import pwd                  # para /etc/passwd
import grp
from datetime import datetime # para las fechas
from datetime import date
from datetime import timedelta
import stat                 # para permisos
import tarfile              # para archivos .tar

def tracta_exepcio(error):
    exception_type = type(error).__name__
    print("\n",exception_type, file=sys.stderr)
    print(error, file=sys.stderr)
    
def llista_dir():
    global lboxP, lboxS
    global quefaig
    quefaig.set("llistant el directori en curs                   ")
    llista_dirPy()
    llista_dirSh()
    quefaig.set("llistant el directori en curs                   ")

def llista_dirPy():
    global lboxP
    global quefaig
    quefaig.set("llistant el directori en curs en python ")
    elements=os.listdir('./')
    lboxP.delete(0,END)
    for element in elements:
        lboxP.insert(END,element)

def llista_dirSh():
    global lboxS
    global quefaig
    quefaig.set("llistant el directori en curs en shell   ")
    lboxS.delete(0,END)
    out=subprocess.check_output(["ls","./"], universal_newlines=True)
    for elem in out.splitlines():
       lboxS.insert(END,elem)

def noms_curts():
    global lboxP, lboxS
    global quefaig
    quefaig.set("Buscant els noms d'usuaris amb menys d'un cert numero de caràcters ")
    noms_curtsPy()
    noms_curtsSh()

def noms_curtsPy():
    global lboxP
    global quefaig
    mida=simpledialog.askinteger('Mida mínima', 'Quina mida mínima de caracters dels noms vols?')
    quefaig.set("Buscant els noms d'usuaris amb menys de "+str(mida)+" caracters (Python) ")
    lboxP.delete(0,END)
    noms=spwd.getspall()
    for nom in noms:
        if nom.sp_pwdp not in ("*", "!"):
            if(len(nom.sp_nam) < mida):
                lboxP.insert(END, nom.sp_nam)
    
def noms_curtsSh():
    global lboxS
    global quefaig
    mida=simpledialog.askinteger('Mida mínima', 'Quina mida mínima de caracters dels noms vols?')
    quefaig.set("Buscant els noms d'usuaris amb menys de "+str(mida)+" caracters (Python) ")
    lboxS.delete(0,END)
    out=subprocess.check_output(["cut", "-d:", "-f1,2","/etc/shadow"], universal_newlines=True)
    for usu in out.split():
        if(usu.split(':')[1] not in ("*","!") ):
            if(len(usu.split(':')[0]) < mida):
                lboxS.insert(END, usu.split(':')[0])

def sudoers():
    global lboxP, lboxS
    global quefaig
    quefaig.set("Buscant els sudoers")
    sudoersPy()
    sudoersSh()
    quefaig.set("Buscant els sudoers")

def sudoersPy():
    global lboxP
    global quefaig
    quefaig.set("Buscant els sudoers (Python) ")
    lboxP.delete(0,END)
    usuaris=grp.getgrgid(27)
    for user in usuaris.gr_mem:
        lboxP.insert(END, user)


def sudoersSh():
    global lboxS
    global quefaig
    quefaig.set("Buscant els sudoers (Shell) ")
    lboxS.delete(0,END)
    usuaris=spwd.getspall()
    for usu in usuaris:
        sudoer=0
        out=subprocess.check_output(["groups",usu.sp_nam], universal_newlines=True)
        for group in out.split():
            if(group in ("sudo")):
                sudoer=1
        if (sudoer == 1):
            lboxS.insert(END, usu.sp_nam)

def exec_others():
    global lboxP
    global lboxS
    global quefaig
    quefaig.set("Arxius amb permisos d'execució de others ")
    exec_othersPy()
    exec_othersSh()
    quefaig.set("Arxius amb permisos d'execució de others ")

def exec_othersPy():
    global lboxP
    global quefaig
    quefaig.set("Arxius amb permisos d'execució de others (Python)")
    lboxP.delete(0,END)
    directori= os.listdir('./test')
    for f in directori:
        path = os.path.join("./test", f)
        estat = os.stat(path)
        permis = estat.st_mode & stat.S_IXOTH
        if(permis == 1):
            lboxP.insert(END, f)

      
def exec_othersSh():
    global lboxP
    global quefaig
    quefaig.set("Arxius amb permisos d'execució de others (Shell)")
    lboxS.delete(0,END)
    out=subprocess.check_output(["find","./test","-type","f","-perm", "/o=x"], universal_newlines=True)
    for f in out.split():
        lboxS.insert(END, f)



def massa_temps():
    global lboxP, lboxS
    global quefaig
    quefaig.set("llistant els usuaris que fan massa temps no canvien la contrasenya                   ")
    massa_tempspy()
    massa_tempssh()
    quefaig.set("llistant els usuaris que fan massa temps no canvien la contrasenya                   ")

def massa_tempspy():
    global lboxP
    global quefaig
    quefaig.set("llistant els usuaris que fan massa temps no canvien la contrasenya en python")
    mida=simpledialog.askinteger('Num dies','Quants dies vols?')
    entry = spwd.getspall()
    #calculo de fechas
    a = date.today() - timedelta(days=mida)
    b = date(1970,1,1)
    numDias = (a-b).days

    lboxP.delete(0,END)
    for element in entry:
        ultimoCambio = element.sp_lstchg
        if(ultimoCambio < numDias):
            lboxP.insert(END,element.sp_nam)



def massa_tempssh():
    global lboxS
    global quefaig
    quefaig.set("llistant els usuaris que fan massa temps no canvien la contrasenya en shell")
    mida=simpledialog.askinteger('Num dies','Quants dies vols?')
    entry = spwd.getspall()
    #calculo de fechas
    a = date.today() - timedelta(days=mida)
    b = date(1970,1,1)
    numDias = (a-b).days

def setuid_actiu():
    global lboxP, lboxS
    global quefaig
    quefaig.set("llistant els usuaris que tenen el SETUID actiu                   ")
    setuid_actiupy()
    setuid_actiush()
    quefaig.set("llistant els usuaris que tenen el SETUID actiu                   ")


def setuid_actiupy():
    global lboxP
    global quefaig
    quefaig.set("llistant els usuaris que tenen el SETUID actiu amb python")
    lboxP.delete(0,END)
    directorio = os.listdir('./test')
    for line in directorio:
        archivo, extension = os.path.splitext(line)
        #print("El archivo {} tiene extension {}".format(archivo,extension))
        if(extension != ".tar") and (extension != ".tgz"):
            myFile = os.path.join('./test',line)
            test = os.stat(myFile)
            result = test.st_mode & stat.S_ISUID
            if(result != 0):
                lboxP.insert(END,line)


def setuid_actiush():
    global lboxS
    global quefaig
    quefaig.set("llistant els usuaris que tenen el SETUID actiu amb shell")

def permis_exec_tar():
    global lboxP, lboxS
    global quefaig
    quefaig.set("llistant els fitxers tar que tenen permisos d'execucio                   ")
    permis_exec_tarpy()
    permis_exec_tarsh()
    quefaig.set("llistant els fitxers tar que tenen permisos d'execucio                   ")


def permis_exec_tarpy():
    global lboxP
    global quefaig
    quefaig.set("llistant els fitxers tar que tenen permisos d'execucio amb python")
    #crear directorio para descomprimir
    os.mkdir('./descomprimir')
    directorio = os.listdir('./test')
    for line in directorio:
        archivo, extension = os.path.splitext(line)
        #print("El archivo {} tiene extension {}".format(archivo,extension))
        if(extension == ".tar") or (extension == ".tgz"):
            with tarfile.open(line) as t:
                myFile = os.path.join('./test',line)
                t.extract(myFile,'./descomprimir')
    print(os.listdir('./descomprimir'))




def permis_exec_tarsh():
    global lboxs
    global quefaig
    quefaig.set("llistant els fitxers tar que tenen permisos d'execucio amb shell")

def netejar():
    global lboxP, lboxS
    global quefaig
    quefaig.set("netejant la informació trobada")
    lboxP.delete(0,END)
    lboxS.delete(0,END)

def tancaGUI():
    guiroot.quit()

def acabar():
    tancaGUI()

#### tkinter GUI
# No cal mes informacio, pero si teniu curiositat,
# sense entar en molts detalls tcl/tk:
# https://likegeeks.com/es/ejemplos-de-la-gui-de-python/

#### inici del programa a executar en l'entorn python 3

guiroot= Tk()
guiroot.title("Comprovar seguretat bàsica del sistema")
guiroot.minsize(500,400)
### cerca= StringVar()  # variable usada en els QUERIES

quefaig = StringVar()
quefaig.set("No se que fer encara, escull una opció")

# layout del GUI
frameBotons= Frame(guiroot)
Button (frameBotons, text='llista_dir', command=llista_dir).pack(anchor=W,side=LEFT)
Button (frameBotons, text='noms curts', command=noms_curts).pack(anchor=W,side=LEFT)
Button (frameBotons, text='sudoers', command=sudoers).pack(side=LEFT)
Button (frameBotons, text='massa temps', command=massa_temps).pack(side=LEFT)
Button (frameBotons, text='exec others', command=exec_others).pack(side=LEFT)
Button (frameBotons, text='setuid actiu', command=setuid_actiu).pack(side=LEFT)
Button (frameBotons, text='permis exec a tar', command=permis_exec_tar).pack(anchor=E,side=LEFT)
Button (frameBotons, text='netejar', command=netejar).pack(anchor=W,side=LEFT)
frameBotons.pack(expand=True,fill=BOTH,padx=10,pady=5)

frameque= Frame(guiroot)
Label (frameque,text='Què faig:',font=("Arial Bold",14)).pack(anchor=W,side=LEFT)
Label (frameque,textvariable=quefaig, font=("Arial",14)).pack(anchor=W, side=LEFT)
frameque.pack(side=TOP,fill=BOTH,padx=10,pady=10)

frameEvents= Frame(guiroot)
frameEvents.pack(side=TOP, expand=True, fill=BOTH,padx=20,pady=5)

frameEventsPy= Frame(frameEvents)
frameBotonsPy= Frame(frameEvents)
frameEventsPy.pack(side=LEFT,expand=True,fill=BOTH)
frameBotonsPy.pack(side=LEFT,expand=True,fill=BOTH,padx=5)

Label (frameEventsPy,text='Informació trobada Python:',font=("Arial Bold",14)).pack(anchor=W,side=TOP)
scrollist = Scrollbar(frameEventsPy,orient=VERTICAL)
lboxP = Listbox(frameEventsPy,yscrollcommand=scrollist.set,selectmode=SINGLE,exportselection=False)
scrollist.config(command=lboxP.yview)
scrollist.pack(side=RIGHT,fill=Y)
lboxP.pack(side=LEFT,expand=True,fill=BOTH)

Label  (frameBotonsPy, text='Només Python:',font=("Arial Bold",14)).pack(anchor=W,side=TOP,pady=20)
Button (frameBotonsPy, text='llista dir', command=llista_dirPy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='noms curts', command=noms_curtsPy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='sudoers', command=sudoersPy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='massa temps', command=massa_tempspy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='exec others', command=exec_othersPy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='setuid actiu', command=setuid_actiupy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='exec a tar', command=permis_exec_tarpy).pack(anchor=W,side=TOP)
Button (frameBotonsPy, text='netejar', command=netejar).pack(anchor=W,side=TOP)

frameEventsSh= Frame(frameEvents)
frameBotonsSh= Frame(frameEvents)
frameEventsSh.pack(side=LEFT,expand=True,fill=BOTH)
frameBotonsSh.pack(side=LEFT,expand=True,fill=BOTH,padx=5)

Label (frameEventsSh,text='Informació trobada Shell:',font=("Arial Bold",14)).pack(anchor=W,side=TOP)
scrollist = Scrollbar(frameEventsSh,orient=VERTICAL)
lboxS= Listbox(frameEventsSh,yscrollcommand=scrollist.set,selectmode=SINGLE,exportselection=False)
scrollist.config(command=lboxS.yview)
scrollist.pack(side=RIGHT,fill=Y)
lboxS.pack(side=LEFT,expand=True,fill=BOTH)
frameEventsSh.pack(expand=True,fill=BOTH)

Label  (frameBotonsSh, text='Només Shell :',font=("Arial Bold",14)).pack(anchor=W,side=TOP,pady=20)
Button (frameBotonsSh, text='llista dir', command=llista_dirSh).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='noms curts', command=noms_curtsSh).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='sudoers', command=sudoersSh).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='massa temps', command=massa_tempssh).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='exec others', command=exec_othersSh).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='setuid actiu', command=setuid_actiush).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='exec a tar', command=permis_exec_tarsh).pack(anchor=W,side=TOP)
Button (frameBotonsSh, text='netejar', command=netejar).pack(anchor=W,side=TOP)

frameSortir= Frame(guiroot)
frameSortir.pack(side=TOP, expand=True, fill=BOTH,padx=20,pady=5)

Button (frameSortir, text='Sortir',command=acabar).pack(side=BOTTOM,anchor=W)

comprova= messagebox.askyesno("Benvingut","Vols comprovar alguns aspectes de la seguretat del sistema?")

if comprova:
    guiroot.mainloop()
else:
    acabar()
