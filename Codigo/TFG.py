"""
+------------------------------------------------------------------------------
|Proyecto: Trabajo de fin de Grado
|Tituación: Ingenieria Informatica
|Universidad: Universidad de Burgos
|Autor: Rubén Marcos González
|Tutor: Carlos Pardo Aguilar
|Proyecto original del parser (pycparser): https://github.com/eliben/pycparser
|Fuente de los iconos: https://www.flaticon.com/packs/essential-set-2
+------------------------------------------------------------------------------
"""
#importamos las bibliotecas que vamos a usar
import math
import subprocess
from subprocess import check_output
import tkinter
from tkinter import scrolledtext
from tkinter import filedialog
import copy
from collections import deque
import tooltip as ttp
import pycparser
#Variables globales que se usarán a lo largo del programa
texto = None
filename = None
saved = True
compiled = True
debugging = False

def nuevo():
    '''
    Para crear un nuevo archivo
    
    Inicializa el cuadro de texto para el texto como
    #include <stdio.h>
    
    int main(){
        
        return 0;
    }
    '''
    #Se pone texto como vacio
    global texto
    texto=None
    #Al no trabajar sobre ningún archivo se borre la variable que almacena el nombre del archivo
    global filename
    filename=None
    #Se borra lo que haya en el cuadro de texto para el código
    code.delete(1.0,tkinter.END)
    #Y se pone un código básico por defecto
    #    #include <stdio.h>
    #    
    #    int main(){
    #        
    #        return 0;
    #    }
    code.insert(tkinter.END, "#include <stdio.h>\n\nint main(){\n\t\n\treturn 0;\n}")
    compilebutton.config(state=tkinter.DISABLED)
    exebutton.config(state=tkinter.DISABLED)
    debugbutton.config(state=tkinter.DISABLED)
    global saved
    saved = True
    global compiled
    compiled = True
    

def abrir():
    '''
    Lanza una ventana emergente para seleccionar el archivo sobre el que trabajar
    '''
    global texto
    global filename
    global saved
    global compiled
    try:
        #Se solicita el nombre de un archivo para abrirlo
        filename = filedialog.askopenfilename(title = "Selecciona un archivo tipo C",filetypes = [("Archivo C","*.c")])
        #en caso de que el archivo no tenga la extension adecuada saltará una excepción
        if filename is None or len(filename) < 3 or filename[-2] is not "." or filename[-1] is not "c":
            raise NameError
        #En caso de que no salte la excepción se abre el archivo
        file = open(filename, mode= 'r')
        #Y se copia su contenido en el cuadro de texto asignado al código
        texto = file.read()
        code.delete(1.0,tkinter.END)
        code.insert(tkinter.END, texto)
        file.close()
        savebutton.config(state=tkinter.DISABLED)
        compilebutton.config(state=tkinter.NORMAL)
        exebutton.config(state=tkinter.NORMAL)
        debugbutton.config(state=tkinter.NORMAL)
        compiled = False
    except NameError:
        #Ventana emergente notificando un error con el nombre de archivo inalido
        filename=None
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
        #se sobreescribe el archivo con el nuevo contenido extraido del cuadro de texto destinado al código
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
        #Se solicita el nombre de un archivo para sobreescribirlo o crear uno nuevo
        filename = filedialog.asksaveasfilename(title = "Selecciona un archivo tipo C",filetypes = [("Archivo C","*.c")])
        #en caso de que el archivo no tenga la extension incorrecta saltará una excepción
        if filename is None or len(filename) < 3 or filename[-2] is not "." or filename[-1] is not "c":
            raise NameError
        #se sobreescribe el archivo con el nuevo contenido extraido del cuadro de texto destinado al código
        file = open(filename, mode= 'w+')
        texto = code.get(1.0, tkinter.END)
        file.write(texto)
        file.close()
        savebutton.config(state=tkinter.DISABLED)
        exebutton.config(state=tkinter.NORMAL)
        debugbutton.config(state=tkinter.NORMAL)
        saved = True  
    except NameError:
        #Ventana emergente notificando un error con el nombre de archivo invalido
        filename=None
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
    #si no se han guardado los cambios del archivo se hará automaticamente
    if not saved:
        guardar()
    code.tag_delete("err")
    #se llamará a la consola de comandos para hacer un gcc
    command = "gcc " + filename + " -g -o " + filename[:-2] + " && echo ok || echo err"
    retorno=str(check_output(command, stderr=subprocess.STDOUT, shell=True))[2:-1]
    #si se compila con exito 
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
                try:
                    inicio=str(float(error))
                    fin=str(float(error)+1)
                except ValueError:
                    None
                else:
                    code.tag_add("err",inicio,fin)
                    
                    code.tag_config("err",background="red", foreground="white")
            retorno=retorno[pos+2:]
        raise Exception


def ejecutar():
    '''
    utiliza la consola del sistema para ejecutar un archivo .c previamente compilado
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
        #Se ejecuta el programa a traves de la consola del sistema
        command = filename[:-2] + " && echo ok || echo err"
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
    global debugging
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
        #crea el diccionario de estructuras
        estructuras = dict()
        #crea el diccionario de funciones
        funciones = dict()
        #llama al parser para generar el arbol a evaluar por la aplicación
        parser = pycparser.parse_file(filename)
        iterar = iter(parser)
        try:
            while(True):
                #Se recorre el arbol
                siguiente = next(iterar)
#                print(siguiente.show())
                #si se encuentra con la declaración de un struct lo añadimos al diccionario de structs
                if isinstance(siguiente, pycparser.c_ast.Decl):
                    if isinstance(next(iter(siguiente)), pycparser.c_ast.Struct):
                        structs(next(iter(siguiente)))
                #si se encuantra con la deficnición de una función lo añadimos al diccionario de funciones
                elif isinstance(siguiente, pycparser.c_ast.FuncDef):
                    nombre = getattr(next(iter(siguiente)),'name')
                    funciones[nombre]=siguiente
        except StopIteration:
            #Se pone como verdadera la variable de si se está debuggeando
            debugging = True
            #Se recicla el mismo botón para entrar y salir del modo debug
            debugbutton.config(text="Salir del modo debug", command=debugoff, image=iconstop, width=30, height=30)
            debugbutton_ttp.text="Salir del modo debug"
            #Se deshabilitan los botones que no vamos a usar durante el debuggueo
            newbutton.config(state=tkinter.DISABLED)
            openbutton.config(state=tkinter.DISABLED)
            exebutton.config(state=tkinter.DISABLED)
            nextbutton.config(state=tkinter.NORMAL)
            stepbutton.config(state=tkinter.NORMAL)
            code.config(state=tkinter.DISABLED)
            #Se crea la lista de bicolas para poder ir recorriendo las funciones
            iterexec = list()
            #Se añade el main
            iterexec.append(copy.deepcopy(deque(dict(funciones['main'].children())['body'])))
            #Se crea la lista de diccionarios para almacenar las variables
            vardicts = list()
            #Se añade el primer diccionario para las variables del main
            vardicts.append(["main",dict()])
            #Se crea la bicola para los retornos
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
            #Cuando termine de ejecutar una función borrará el último componente de las listas tanto de funciones a ejecutar como la de la lista de diccionarios de variables
            iterexec.pop()
            vardicts.pop()
            nextline()
        except IndexError:
            #Cuando finalice la ejcucción del archivo lo notificará con una ventana emergente
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
    #Se captura la excepción llamada a función para poder trabajar con ella
    except FuncCallError:
        iterexec[-2].appendleft(line)
    #Se captura la excepción de retorno para poder vaciar la pila de ejecución de la función actual
    except ReturnError:
        while(True):
            try:
                iterexec[-1].pop()
            except IndexError:
                break
    finally:
        #Se imprimen las variables
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
    '''
    esta función se ejecuta cada vez que el usuario pulsa el botón step
    llama en bucle aa nextline para ir ejecutando las funciones enteras en vez de ir linea a linea
    '''
    fin = len(iterexec)
    nextline()
    #Bucle con el que se van ejecutando lineas hasta finalizar la ejecución de una función
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
#        print(line)
        #Inicializacion de structs
        if isinstance(line.type.type, pycparser.c_ast.Struct):
            vardicts[-1][1][line.name][0] = line.type.type.name+"(Struct)"
            vardicts[-1][1][line.name][1] = copy.deepcopy(estructuras[line.type.type.name])
            
        #Declaracion de arrays
        elif isinstance(line.type, pycparser.c_ast.ArrayDecl):
            vardicts[-1][1][line.name][1] = list()
            vardicts[-1][1][line.name][0] = arraydecl(line.type,vardicts[-1][1][line.name][1])
            
        #Otros
        else:
            vardicts[-1][1][line.name][0] = line.type.type.names[0]
            
        #Igualar a retorno de funcion
        if isinstance(line.init, pycparser.c_ast.FuncCall):
            if line.init.name.name in funciones:
                line.init = innerfunction(line.init)
                raise FuncCallError
            else:
                line.init = outterfunction(line.init) 
        
        #Valor inicial en arrays
        elif isinstance(line.init, pycparser.c_ast.InitList):
            initlist(line.init,vardicts[-1][1][line.name][1])
            
        #Valor inicial
        elif line.init is not None:
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
    Llamadas a funciones propias del archivo
    
    Devuelve las funciones transformadas en su valor de retorno
    '''
    cabecera = dict()
    #se van analizando las variables pasadas por cabecera
    for i in range(len(funciones[line.name.name].decl.type.args.params)):
        #Recursividad para casos como: F(G(x))
        if isinstance(line.args.exprs[i], pycparser.c_ast.FuncCall):
            if line.args.exprs[i].name.name in funciones:
                line.args.exprs[i] = innerfunction(line.args.exprs[i])
                raise FuncCallError
            else:
                line.args.exprs[i] = outterfunction(line.args.exprs[i])
        cabecera[funciones[line.name.name].decl.type.args.params[i].name] = [funciones[line.name.name].decl.type.args.params[i].type.type.names[0],getvalue(line.args.exprs[i])]
    #Se añade a la lista de funciones que ejecutar a la que se ha llamado
    iterexec.append(copy.deepcopy(deque(funciones[line.name.name].body)))
    #se añade a la lista de varibles las variables internas de la nueva función
    vardicts.append([line.name.name,cabecera])
    funcion=copy.deepcopy(line)
    #Se crea un tipo constante para poder asignar un valor a la función
    line=pycparser.c_ast.Constant(None,None)
    line.type=funciones[funcion.name.name].decl.type.type.type.names[0]
    #se añade esa constante a la pila de retornos
    if line.type != "void":
        retornos.append(line)
    #Se devuelve el valor de funcion en forma de constante
    return line
    



def outterfunction(line):
    '''
    Llamadas a funciones originales de C
    '''
    #En caso de que la función sea hacer un print
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
    #En caso de que la función sea hacer un scan
    elif "scanf" == line.name.name:
        scanf(line)
    #En caso de que la función sea copiar string en una variable
    elif "strcpy" == line.name.name:
        rstring = line.args.exprs[1].value
        lstring = vardicts[-1][1][line.args.exprs[0].name.name][1][line.args.exprs[0].field.name][1]
        for i in range(len(rstring[1:-1])):
            lstring[i]=rstring[i+1]
    #En caso de que la función sea una potencia
    elif "pow" == line.name.name:
        resultado = float(line.args.exprs[0]**line.args.exprs[1])
        return pycparser.c_ast.Constant("double",str(resultado))
    #En caso de que la función sea una raiz cuadrada
    elif "sqrt" == line.name.name:
        resultado = math.sqrt(line.args.exprs[0])
        return pycparser.c_ast.Constant("double",str(resultado))
        



def scanf(line):
    '''
    Lanza una ventana emergente para introducir el valor solicitado por el scanf
    '''
    def escanear():
        #Obtiene el valor del cuadro de texto
        value.value=valueentry.get()
        scan.destroy()
        #y se lo asigna a la variable correspondiente
        asignacion = pycparser.c_ast.Assignment("=",line.args.exprs[1],value)
        try:
            evalline(asignacion)
        except ValueError:
            #ventana emergente en caso de que se haya introducido un valor incorrecto
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
            stepbutton.config(state=tkinter.NORMAL)
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
    #se almacena en el diccionario asigando a las estructuras la estructura recien declarada
    estructuras[line.name]=newst
    



def arraydecl(line,og):
    '''
    Declaracion de arrays, necesario para hacerlos multidimensionales
    
    TODO: inicializar los arrays => int x[]={1,2}
    '''
    global vardicts
    #se crea un array del tamaño correspondiente con valores vacios
    for i in range(int(line.dim.value)):
        #Recursividad en el caso de que el array sea multidimensional
        if isinstance(line.type, pycparser.c_ast.ArrayDecl):
            og.append([])
            retorno = arraydecl(line.type,og[i])
        else:
            og.append(None)
            retorno = line.type.type.names[0]
    #Para mostrar el tipo del array con sus dimensiones
    retorno += "["+ line.dim.value +"]"
    return retorno



def initlist(line,og):
    '''
    Inicializa los valores de un array
    
    TODO: inicializar los arrays => int x[]={1,2}
    '''
    global vardicts
    n=0
    #se asignan los valores iniciales a un array
    for i in line:
        #recursividad en caso de que sea multidimensional
        if isinstance(i, pycparser.c_ast.InitList):
            initlist(i,og[n])
        else:
            og[n]=getvalue(i)
        n+=1


def arrayref(line):
    '''
    tomar la referencia de un array
    
    devuelve el array correspondiente
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
    
    la variable index pasada por cabecera se utiliza porque las variables de tipos primitivos son inmutables y si se pasa una lista permite modificar su valor
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
    
    devolverá el valor correspondiente para poder ser asignado a una variable
    '''
    global vardicts
    #en el caso i = 5 devuelve 5
    if isinstance(line, pycparser.c_ast.Constant):
        if "int" in line.type:
            return int(line.value)
        elif "double" in line.type:
            return float(line.value)
        return line.value
    #en el caso i = -5 devuelve -5
    elif isinstance(line, pycparser.c_ast.UnaryOp):
        return unary(line)
    #♣en el caso i = 3 + 2 devueve 5
    elif isinstance(line, pycparser.c_ast.BinaryOp):
        return binary(line)
    #en el caso a = 1; i = a devuelve 1
    elif isinstance(line, pycparser.c_ast.ID):
        return copy.copy(vardicts[-1][1][line.name][1])
    #devuelve el valor de una posicion del array
    elif isinstance(line, pycparser.c_ast.ArrayRef):
        return copy.copy(arrayref(line)[int(line.subscript.value)])
    #devuelve el valor de un campo del struct
    elif isinstance(line, pycparser.c_ast.StructRef):
        return copy.copy(vardicts[-1][1][line.name.name][1][line.field.name][1])



def unary(line):
    '''
    realiza operaciones con un solo operando como puede ser a++ o -b
    '''
    #manejo en el caso de que el operando sea una función
    if isinstance(line.expr, pycparser.c_ast.FuncCall):
        if line.expr.name.name in funciones:
            line.expr = innerfunction(line.expr)
            raise FuncCallError
        else:
            line.expr = outterfunction(line.expr)
    #manejo en el caso de que el operando sea una variable
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
    #manejo en el caso de que el operando sea un valor fijo
    return getvalue(line.expr)*-1
        
def binary(line):
    '''
    Obtine el valor de una operación aritmetologica como puede ser a&&b o 7+3
    
    en el caso de ser una operación con mas de un operando se utilizará recursividad
    ej: 3 + 5 + 7 => binary(binary(3,+,5),+,7)
    '''
    global vardicts
    global retornos
    operandos = list()
    
    #Obtencion de los operandos
    #manejo de las funciones en caso de que el primer operando sea una funcion
    if isinstance(line.left, pycparser.c_ast.FuncCall):
        if line.left.name.name in funciones:
            line.left = innerfunction(line.left)
            raise FuncCallError
        else:
            line.left = outterfunction(line.left)
    #manejo de las funciones en caso de que el segundo operando sea una funcion
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
    #distinto
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
    '''
    Excepcion creada para manejar las llamadas a función
    '''
    pass


class ReturnError(Exception):
    '''
    Excepcion creada para manejar los retornos
    '''
    pass



def debugoff():
    '''
    Sale del modo debug
    '''
    global debugging
    #Cambia el estado de los botones para que puedan ser usados de forma normal
    newbutton.config(state=tkinter.NORMAL)
    openbutton.config(state=tkinter.NORMAL)
    exebutton.config(state=tkinter.NORMAL)
    nextbutton.config(state=tkinter.DISABLED)
    stepbutton.config(state=tkinter.DISABLED)
    debugbutton.config(text="Acceder al modo debug", command=debugon, image=iconstart, width=30, height=30)
    debugbutton_ttp.text="Acceder al modo debug"
    #Permitimos la edición de codigo de nuevo
    code.config(state=tkinter.NORMAL)
    code.tag_delete("exe")
    #Borramos las variables
    variables.config(state=tkinter.NORMAL)
    variables.delete(1.0,tkinter.END)
    variables.config(state=tkinter.DISABLED)
    #Se pone como falsa la variable de si se está debuggeando
    debugging = False

def editado(texto):
    '''
    Se ejecuta esta funcion cada vez que el usuario modifica el codigo
    '''
    global saved
    global compiled
    global debugging
    code.tag_delete("err")
    #para evitar que ocurra durante la depuración
    if not debugging:
        #se desbloquean los botones de compilar y guardar si se modifica el codigo
        savebutton.config(state=tkinter.NORMAL)
        compilebutton.config(state=tkinter.NORMAL)
        #las variables internas para saber si se han guardado los cambios y si se ha compilado cambiarán a falso
        saved = False
        compiled = False
    

    
if __name__ == "__main__":
    #se genera la ventana con la que vamos a trabajar
    root = tkinter.Tk()
    #cargamos los iconos que usaremos en los botones del programa
    iconnew=tkinter.PhotoImage(file="icons/new.png").subsample(18,18)
    iconopen=tkinter.PhotoImage(file="icons/open.png").subsample(18,18)
    iconsave=tkinter.PhotoImage(file="icons/save.png").subsample(18,18)
    iconstart=tkinter.PhotoImage(file="icons/start.png").subsample(18,18)
    iconstop=tkinter.PhotoImage(file="icons/stop.png").subsample(18,18)
    iconcompile=tkinter.PhotoImage(file="icons/compile.png").subsample(18,18)
    iconexe=tkinter.PhotoImage(file="icons/execute.png").subsample(18,18)
    iconstep=tkinter.PhotoImage(file="icons/step.png").subsample(18,18)
    iconnext=tkinter.PhotoImage(file="icons/next.png").subsample(18,18)
    #Se da un nombre a la ventana del programa
    root.title("TFG")
    #Hace que el programa se inicie a pantalla completa
    root.state('zoomed')
    #Se define el frame en el que van a aparecer los botones
    frame = tkinter.Frame(root)
    frame.pack()
    #Se define el frame en el que irán el cuadro de texto del codigo y el que mostrará la variables
    textframe = tkinter.Frame(root)
    textframe.pack()
    #Se define el frame en el que irá el cuadro de texto
    consoleframe = tkinter.Frame(root)
    consoleframe.pack()
    #se genera el boton "nuevo"
    newbutton = tkinter.Button(frame, text="Nuevo", command=nuevo, image=iconnew, width=30, height=30)
    newbutton.pack( side = tkinter.LEFT)
    newbutton_ttp = ttp.CreateToolTip(newbutton, "Nuevo")
    #se genera el botón "abrir"
    openbutton = tkinter.Button(frame, text="Abrir", command=abrir, image=iconopen, width=30, height=30)
    openbutton.pack( side = tkinter.LEFT )
    openbutton_ttp = ttp.CreateToolTip(openbutton, "Abrir")
    #se genera el botón "guardar"
    savebutton = tkinter.Button(frame, text="Guardar", command=guardar, image=iconsave, width=30, height=30, state=tkinter.DISABLED)
    savebutton.pack( side = tkinter.LEFT )
    savebutton_ttp = ttp.CreateToolTip(savebutton, "Guardar")
    #se genera el botón "compilar"
    compilebutton = tkinter.Button(frame, text="Compilar",command=compilar, image=iconcompile, width=30, height=30, state=tkinter.DISABLED)
    compilebutton.pack( side = tkinter.LEFT )
    compilebutton_ttp = ttp.CreateToolTip(compilebutton, "Compilar")
    #se genera el botón "ejecutar"
    exebutton = tkinter.Button(frame, text="Ejecutar",command=ejecutar, image=iconexe, width=30, height=30, state=tkinter.DISABLED)
    exebutton.pack( side = tkinter.LEFT )
    exebutton_ttp = ttp.CreateToolTip(exebutton, "Ejecutar")
    #se genera el botón "Acceder al modo debug"
    debugbutton = tkinter.Button(frame, text="Acceder al modo debug",command=debugon, image=iconstart, width=30, height=30, state=tkinter.DISABLED)
    debugbutton.pack( side = tkinter.LEFT )
    debugbutton_ttp = ttp.CreateToolTip(debugbutton, "Acceder al modo debug")
    #se genera el botón para ejecutar siguiente linea entrando en función
    nextbutton = tkinter.Button(frame, text="Next",command=nextline, image=iconnext, width=30, height=30, state=tkinter.DISABLED )
    nextbutton.pack( side = tkinter.LEFT )
    nextbutton_ttp = ttp.CreateToolTip(nextbutton, "Ejecutar siguiente linea entrando en función")
    #se genera el botón para ejecutar siguiente linea saltando función
    stepbutton = tkinter.Button(frame, text="Skip",command=skip, image=iconstep, width=30, height=30, state=tkinter.DISABLED )
    stepbutton.pack( side = tkinter.LEFT )
    stepbutton_ttp = ttp.CreateToolTip(stepbutton, "Ejecutar siguiente linea saltando función")
    #se genera un cuadro de texto para modificar el código
    code = scrolledtext.ScrolledText(textframe, height=40, width=200)
    code.pack(side = tkinter.LEFT)
    #se genera un cuadro de texto para mostrar las variables
    variables = scrolledtext.ScrolledText(textframe, height=40, width=75)
    variables.pack(side = tkinter.RIGHT)
    variables.config(state=tkinter.DISABLED)
    #se genera un cuadro de texto para mostrar la salida de la consola
    consola = scrolledtext.ScrolledText(consoleframe, height=20, width=270)
    consola.pack(side = tkinter.BOTTOM)
    consola.config(state=tkinter.DISABLED)
    #cada vez que el usuario pulsa un tecla llama a la función editado
    code.bind('<KeyRelease>', editado)

    root.mainloop()