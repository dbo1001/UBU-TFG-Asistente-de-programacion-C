# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal
"""

#from os import system
import subprocess
#import difflib
#from subprocess import Popen
from subprocess import check_output
#import gdb
#import shlex
import tkinter
import copy
#import re
#from itertools import tee
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
    code.delete(1.0,tkinter.END)
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
        code.delete(1.0,tkinter.END)
        code.insert(tkinter.END, texto)
        file.close()
        savebutton.config(state=tkinter.DISABLED)
        compiled = False
    except NameError:   
        adv = tkinter.Tk()
        adv.title("Advertencia")
        textframe = tkinter.Frame(adv)
        textframe.pack( side = tkinter.TOP )
        textlabel = tkinter.Label(textframe, text="No has seleccionado ningun archivo")
        textlabel.pack( side = tkinter.LEFT)
        aceptframe = tkinter.Frame(adv)
        aceptframe.pack( side = tkinter.BOTTOM )
        aceptbutton = tkinter.Button(aceptframe, text="Aceptar",command=adv.destroy)
        aceptbutton.pack( side = tkinter.LEFT)
        
        
        
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
        texto = code.get(1.0, tkinter.END)
        file.write(texto)
        file.close()
        savebutton.config(state=tkinter.DISABLED)
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
        texto = code.get(1.0, tkinter.END)
        file.write(texto)
        file.close()
        savebutton.config(state=tkinter.DISABLED)
        saved = True  
    except NameError:
        adv = tkinter.Tk()
        adv.title("Advertencia")
        textframe = tkinter.Frame(adv)
        textframe.pack( side = tkinter.TOP )
        textlabel = tkinter.Label(textframe, text="No has seleccionado ningun archivo")
        textlabel.pack( side = tkinter.LEFT)
        aceptframe = tkinter.Frame(adv)
        aceptframe.pack( side = tkinter.BOTTOM )
        aceptbutton = tkinter.Button(aceptframe, text="Aceptar",command=adv.destroy)
        aceptbutton.pack( side = tkinter.LEFT)

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
        consola.config(state=tkinter.NORMAL)
        consola.insert(tkinter.END, 'Compilado correctamente')
        consola.insert(tkinter.END, '\n')
        consola.config(state=tkinter.DISABLED)
        compilebutton.config(state=tkinter.DISABLED)
        compiled=True
    else:
        #Esto es por un error que los \n los escribe como texto tal cual en vez de hacer un salto de linea
        while "\\" in retorno:
            pos=retorno.find('\\')
            consola.config(state=tkinter.NORMAL)
            consola.insert(tkinter.END, retorno[:pos])
            if retorno[pos+1] is 'n':
                consola.insert(tkinter.END, '\n')
                consola.config(state=tkinter.DISABLED)
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
            consola.config(state=tkinter.NORMAL)
            consola.delete(1.0,tkinter.END)
            consola.insert(tkinter.END, 'Archivo no compilado')
            consola.insert(tkinter.END, '\n')
            consola.insert(tkinter.END, 'Compilando...')
            consola.insert(tkinter.END, '\n')
            consola.config(state=tkinter.DISABLED)
            compilar()
    except Exception:
        print("error")
            
    else:
        command = filename[:-2] + " && echo ok || echo err"
#        p = subprocess.Popen([filename[:-2]], stdin=subprocess.PIPE)

        retorno=str(check_output(command, shell=True))[2:-3]
        while "\\" in retorno:
            pos=retorno.find('\\')
            consola.config(state=tkinter.NORMAL)
            if retorno[:pos] is 'ok':
                consola.insert(tkinter.END, '\n')
                consola.config(state=tkinter.DISABLED)  
                break
            consola.insert(tkinter.END, retorno[:pos])
            if retorno[pos+1] is 'n':
                consola.insert(tkinter.END, '\n')
            retorno=retorno[pos+2:]
            if retorno is 'ok':
                consola.insert(tkinter.END, '\n')
                consola.config(state=tkinter.DISABLED)  
                break
            consola.config(state=tkinter.DISABLED)
	

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
    global estructuras
    global retornos
    try:
        if not compiled:
            consola.config(state=tkinter.NORMAL)
            consola.delete(1.0,tkinter.END)
            consola.insert(tkinter.END, 'Archivo no compilado')
            consola.insert(tkinter.END, '\n')
            consola.insert(tkinter.END, 'Compilando...')
            consola.insert(tkinter.END, '\n')
            consola.config(state=tkinter.DISABLED)
            compilar()
    except Exception:
        print("error")
    else:
        estructuras = dict()
        funciones = dict()
        parser = pycparser.parse_file(filename)
        iterar = iter(parser)
        try:
            while(True):
                siguiente = next(iterar)
                print(siguiente.show())
                
                if isinstance(siguiente, pycparser.c_ast.Decl):
                    if isinstance(next(iter(siguiente)), pycparser.c_ast.Struct):
                        structs(next(iter(siguiente)))
                elif isinstance(siguiente, pycparser.c_ast.FuncDef):
                    nombre = getattr(next(iter(siguiente)),'name')
                    funciones[nombre]=siguiente
        except StopIteration:
            #Reutilizo el mismo boton para entrar y salir del modo debug
            debugbutton.config(text="Salir del modo debug", command=debugoff, image=iconstop, width=30, height=30)
            #Deshabilitamos los botones que no vamos a usar durante el debuggueo
            newbutton.config(state=tkinter.DISABLED)
            openbutton.config(state=tkinter.DISABLED)
            exebutton.config(state=tkinter.DISABLED)
            nextbutton.config(state=tkinter.NORMAL)
            stepbutton.config(state=tkinter.NORMAL)
            code.config(state=tkinter.DISABLED)
            iterexec = list()
            iterexec.append(copy.deepcopy(deque(dict(funciones['main'].children())['body'])))
            vardicts = list()
            vardicts.append(["main",dict()])
            retornos = deque()
                

def nextline():
    '''
    esta función se ejecuta cada vez que el usuario pulsa el botón next
    le va pasando por cabecera las lineas del codigo en formato tabla ast
    '''
    global vardicts
    try:
        line = iterexec[-1].popleft()
        
        numline=str(line.coord)
        pos = numline.find(".c:")
        numline=numline[pos+3:]
        pos = numline.find(":")
        numline=numline[:pos]
        
        inicio=str(float(numline))
        fin=str(float(numline)+1)
        #pinta de color azul la linea ejecutada
        code.tag_delete("exe")
        code.tag_add("exe",inicio,fin)
        code.tag_config("exe",background="blue", foreground="white")
        
        evalline(line)

    except IndexError:
        try:
            iterexec.pop()
            vardicts.pop()
            nextline()
        except IndexError:
            code.tag_delete("exe")
            nextbutton.config(state=tkinter.DISABLED)
            stepbutton.config(state=tkinter.DISABLED)
            adv = tkinter.Toplevel(root)
            adv.title("Advertencia")
            adv.focus_set()
            adv.grab_set()
            adv.transient(master=root)
            textframe = tkinter.Frame(adv)
            textframe.pack( side = tkinter.TOP )
            textlabel = tkinter.Label(textframe, text="Ejecucion finalizada", height=10, width=50)
            textlabel.pack( side = tkinter.LEFT)
            aceptframe = tkinter.Frame(adv)
            aceptframe.pack( side = tkinter.BOTTOM )
            aceptbutton = tkinter.Button(aceptframe, text="Aceptar",command=adv.destroy)
            aceptbutton.pack( side = tkinter.LEFT)
    except FuncCallError:
#        print(line)
        iterexec[-2].appendleft(line)
    except ReturnError:
        while(True):
            try:
                iterexec[-1].pop()
            except IndexError:
                break
    finally:
        #Imprimimos las variables
        variables.config(state=tkinter.NORMAL)
        variables.delete(1.0,tkinter.END)
        for i in vardicts:
            variables.insert(tkinter.END, str(i[0]))
            variables.insert(tkinter.END, '\n')
            for j, k in i[1].items():
                if isinstance(k[1],dict):
                    var = str(j) + ": "+ str(k[0])+"\n"
                    for m, n in k[1].items():
                        var+="->"
                        if 'char' in n[0]:
                            var+=str(m) + ": " + n[0] + ": "
                            for l in range(len(n[1])):
                                if n[1][l] is None:
                                    if l == 0:
                                        var+="#VALUE!"
                                    break
                                else:
                                    var+=n[1][l]
                            var+="\n"
                        else:
                            if n[1] is None:
                                var+=str(m) + ": " + n[0] + ": #VALUE!"
                            else:
                                var+=str(m) + ": "+ n[0] + ": "+ str(n[1])
                            var+="\n"
                else:
                    if k[1] is None:
                        var = str(j) + ": "+ k[0] + ": #VALUE!"
                    else:
                        var = str(j) + ": "+ k[0] + ": " + str(k[1])
                variables.insert(tkinter.END, var)
                variables.insert(tkinter.END, '\n')
            variables.insert(tkinter.END, '\n')
        variables.config(state=tkinter.DISABLED)
            
        

def skip():
    fin = len(iterexec)
    nextline()
    while(len(iterexec) > fin):
        nextline()
    
    
    
def evalline(line):
    '''
    Analiza la linea que se le pasa por cabecera
    '''
    global vardicts
    global estructuras
    global funciones
    global iterexec
    global retornos
    #Declaracion de variables/constantes
    if isinstance(line, pycparser.c_ast.Decl):
        vardicts[-1][1][line.name] = [None,None]
        #Asignacion de tipo
        if isinstance(line.type.type, pycparser.c_ast.Struct):
            vardicts[-1][1][line.name][0] = line.type.type.name+"(Struct)"
            vardicts[-1][1][line.name][1] = copy.deepcopy(estructuras[line.type.type.name])
        else:
            vardicts[-1][1][line.name][0] = line.type.type.names[0]
            
        #Igualar a retorno de funcion
        if isinstance(line.init, pycparser.c_ast.FuncCall):
            if line.init.name.name in funciones:
                line.init = innerfunction(line.init)
                raise FuncCallError
            else:
                line.init = outterfunction(line.init) 
            
        #Declaracion de arrays
        elif isinstance(line.init, pycparser.c_ast.ArrayDecl):
            vardicts[-1][1][line.name][1] = list()
            vardicts[-1][1][line.name][0] = arraydecl(line.init,vardicts[-1][1][line.name][1])
        
        #Valor inicial en arrays
        elif isinstance(line.init, pycparser.c_ast.InitList):
            initlist(line.init,vardicts[-1][1][line.name][1])
            
        #Valor inicial
        else:
            vardicts[-1][1][line.name][1] = getvalue(line.init)

    #Asignacion de valores
    elif isinstance(line, pycparser.c_ast.Assignment):
        if isinstance(line.rvalue, pycparser.c_ast.FuncCall):
            if line.rvalue.name.name in funciones:
                line.rvalue = innerfunction(line.rvalue)
                raise FuncCallError
            else:
                line.rvalue = outterfunction(line.rvalue)
            
        if isinstance(line.lvalue, pycparser.c_ast.ArrayRef):
            setvalue(arrayref(line.lvalue),int(line.lvalue.subscript.value),line.op,line.rvalue)
        elif isinstance(line.lvalue, pycparser.c_ast.StructRef):
            setvalue(vardicts[-1][1][line.lvalue.name.name][1][line.lvalue.field.name],1,line.op,line.rvalue)
        else:
            setvalue(vardicts[-1][1][line.lvalue.name],1,line.op,line.rvalue)

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
    
    #Llamadas a funciones
    elif isinstance(line, pycparser.c_ast.FuncCall):
        if line.name.name in funciones:
            innerfunction(line)
        else:
            outterfunction(line)
        
        
    #Return
    elif isinstance(line, pycparser.c_ast.Return):
        valor = getvalue(line.expr)
        retornos.pop().value=valor
        raise ReturnError
                


def innerfunction(line):
    '''
    Llamadas a funciones
    '''
    cabecera = dict()
    for i in range(len(funciones[line.name.name].decl.type.args.params)):
        if isinstance(line.args.exprs[i], pycparser.c_ast.FuncCall):
            if line.args.exprs[i].name.name in funciones:
                line.args.exprs[i] = innerfunction(line.args.exprs[i])
                raise FuncCallError
            else:
                line.args.exprs[i] = outterfunction(line.args.exprs[i])
        cabecera[funciones[line.name.name].decl.type.args.params[i].name] = [funciones[line.name.name].decl.type.args.params[i].type.type.names[0],getvalue(line.args.exprs[i])]
    iterexec.append(copy.deepcopy(deque(funciones[line.name.name].body)))
    vardicts.append([line.name.name,cabecera])
    funcion=copy.deepcopy(line)
    line=pycparser.c_ast.Constant(None,None)
    line.type=funciones[funcion.name.name].decl.type.type.type.names[0]
    if line.type != "void":
        retornos.append(line)
    return line
    



def outterfunction(line):
        
    if "printf" == line.name.name:
        consola.config(state=tkinter.NORMAL)
        i=1
        imprimir = line.args.exprs[0].value[1:-1]
        while '%' in imprimir:
            position = imprimir.find('%')
            imprimir = imprimir[:position] + str(getvalue(line.args.exprs[i])) + imprimir[position+2:]
            i+=1
        while '\\n' in imprimir:
            position = imprimir.find('\\n')
            consola.insert(tkinter.END, imprimir[:position])
            consola.insert(tkinter.END, '\n')
            imprimir = imprimir[position+2:]
        consola.insert(tkinter.END, imprimir)
        consola.config(state=tkinter.DISABLED)
    elif "scanf" == line.name.name:
        scanf(line)
    elif "strcpy" == line.name.name:
        rstring = line.args.exprs[1].value
        lstring = vardicts[-1][1][line.args.exprs[0].name.name][1][line.args.exprs[0].field.name][1]
        for i in range(len(rstring[1:-1])):
            lstring[i]=rstring[i+1]



def scanf(line):
    '''
    Lanza una ventana emergente para introducir el valor solicitado por el scanf
    '''
    def escanear():
        value.value=valueentry.get()
        scan.destroy()
        asignacion = pycparser.c_ast.Assignment("=",line.args.exprs[1],value)
        try:
            evalline(asignacion)
        except ValueError:
            debugoff()
            error = tkinter.Toplevel(root)
            error.title("Advertencia")
            error.focus_set()
            error.grab_set()
            error.transient(master=root)
            textframe = tkinter.Frame(error)
            textframe.pack( side = tkinter.TOP )
            textlabel = tkinter.Label(textframe, text="Valor introducido no valido", height=10, width=50)
            textlabel.pack( side = tkinter.LEFT)
            aceptframe = tkinter.Frame(error)
            aceptframe.pack( side = tkinter.BOTTOM )
            aceptbutton = tkinter.Button(aceptframe, text="Aceptar",command=error.destroy)
            aceptbutton.pack( side = tkinter.LEFT)
        else:
            nextbutton.config(state=tkinter.NORMAL)
    value = pycparser.c_ast.Constant(None,None)
    #conversion de tipos
    if "d" in line.args.exprs[0].value:
        value.type='int'
    elif "f" in line.args.exprs[0].value:
        value.type='double'
    elif "c" in line.args.exprs[0].value:
        value.type='char'
    elif "s" in line.args.exprs[0].value:
        value.type='string'
    #Ventana emergente que solicita la introduccion de una variable para el scan
    nextbutton.config(state=tkinter.DISABLED)
    stepbutton.config(state=tkinter.DISABLED)
    scan = tkinter.Toplevel(root)
    scan.focus_set()
    scan.grab_set()
    scan.transient(master=root)
    scan.title("Escanear valor")
    textframe = tkinter.Frame(scan)
    textframe.pack(side = tkinter.TOP)
    textlabel = tkinter.Label(textframe, text="Introduce el valor adecuado", height=4, width=50)
    textlabel.pack(side = tkinter.LEFT)
    valueframe = tkinter.Frame(scan)
    valueframe.pack(side = tkinter.TOP)
    valueentry = tkinter.Entry(valueframe)
    valueentry.pack(side = tkinter.LEFT)
    buttonframe = tkinter.Frame(scan)
    buttonframe.pack(side = tkinter.BOTTOM)
    aceptbutton = tkinter.Button(buttonframe, text="Aceptar", command=escanear)
    aceptbutton.pack()
    
    
    
    
def structs(line):
    '''
    Declaracion de structuras
    
    se utilizara una lista de diccionarios en el que la clave sera el nombre de los campos
    '''
    global estructuras
    newst = dict()
    for i in line:
        newst[i.name] = [None,None]
        for j in i:
            #Asignacion de tipo
            if isinstance(j, pycparser.c_ast.TypeDecl):
                newst[i.name][0] = j.type.names[0]
            #Declaracion de arrays
            elif isinstance(j, pycparser.c_ast.ArrayDecl):
                newst[i.name][1] = list()
                newst[i.name][0] = arraydecl(j,newst[i.name][1])
    estructuras[line.name]=newst
    



def arraydecl(line,og):
    '''
    Declaracion de arrays, necesario para hacerlos multidimensionales
    
    TODO: inicializar los arrays => int x[]={1,2}
    '''
    global vardicts
    for i in range(int(line.dim.value)):
        if isinstance(line.type, pycparser.c_ast.ArrayDecl):
            og.append([])
            retorno = arraydecl(line.type,og[i])
        else:
            og.append(None)
            retorno = line.type.type.names[0]
    retorno += "["+ line.dim.value +"]"
    return retorno



def initlist(line,og):
    '''
    Inicializa los valores de un array
    
    TODO: inicializar los arrays => int x[]={1,2}
    '''
    global vardicts
    n=0
    for i in line:
        if isinstance(i, pycparser.c_ast.InitList):
            initlist(i,og[n])
        else:
            og[n]=getvalue(i)
        n+=1


def arrayref(line):
    '''
    tomar la referencia de un array
    '''
    global vardicts
    if isinstance(line.name, pycparser.c_ast.ArrayRef):
        return arrayref(line.name)[int(line.name.subscript.value)]
    if isinstance(line.name, pycparser.c_ast.StructRef):
        return vardicts[-1][1][line.name.name.name][1][line.name.field.name][1]
    return vardicts[-1][1][line.name.name][1]



def setvalue(left,index,op,right):
    '''
    Asigna un valor a una variable
    
    a     =   18
    ^     ^   ^
    left  op  right
    
    la variable index pasada por cabecera se utiliza porque las variables de tipos primitivos son inmutables y si paso una lista me permite modificar su valor
    '''
    if '+' in op:
        left[index] += getvalue(right)
    elif '-' in op:
        left[index] -= getvalue(right)
    elif '*' in op:
        left[index] *= getvalue(right)
    elif '/' in op:
        left[index] /= getvalue(right)
    else:
        left[index] = getvalue(right)


    
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
    elif isinstance(line, pycparser.c_ast.ArrayRef):
        return copy.copy(arrayref(line)[int(line.subscript.value)])
    elif isinstance(line, pycparser.c_ast.StructRef):
        return copy.copy(vardicts[-1][1][line.name.name][1][line.field.name][1])



def unary(line):
    '''
    reliza operaciones con un solo operando como puede ser a++ o -b
    '''
    global vardicts
    if isinstance(line.expr, pycparser.c_ast.FuncCall):
        if line.expr.name.name in funciones:
            line.expr = innerfunction(line.expr)
            raise FuncCallError
        else:
            line.expr = outterfunction(line.expr)
        
    elif isinstance(line.expr, pycparser.c_ast.ID):
        variable = line.expr.name
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

    return getvalue(line.expr)*-1
        
def binary(line):
    '''
    Obtine el valor de una operación aritmetologica como puede ser a&&b o 7+3
    
    en el caso de ser una operación con mas de un opernado se utilizará recursividad
    ej: 3 + 5 + 7 => binary(binary(3,+,5),+,7)
    '''
    global vardicts
    global retornos
    operandos = list()
    
    #Obtencion de los operandos
    
    if isinstance(line.left, pycparser.c_ast.FuncCall):
        if line.left.name.name in funciones:
            line.left = innerfunction(line.left)
            raise FuncCallError
        else:
            line.left = outterfunction(line.left)
            
    if isinstance(line.right, pycparser.c_ast.FuncCall):
        if line.right.name.name in funciones:
            line.right = innerfunction(line.right)
            raise FuncCallError
        else:
            line.right = outterfunction(line.right)
            
    operandos.append(getvalue(line.left))
    operandos.append(getvalue(line.right))
    
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
    
                            

class FuncCallError(Exception):
    pass


class ReturnError(Exception):
    pass



def debugoff():
    '''
    Sale del modo debug
    '''
    newbutton.config(state=tkinter.NORMAL)
    openbutton.config(state=tkinter.NORMAL)
    exebutton.config(state=tkinter.NORMAL)
    nextbutton.config(state=tkinter.DISABLED)
    stepbutton.config(state=tkinter.DISABLED)
    code.config(state=tkinter.NORMAL)
    code.tag_delete("exe")
    variables.config(state=tkinter.NORMAL)
    variables.delete(1.0,tkinter.END)
    variables.config(state=tkinter.DISABLED)
    debugbutton.config(text="Acceder al modo debug", command=debugon, image=iconstart, width=30, height=30)

def editado(texto):
    '''
    Se ejecuta esta funcion cada vez que el usuario modifica el codigo
    '''
    global saved
    global compiled
    code.tag_delete("err")
    savebutton.config(state=tkinter.NORMAL)
    compilebutton.config(state=tkinter.NORMAL)
    saved = False
    compiled = False
    

def get_file():
    '''
    Abre una ventana emergente para abrir un archivo
    '''
    global filename
#    Tk().withdraw()
    filename = filedialog.askopenfilename()
    if filename is None or len(filename) < 3 or filename[-2] is not "." or filename[-1] is not "c":
        raise NameError
    

    
if __name__ == "__main__":
    root = tkinter.Tk()
    
    iconnew=tkinter.PhotoImage(file="icons/new.png").subsample(18,18)
    iconopen=tkinter.PhotoImage(file="icons/open.png").subsample(18,18)
    iconsave=tkinter.PhotoImage(file="icons/save.png").subsample(18,18)
    iconstart=tkinter.PhotoImage(file="icons/start.png").subsample(18,18)
    iconstop=tkinter.PhotoImage(file="icons/stop.png").subsample(18,18)
    iconcompile=tkinter.PhotoImage(file="icons/compile.png").subsample(18,18)
    iconexe=tkinter.PhotoImage(file="icons/execute.png").subsample(18,18)
    iconstep=tkinter.PhotoImage(file="icons/step.png").subsample(18,18)
    iconnext=tkinter.PhotoImage(file="icons/next.png").subsample(18,18)


    root.title("TFG")
    root.state('zoomed')
    frame = tkinter.Frame(root)
    frame.pack()
    
    textframe = tkinter.Frame(root)
    textframe.pack()
    
    consoleframe = tkinter.Frame(root)
    consoleframe.pack()
    
    newbutton = tkinter.Button(frame, text="Nuevo...", command=nuevo, image=iconnew, width=30, height=30)
    newbutton.pack( side = tkinter.LEFT)
    
    openbutton = tkinter.Button(frame, text="Abrir", command=abrir, image=iconopen, width=30, height=30)
    openbutton.pack( side = tkinter.LEFT )
    
    savebutton = tkinter.Button(frame, text="Guardar", command=guardar, image=iconsave, width=30, height=30, state=tkinter.DISABLED)
    savebutton.pack( side = tkinter.LEFT )
       
    compilebutton = tkinter.Button(frame, text="Compilar",command=compilar, image=iconcompile, width=30, height=30, state=tkinter.DISABLED)
    compilebutton.pack( side = tkinter.LEFT )
    
    exebutton = tkinter.Button(frame, text="Ejecutar",command=ejecutar, image=iconexe, width=30, height=30)
    exebutton.pack( side = tkinter.LEFT )
    
    debugbutton = tkinter.Button(frame, text="Acceder al modo debug",command=debugon, image=iconstart, width=30, height=30)
    debugbutton.pack( side = tkinter.LEFT )
    
    nextbutton = tkinter.Button(frame, text="Next",command=nextline, image=iconnext, width=30, height=30, state=tkinter.DISABLED )
    nextbutton.pack( side = tkinter.LEFT )
    
    stepbutton = tkinter.Button(frame, text="Skip",command=skip, image=iconstep, width=30, height=30, state=tkinter.DISABLED )
    stepbutton.pack( side = tkinter.LEFT )
    
    code = scrolledtext.ScrolledText(textframe, height=40, width=200)
    code.pack(side = tkinter.LEFT)
#    code.tag_add("exe","1.0","1.0")

    variables = scrolledtext.ScrolledText(textframe, height=40, width=75)
    variables.pack(side = tkinter.RIGHT)
    variables.config(state=tkinter.DISABLED)
    
    consola = scrolledtext.ScrolledText(consoleframe, height=20, width=270)
    consola.pack(side = tkinter.BOTTOM)
    consola.config(state=tkinter.DISABLED)
    
    code.bind('<KeyRelease>', editado)

    root.mainloop()