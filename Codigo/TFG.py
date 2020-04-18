# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

from os import system
import subprocess
from subprocess import Popen
from subprocess import check_output
#import gdb
import shlex
import tkinter
import copy
import re
from itertools import tee
from collections import deque
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import pycparser

texto = None
filename = None
saved = True
compiled = True


def nuevo():
    global texto
    texto=None
    global filename
    filename=None
    code.delete(1.0,END)
    global saved
    saved = True
    global compiled
    compiled = True
    

def abrir(): 
    global texto
    global filename
    global saved
    global compiled
    try:
        get_file()
        file = open(filename, mode= 'r')
        texto = file.read()
        code.delete(1.0,END)
        code.insert(tkinter.END, texto)
        file.close()
        savebutton.config(state=DISABLED)
        compiled = False
    except NameError:   
        adv = Tk()
        adv.title("Advertencia")
        textframe = Frame(adv)
        textframe.pack( side = TOP )
        textlabel = Label(textframe, text="No has seleccionado ningun archivo")
        textlabel.pack( side = LEFT)
        aceptframe = Frame(adv)
        aceptframe.pack( side = BOTTOM )
        aceptbutton = Button(aceptframe, text="Aceptar",command=adv.destroy)
        aceptbutton.pack( side = LEFT)
        
        
        
def guardar():
    global texto
    global filename
    global saved
    if filename is None:
        guardar_como()
    else:
        file = open(filename, mode= 'w+')
        texto = code.get(1.0, END)
        file.write(texto)
        file.close()
        savebutton.config(state=DISABLED)
        saved = True
        
def guardar_como(): 
    global texto
    global filename
    global saved
    try:
        get_file()
        file = open(filename, mode= 'w+')
        texto = code.get(1.0, END)
        file.write(texto)
        file.close()
        savebutton.config(state=DISABLED)
        saved = True  
    except NameError:
        adv = Tk()
        adv.title("Advertencia")
        textframe = Frame(adv)
        textframe.pack( side = TOP )
        textlabel = Label(textframe, text="No has seleccionado ningun archivo")
        textlabel.pack( side = LEFT)
        aceptframe = Frame(adv)
        aceptframe.pack( side = BOTTOM )
        aceptbutton = Button(aceptframe, text="Aceptar",command=adv.destroy)
        aceptbutton.pack( side = LEFT)

def compilar():
    global filename
    global saved
    global compiled
    print(saved)
    if not saved:
        guardar()
    command = "gcc " + filename + " -g -o " + filename[:-2] + " && echo ok || echo err"
    retorno=str(check_output(command, stderr=subprocess.STDOUT, shell=True))[2:-1]
    if len(retorno) == 7:
        consola.config(state=NORMAL)
        consola.insert(tkinter.END, 'Compilado correctamente')
        consola.insert(tkinter.END, '\n')
        consola.config(state=DISABLED)
        compilebutton.config(state=DISABLED)
        compiled=True
    else:
        while "\\" in retorno:
            pos=retorno.find('\\')
            consola.config(state=NORMAL)
            consola.insert(tkinter.END, retorno[:pos])
            if retorno[pos+1] is 'n':
                consola.insert(tkinter.END, '\n')
            consola.config(state=DISABLED)
            retorno=retorno[pos+2:]
        raise Exception


def ejecutar():
    global filename
    global compiled
    try:
        if not compiled:
            consola.config(state=NORMAL)
            consola.insert(tkinter.END, 'Archivo no compilado')
            consola.insert(tkinter.END, '\n')
            consola.insert(tkinter.END, 'Compilando...')
            consola.insert(tkinter.END, '\n')
            consola.config(state=DISABLED)
            compilar()
    except Exception:
        print("error")
            
    else:
        command = filename[:-2] + " && echo ok || echo err"
        p = subprocess.Popen([filename[:-2]], stdin=subprocess.PIPE)
#        print(p.communicate().decode)

        retorno=str(check_output(command, shell=True))[2:-3]
        while "\\" in retorno:
            pos=retorno.find('\\')
            consola.config(state=NORMAL)
            if retorno[:pos] is 'ok':
                consola.insert(tkinter.END, '\n')
                consola.config(state=DISABLED)  
                break
            consola.insert(tkinter.END, retorno[:pos])
            if retorno[pos+1] is 'n':
                consola.insert(tkinter.END, '\n')
            retorno=retorno[pos+2:]
            if retorno is 'ok':
                consola.insert(tkinter.END, '\n')
                consola.config(state=DISABLED)  
                break
            consola.config(state=DISABLED)
	

def debugon():
    global filename
    global compiled
    global funciones
    global iterexec
    global vardicts
    try:
        if not compiled:
            consola.config(state=NORMAL)
            consola.insert(tkinter.END, 'Archivo no compilado')
            consola.insert(tkinter.END, '\n')
            consola.insert(tkinter.END, 'Compilando...')
            consola.insert(tkinter.END, '\n')
            consola.config(state=DISABLED)
            compilar()
    except Exception:
        print("error")
    else:
        funciones = dict()
        parser = pycparser.parse_file(filename,use_cpp=False)
        iterar = iter(parser)
        try:
            while(True):
                siguiente = next(iterar)
                print(siguiente.show())
                if isinstance(siguiente, pycparser.c_ast.FuncDef):
                    nombre = getattr(next(iter(siguiente)),'name')
                    funciones[nombre]=siguiente
        except StopIteration:
            debugbutton.config(text="Salir del modo debug", command=debugoff)
            savebutton.config(state=DISABLED)
            compilebutton.config(state=DISABLED)
            newbutton.config(state=DISABLED)
            openbutton.config(state=DISABLED)
            exebutton.config(state=DISABLED)
            nextbutton.config(state=NORMAL)
            code.config(state=DISABLED)
            iterexec = list()
            iterexec.append(deque(dict(funciones['main'].children())['body']))
            vardicts = list()
            vardicts.append(["main",dict()])
                

def nextline():
    try:
        line = iterexec[-1].popleft()
        
        #Declaracion de variables/constantes
        if isinstance(line, pycparser.c_ast.Decl):
            vardicts[-1][1][line.name]=[None,None]
            print(line)
            for i in line:
                #Asignacion de tipo
                if isinstance(i, pycparser.c_ast.TypeDecl):                            
                    vardicts[-1][1][line.name][0]=dict(i.children())["type"].names[0]
                #Valor inicial
                else:
                    vardicts[-1][1][line.name][1] = getvalue(i)
            if vardicts[-1][1][line.name][1] is not None:
                if "int" in vardicts[-1][1][line.name][0]:
                    vardicts[-1][1][line.name][1] = int(vardicts[-1][1][line.name][1])
                elif "float" or "double" in vardicts[-1][1][line.name][0]:
                    vardicts[-1][1][line.name][1] = float(vardicts[-1][1][line.name][1])
                            
        #Asignacion de valores
        elif isinstance(line, pycparser.c_ast.Assignment):
            partes = iter(line)
            left = next(partes).name
            right = next(partes)
            vardicts[-1][1][left][1] = getvalue(right)
            if "int" in vardicts[-1][1][left][0]:
                vardicts[-1][1][left][1] = int(vardicts[-1][1][left][1])
            elif "float" or "double" in vardicts[-1][1][left][0]:
                vardicts[-1][1][left][1] = float(vardicts[-1][1][left][1])
            
        #Incrementar/decrementar
        elif isinstance(line, pycparser.c_ast.UnaryOp):
            unary(line)
            
        #If
        elif isinstance(line, pycparser.c_ast.If):
            ifbody=dict(line.children())
            condicion=getvalue(ifbody['cond'])
            if condicion:
                iterexec.append(deque(ifbody['iftrue']))
            elif 'iffalse' in ifbody:
                iterexec.append(deque(ifbody['iffalse']))
        
        #While
        elif isinstance(line, pycparser.c_ast.While):
            whilebody=dict(line.children())
            condicion=getvalue(whilebody['cond'])
            if condicion:
                iterexec[-1].appendleft(line)
                iterexec.append(deque(whilebody['stmt']))
            
        
        #Imprimimos lsa variables
        variables.config(state=NORMAL)
        variables.delete(1.0,END)
        for i in vardicts:
            variables.insert(tkinter.END, str(i[0]))
            variables.insert(tkinter.END, '\n')
            for j, k in i[1].items():
                var = str(j) + ": "+ str(k)
                variables.insert(tkinter.END, var)
                variables.insert(tkinter.END, '\n')
        variables.config(state=DISABLED)

    except IndexError:
        try:
            iterexec.pop()
        except IndexError:
            adv = Tk()
            adv.title("Advertencia")
            textframe = Frame(adv)
            textframe.pack( side = TOP )
            textlabel = Label(textframe, text="Ejecucion finalizada", height=10, width=50)
            textlabel.pack( side = LEFT)
            aceptframe = Frame(adv)
            aceptframe.pack( side = BOTTOM )
            aceptbutton = Button(aceptframe, text="Aceptar",command=adv.destroy)
            aceptbutton.pack( side = LEFT)
            
        
                
def getvalue(line):
    if isinstance(line, pycparser.c_ast.Constant):
        return line.value
    elif isinstance(line, pycparser.c_ast.UnaryOp):
        return unary(line)
    elif isinstance(line, pycparser.c_ast.BinaryOp):
        return binary(line)
    elif isinstance(line, pycparser.c_ast.ID):
        return copy.copy(vardicts[-1][1][line.name][1])
    
    
def unary(line):
    global vardicts
    son = next(iter(line))
    if isinstance(son, pycparser.c_ast.ID):
        variable = son.name
        retorno = copy.copy(vardicts[-1][1][variable][1])
        #aumentar
        if "++" in line.op:
            vardicts[-1][1][variable][1]+=1
        #decrementar
        elif "--" in line.op:
            vardicts[-1][1][variable][1]-=1
        #negativo
        else:
            return retorno * -1
        #Ejemplo y=x++ o y=x--
        if "p" in line.op:
            return retorno
        #Ejemplo y=--x o y=++x
        else:
            return copy.copy(vardicts[-1][1][variable][1])
            
    elif isinstance(son, pycparser.c_ast.Constant):
        if "int" in son.type:
            return int(son.value)*-1
        elif "double" in son.type:
            return float(son.value)*-1
            
    elif isinstance(son, pycparser.c_ast.BinaryOp):
        return binary(son)*-1
        
    elif isinstance(son, pycparser.c_ast.UnaryOp):
        return unary(son)*-1
        
def binary(line):
    global vardicts
    operandos = list()
    #Obtencion de los operandos
    for son in line:
        if isinstance(son, pycparser.c_ast.ID):
            variable = son.name
            operandos.append(copy.copy(vardicts[-1][1][variable][1]))
                
        elif isinstance(son, pycparser.c_ast.Constant):
            if "int" in son.type:
                operandos.append(int(son.value))
            elif "double" in son.type:
                operandos.append(float(son.value))
                
        elif isinstance(son, pycparser.c_ast.BinaryOp):
            operandos.append(binary(son))
            
        elif isinstance(son, pycparser.c_ast.UnaryOp):
            operandos.append(unary(son))
            
    #Operaciones llevadas a cabo
    
    #suma
    if "+" in line.op:
        return operandos[0]+operandos[1]
    #resta
    elif "-" in line.op:
        return operandos[0]-operandos[1]
    #multiplicacion
    elif "*" in line.op:
        return operandos[0]*operandos[1]
    #division
    elif "/" in line.op:
        if type(operandos[0]) is int and type(operandos[1]) is int:
            return int(operandos[0]/operandos[1])
        return operandos[0]/operandos[1]
    #resto
    elif "%" in line.op:
        return operandos[0]*operandos[1]
    #and
    elif "&&" in line.op:
        return operandos[0] and operandos[1]
    #and binario
    elif "&" in line.op:
        return operandos[0]&operandos[1]
    #or
    elif "||" in line.op:
        return operandos[0] or operandos[1]
    #or binario
    elif "|" in line.op:
        return operandos[0]|operandos[1]
    #xor binario
    elif "^" in line.op:
        return operandos[0]^operandos[1]
    #igualdad
    elif "==" in line.op:
        return int(operandos[0] == operandos[1])
    #distint0
    elif "!=" in line.op:
        return int(operandos[0] != operandos[1])
    #menor o igual
    elif "<=" in line.op:
        return int(operandos[0] <= operandos[1])
    #mayor o igual
    elif ">=" in line.op:
        return int(operandos[0] >= operandos[1])
    #menor que
    elif "<" in line.op:
        return int(operandos[0] < operandos[1])
    #mayor que
    elif ">" in line.op:
        return int(operandos[0] > operandos[1])
    
                            
    
def debugoff():
    newbutton.config(state=NORMAL)
    openbutton.config(state=NORMAL)
    exebutton.config(state=NORMAL)
    nextbutton.config(state=DISABLED)
    code.config(state=NORMAL)
    debugbutton.config(text="Acceder al modo debug", command=debugon)

def editado(texto):
    global saved
    global compiled
    savebutton.config(state=NORMAL)
    compilebutton.config(state=NORMAL)
    saved = False
    compiled = False
    

def get_file():   
    global filename
    Tk().withdraw()
    filename = filedialog.askopenfilename()
    if filename is None or len(filename) < 3 or filename[-2] is not "." or filename[-1] is not "c":
        raise NameError
    

    
if __name__ == "__main__":
    root = Tk()
    root.title("TFG")
    root.state('zoomed')
    frame = Frame(root)
    frame.pack()
    
    textframe = Frame(root)
    textframe.pack()
    
    consoleframe = Frame(root)
    consoleframe.pack()
    
    newbutton = Button(frame, text="Nuevo...",command=nuevo)
    newbutton.pack( side = LEFT)
    
    openbutton = Button(frame, text="Abrir",command=abrir)
    openbutton.pack( side = LEFT )
    
    savebutton = Button(frame, text="Guardar",command=guardar, state=DISABLED)
    savebutton.pack( side = LEFT )
       
    compilebutton = Button(frame, text="Compilar",command=compilar, state=DISABLED)
    compilebutton.pack( side = LEFT )
    
    exebutton = Button(frame, text="Ejecutar",command=ejecutar)
    exebutton.pack( side = LEFT )
    
    debugbutton = Button(frame, text="Acceder al modo debug",command=debugon)
    debugbutton.pack( side = LEFT )
    
    nextbutton = Button(frame, text="Next",command=nextline, state=DISABLED )
    nextbutton.pack( side = LEFT )
    
    code = scrolledtext.ScrolledText(textframe, height=40, width=200)
    code.pack(side = LEFT)

    variables = scrolledtext.ScrolledText(textframe, height=40, width=75)
    variables.pack(side = RIGHT)
    variables.config(state=DISABLED)
    
    consola = scrolledtext.ScrolledText(consoleframe, height=20, width=270)
    consola.pack(side = BOTTOM)
    consola.config(state=DISABLED)
    
    code.bind('<KeyRelease>', editado)

    root.mainloop()