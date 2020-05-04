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
    '''
    Guarda los cambios efectuados en el archivo
    '''
    global texto
    global filename
    global saved
    if filename is None:
        #En caso de que no tenga asignado un nombre de archivo te pide uno
        guardar_como()
    else:
        file = open(filename, mode= 'w+')
        texto = code.get(1.0, END)
        file.write(texto)
        file.close()
        savebutton.config(state=DISABLED)
        saved = True
        
def guardar_como():
    '''
    Te permite seleccionar un archivo y sobreescribirlo con el codigo actual en el programa
    '''
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
    '''
    compila un archivo con extensión .c
    en caso de haber errores de compilación, pintará en rojo las lineas que detecta como erroneas
    
    si el archivo no esta guardado llama a la función guardar
    '''
    global filename
    global saved
    global compiled
    if not saved:
        guardar()
    code.tag_delete("err")
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
        #Esto es por un error que los \n los escribe como texto tal cual en vez de hacer un salto de linea
        while "\\" in retorno:
            pos=retorno.find('\\')
            consola.config(state=NORMAL)
            consola.insert(tkinter.END, retorno[:pos])
            if retorno[pos+1] is 'n':
                consola.insert(tkinter.END, '\n')
                consola.config(state=DISABLED)
                errorpos=retorno.find(".c:",len(filename)+2)
                error=copy.copy(retorno[errorpos+3:])
                errorpos=error.find(":")
                error=error[:errorpos]
                #pinta las lineas en las que el compilador detecta un error de rojo
                inicio=str(float(error))
                fin=str(float(error)+1)
                
                code.tag_add("err",inicio,fin)
                
                code.tag_config("err",background="red", foreground="white")
            retorno=retorno[pos+2:]
        raise Exception


def ejecutar():
    '''
    utiliza la consola del sistema para ejecutar un archivo .c
    las funciones de entrada (como un scanf) son irrealizables
    
    si el archivo no esta compilado se llamará a la función compilar
    '''
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
    '''
    permite al usuario acceder a las opciones del debug
    
    si el archivo no esta compilado llamará a la función compilar
    '''
    global filename
    global compiled
    global funciones
    global iterexec
    global vardicts
    global nlib
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
            texto = code.get(1.0, END)
            nlib = texto.count("#include")
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
    '''
    esta función se ejecuta cada vez que el usuario pulsa el botón next
    le va pasando por cabecera las lineas del codigo en formato tabla ast
    '''
    global vardicts
    global nlib
    try:
        line = iterexec[-1].popleft()
        
        numline=str(line.coord)
        pos = numline.find(".c:")
        numline=numline[pos+3:]
        print(numline)
        pos = numline.find(":")
        numline=numline[:pos]
        print(numline)
        
        inicio=str(float(numline)+nlib)
        fin=str(float(numline)+1+nlib)
        #pinta de color azul la linea ejecutada
        code.tag_delete("exe")
        code.tag_add("exe",inicio,fin)
        code.tag_config("exe",background="blue", foreground="white")
        
        evalline(line)

    except IndexError:
        try:
            iterexec.pop()
        except IndexError:
            code.tag_delete("exe")
            nextbutton.config(state=DISABLED)
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
    finally:
        #Imprimimos lsa variables
        variables.config(state=NORMAL)
        variables.delete(1.0,END)
        for i in vardicts:
            variables.insert(tkinter.END, str(i[0]))
            variables.insert(tkinter.END, '\n')
            for j, k in i[1].items():
                if isinstance(k[1],dict):
                    var = str(j) + ": "+ str(k[0])+"\n"
                    for m, n in k[1].items():
                        var+=str(m) + ": "+ str(n)+"\n"
                else:
                    var = str(j) + ": "+ str(k)
                variables.insert(tkinter.END, var)
                variables.insert(tkinter.END, '\n')
        variables.config(state=DISABLED)
            
        

def evalline(line):
    '''
    Analiza la linea que se le pasa por cabecera
    '''
    global vardicts
    #Declaracion de variables/constantes
    if isinstance(line, pycparser.c_ast.Decl):
        vardicts[-1][1][line.name]=[None,None]
        for i in line:
            #Asignacion de tipo
            if isinstance(i, pycparser.c_ast.TypeDecl):
                vardicts[-1][1][line.name][0]=dict(i.children())["type"].names[0]
            #Declaracion de arrays
            elif isinstance(i, pycparser.c_ast.ArrayDecl):
                vardicts[-1][1][line.name][1]=dict()
                hijos=dict(i.children())
                if "dim" in hijos:
                    vardicts[-1][1][line.name][0]=str(hijos["type"].type.names[0])+"["+str(hijos["dim"].value)+"]"
                    for j in range(int(hijos["dim"].value)):
                        posicion=line.name+"["+str(j)+"]"
                        vardicts[-1][1][line.name][1][posicion]=None
                else:
                    vardicts[-1][1][line.name][0]=str(hijos["type"].type.names[0])
            
            #Valor inicial en arrays
            elif isinstance(i, pycparser.c_ast.InitList):
                hijos=i.children()
                for j in range(len(hijos)):
                    posicion=line.name+"["+str(j)+"]"
                    vardicts[-1][1][line.name][1][posicion]=getvalue(hijos[j][1])
            #Valor inicial
            else:
                vardicts[-1][1][line.name][1] = getvalue(i)

    #Asignacion de valores
    elif isinstance(line, pycparser.c_ast.Assignment):
        partes = iter(line)
        left = next(partes)
        right = next(partes)
        if isinstance(left, pycparser.c_ast.ArrayRef):
            array=left.name.name
            pos=array+"["+str(getvalue(left.subscript))+"]"
            setvalue(vardicts[-1][1][array][1][pos],line.op,getvalue(right))
        else:
            setvalue(vardicts[-1][1][left.name][1],line.op,getvalue(right))

    #Incrementar/decrementar
    elif isinstance(line, pycparser.c_ast.UnaryOp):
        unary(line)

    #If
    elif isinstance(line, pycparser.c_ast.If):
        ifbody=dict(line.children())
        #If true
        if getvalue(ifbody['cond']):
            anadido=deque(ifbody['iftrue'])
            iterexec[-1].extend(anadido)
            iterexec[-1].rotate(len(anadido))
        #Else
        elif 'iffalse' in ifbody:
            anadido=deque(ifbody['iffalse'])
            iterexec[-1].extend(anadido)
            iterexec[-1].rotate(len(anadido))
            
    #While
    elif isinstance(line, pycparser.c_ast.While):
        whilebody=dict(line.children())
        #while true
        if getvalue(whilebody['cond']):
            anadido=deque(whilebody['stmt'])
            iterexec[-1].appendleft(line)
            iterexec[-1].extend(anadido)
            iterexec[-1].rotate(len(anadido))

    #For
    elif isinstance(line, pycparser.c_ast.For):
        forbody=dict(line.children())
        #for([],,)
        if 'init' in forbody:
            init = forbody['init']
            if isinstance(init, pycparser.c_ast.DeclList):
                for i in init:
                    evalline(i)
            else:
                evalline(forbody['init'])
            line.init = None
        #for(,,[])
        else:
            evalline(forbody['next'])
        #for(,[],)
        if getvalue(forbody['cond']):
            anadido=deque(forbody['stmt'])
            iterexec[-1].appendleft(line)
            iterexec[-1].extend(anadido)
            iterexec[-1].rotate(len(anadido))

def ArrayDecl(line,og):
    vardicts[-1][1][line.name][1]=dict()
    hijos=dict(i.children())
    if "dim" in hijos:
        vardicts[-1][1][line.name][0]=str(hijos["type"].type.names[0])+"["+str(hijos["dim"].value)+"]"
        for j in range(int(hijos["dim"].value)):
            posicion=line.name+"["+str(j)+"]"
            vardicts[-1][1][line.name][1][posicion]=None
    else:
        vardicts[-1][1][line.name][0]=str(hijos["type"].type.names[0])
    

def setvalue(left,op,right):
    '''
    Asigna un valor a una variable
    
    a     =   18
    ^     ^   ^
    left  op  right
    '''
    if '+' in op:
        left += getvalue(right)
    elif '-' in op:
        left -= getvalue(right)
    elif '*' in op:
        left *= getvalue(right)
    elif '/' in op:
        left /= getvalue(right)
    else:
        left = getvalue(right)
    
    
def getvalue(line):
    '''
    obtiene el valor de una operación, variable, constante... 
    para poder asiganrselo a una variable, efectuar una comparación, etc
    
    se le pasara por cabezera un objeto ast que puede ser multiples cosas: operaciones, constantes...
    '''
    global vardicts
    if isinstance(line, pycparser.c_ast.Constant):
        if "int" in line.type:
            return int(line.value)
        elif "double" in line.type:
            return float(line.value)
        return line.value
    elif isinstance(line, pycparser.c_ast.UnaryOp):
        return unary(line)
    elif isinstance(line, pycparser.c_ast.BinaryOp):
        return binary(line)
    elif isinstance(line, pycparser.c_ast.ID):
        return copy.copy(vardicts[-1][1][line.name][1])
    
    
def unary(line):
    '''
    reliza operaciones con un solo operando como puede ser a++ o -b
    '''
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
    '''
    Obtine el valor de una operación aritmetologica como puede ser a&&b o 7+3
    
    en el caso de ser una operación con mas de un opernado se utilizará recursividad
    ej: 3 + 5 + 7 => binary(binary(3,+,5),+,7)
    '''
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
    '''
    Sale del modo debug
    '''
    newbutton.config(state=NORMAL)
    openbutton.config(state=NORMAL)
    exebutton.config(state=NORMAL)
    nextbutton.config(state=DISABLED)
    code.config(state=NORMAL)
    code.tag_delete("exe")
    debugbutton.config(text="Acceder al modo debug", command=debugon)

def editado(texto):
    '''
    Se ejecuta esta funcion cada vez que el usuario modifica el codigo
    '''
    global saved
    global compiled
    savebutton.config(state=NORMAL)
    compilebutton.config(state=NORMAL)
    saved = False
    compiled = False
    

def get_file():   
    global filename
#    Tk().withdraw()
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
#    code.tag_add("exe","1.0","1.0")

    variables = scrolledtext.ScrolledText(textframe, height=40, width=75)
    variables.pack(side = RIGHT)
    variables.config(state=DISABLED)
    
    consola = scrolledtext.ScrolledText(consoleframe, height=20, width=270)
    consola.pack(side = BOTTOM)
    consola.config(state=DISABLED)
    
    code.bind('<KeyRelease>', editado)

    root.mainloop()