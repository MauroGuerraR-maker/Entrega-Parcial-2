#Importamos las librerias necesarias
import tkinter as tk
from tkinter import messagebox
import firebase_admin
from firebase_admin import credentials, db

# ---------------- CONFIGURACION FIREBASE ---------------- #

# Cargar credenciales desde el archivo .json
cred = credentials.Certificate("BaseDeDatos.json")          #Rellenar con el Nuevo JSON
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://test-parcial-2-default-rtdb.firebaseio.com/"     #Reemplazar por el link del proyecto
})

# ---------------- CLASES ---------------- #
#Definimos las diferentes clases a tener en cuenta en el sistema de base de datos
class Libro:
    def __init__(self, titulo, autor, categoria, estado):
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.estado = estado

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "categoria": self.categoria,
            "estado": self.estado
        }

# ---------------- FUNCIONES UI ---------------- #
#Definimos las diferentes funciones a tener en cuenta en el sistema de base de datos

def registrar_libro():
    def guardar():                         #Guardamos las diferentes entradas y var definidas anteriormente
        titulo = entrada_titulo.get()
        autor = entrada_autor.get()
        categoria = categoria_var.get()
        estado = estado_var.get()
        if titulo and autor:
            libro = Libro(titulo, autor, categoria,estado)
            db.reference("libros").push(libro.to_dict())         #Subimos los datos
            messagebox.showinfo("Éxito", "Libro registrado en Firebase.")  #Establecemos un mensaje de confirmacion al realizar el push
            ventana.destroy()            #Cerramos la ventana una vez subidos los datos
        else:
            messagebox.showerror("Error", "Completa todos los campos.") #Mensaje de error

    #Configuramos la interfaz grafica de la ventana de registro
    ventana = tk.Toplevel()
    ventana.title("Registrar Libro")
    ventana.geometry("400x300")

    #Definimos los widgets a utilizar dentro de la ventana
    tk.Label(ventana, text="Título del libro:").pack()
    entrada_titulo = tk.Entry(ventana)      #Entrada de Titulo del libro
    entrada_titulo.pack()

    
    tk.Label(ventana, text="Autor:").pack()
    entrada_autor = tk.Entry(ventana)       #Entrada de Autor
    entrada_autor.pack()

    tk.Label(ventana, text="Categoría:").pack()
    categoria_var = tk.StringVar(ventana)         #Definicion de la categoria del libro
    categoria_var.set(categorias[0])
    tk.OptionMenu(ventana, categoria_var, *categorias).pack()

    tk.Label(ventana, text="Estado:").pack()
    estado_var = tk.StringVar(ventana)            #Definicion de la estado del libro
    estado_var.set(estado[0])
    tk.OptionMenu(ventana, estado_var,*estado).pack()

    tk.Button(ventana, text="Guardar", command=guardar).pack(pady=10) #Boton para guardar cambios

def buscar_libro():                    #Deficion de la funcion buscar_libro
    def buscar():
        query = entrada_busqueda.get().lower()      
        lista_resultados.delete(0, tk.END)                 #Se obtienen los datos presentes en Firebase
        libros_firebase = db.reference("libros").get()
        if libros_firebase:
            for datos in libros_firebase.values():             
                if query in datos["titulo"].lower():       #Definimos la busqueda por Titulo
                    lista_resultados.insert(tk.END, f'{datos["titulo"]} - {datos["autor"]} [{datos["categoria"]}] [{datos["estado"]}]')
                if query in datos["autor"].lower():        #Definimos la busqueda por Autor
                    lista_resultados.insert(tk.END, f'{datos["titulo"]} - {datos["autor"]} [{datos["categoria"]}] [{datos["estado"]}]')
                if query in datos["estado"].lower():       #Definimos la busqueda por Estado
                    lista_resultados.insert(tk.END, f'{datos["titulo"]} - {datos["autor"]} [{datos["categoria"]}] [{datos["estado"]}]')
        else:
            lista_resultados.insert(tk.END, "No hay libros registrados.") #Mensaje de error
    def regresar():
        ventana.destroy()        #Definicion para regresar a la ventana principal

    #Interfaz grafica de la ventana de busqueda de libros
    ventana = tk.Toplevel()
    ventana.title("Buscar Libro")       #Caracteristicas de la ventana
    ventana.geometry("400x300")

    #Definimos los widgets a utilizar dentro de la ventana
    tk.Label(ventana, text="Buscar por título, autor y estado:").pack()
    entrada_busqueda = tk.Entry(ventana)  #Caracteristicas del buscador
    entrada_busqueda.pack()

    tk.Button(ventana, text="Buscar", command=buscar).pack() #Boton para realizar la busqueda

    lista_resultados = tk.Listbox(ventana, width=50)
    lista_resultados.pack(pady=10)                        #Se muestra el resultado de la busqueda

    tk.Button(ventana, text="Regresar", command=regresar).pack()  #Se regresa a la ventana principal


# ---------------- INTERFAZ VENTANA PRINCIPAL ---------------- #

#Definicion de variables con botones mediante listas ( categoria y estado )
categorias = ["Ciencia", "Literatura", "Ingenieria"]
estado = ["Prestado", "Disponible"]

#Configuramos la interfaz grafica de la ventana principal
root = tk.Tk()
root.title("Biblioteca Universitaria")
root.geometry("400x300")

#Definimos los widgets a utilizar dentro de la ventana
tk.Label(root, text="Simulador Biblioteca", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Registrar Libro", width=25, command=registrar_libro).pack(pady=5)
tk.Button(root, text="Buscar Libro", width=25, command=buscar_libro).pack(pady=5)

tk.Label(root, text="Desarrollado por: Mauro Guerra").pack(side="bottom", pady=10)

root.mainloop()   #Se establece el mainloop para que la ventana continue abierta
