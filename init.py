import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import concurrent.futures
import logging
import platform
import subprocess

# Función para minificar el texto: reemplaza múltiples espacios y saltos de línea por un solo espacio
def minify_text(text):
    return re.sub(r'\s+', ' ', text).strip()

# Función para leer un archivo
def leer_archivo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        return ruta_archivo, contenido
    except Exception as e:
        logging.error(f"Error al leer {ruta_archivo}: {e}")
        return ruta_archivo, None

# Función principal de procesamiento
def process_files(directorio_raiz, extensiones, tamano_maximo_bytes, omisiones, ruta_salida, log_callback, minificar):
    archivos_a_procesar = []
    log_callback("Iniciando recorrido de directorios...")
    
    # Recorrer directorios y subdirectorios
    for root, dirs, files in os.walk(directorio_raiz):
        for file in files:
            ruta_completa = os.path.join(root, file)
            # Validar extensión
            if not any(ruta_completa.lower().endswith(ext.lower().strip()) for ext in extensiones):
                continue
            # Validar tamaño
            try:
                tamano = os.path.getsize(ruta_completa)
            except Exception as e:
                log_callback(f"Error obteniendo tamaño de {ruta_completa}: {e}")
                continue
            if tamano > tamano_maximo_bytes:
                continue
            # Validar omisiones
            if any(omision.strip() in ruta_completa for omision in omisiones if omision.strip()):
                continue

            archivos_a_procesar.append(ruta_completa)
    
    log_callback(f"Archivos a procesar: {len(archivos_a_procesar)}")
    
    resultados = []
    # Lectura concurrente de archivos
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_archivo = {executor.submit(leer_archivo, archivo): archivo for archivo in archivos_a_procesar}
        for future in concurrent.futures.as_completed(future_to_archivo):
            ruta, contenido = future.result()
            if contenido is not None:
                resultados.append((ruta, contenido))
    
    # Ordenar resultados por ruta (se puede modificar el criterio de ordenación)
    resultados.sort(key=lambda x: x[0])
    
    # Escribir en el archivo de salida
    try:
        with open(ruta_salida, 'w', encoding='utf-8') as salida:
            # Sección introductoria con explicación de los delimitadores
            salida.write("Este archivo contiene la concatenación de varios archivos.\n")
            salida.write("Los delimitadores utilizados son:\n")
            salida.write("  <<<FILE: ruta>>>  -> Indica el inicio del contenido de 'ruta'.\n")
            salida.write("  <<<END: ruta>>>   -> Indica el fin del contenido de 'ruta'.\n\n")
            
            for ruta, contenido in resultados:
                # Si está activada la opción, minifica el contenido
                if minificar:
                    contenido = minify_text(contenido)
                header = f"<<<FILE:{ruta}>>>\n"
                footer = f"<<<END:{ruta}>>>\n"
                salida.write(header)
                salida.write(contenido)
                salida.write("\n")
                salida.write(footer)
                salida.write("\n\n")
        log_callback(f"Proceso completado. Archivo generado: {ruta_salida}")

        # Abrir la carpeta contenedora del archivo de salida
        folder = os.path.dirname(os.path.abspath(ruta_salida))
        log_callback(f"Abriendo carpeta: {folder}")
        if os.name == 'nt':  # Windows
            os.startfile(folder)
        elif os.name == 'posix':
            if platform.system() == "Darwin":
                subprocess.call(["open", folder])
            else:
                subprocess.call(["xdg-open", folder])
    except Exception as e:
        log_callback(f"Error al escribir el archivo de salida: {e}")

# Función para iniciar el procesamiento en un hilo aparte
def iniciar_proceso():
    # Obtener parámetros de la interfaz
    directorio = entry_directorio.get()
    if not os.path.isdir(directorio):
        messagebox.showerror("Error", "El directorio raíz no es válido.")
        return

    extensiones = entry_extensiones.get().split(',')
    try:
        max_mb = float(entry_tamano.get())
    except ValueError:
        messagebox.showerror("Error", "El tamaño máximo debe ser un número (MB).")
        return
    tamano_bytes = int(max_mb * 1024 * 1024)
    omisiones = entry_omisiones.get().split(',')
    salida = entry_salida.get().strip()
    if not salida:
        messagebox.showerror("Error", "Debe especificar un archivo de salida.")
        return

    # Obtener el estado de la opción de minificar
    minificar = var_minificar.get()

    # Limpiar log
    txt_log.delete(1.0, tk.END)
    log("Iniciando proceso de archivos...")

    # Ejecutar el procesamiento en un hilo para no bloquear la interfaz
    thread = threading.Thread(
        target=process_files,
        args=(directorio, extensiones, tamano_bytes, omisiones, salida, log, minificar)
    )
    thread.start()

# Función para seleccionar el directorio raíz mediante un diálogo
def seleccionar_directorio():
    directorio = filedialog.askdirectory()
    if directorio:
        entry_directorio.delete(0, tk.END)
        entry_directorio.insert(0, directorio)

# Función para seleccionar el archivo de salida mediante un diálogo
def seleccionar_salida():
    salida = filedialog.asksaveasfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if salida:
        entry_salida.delete(0, tk.END)
        entry_salida.insert(0, salida)

# Función para agregar mensajes al log (asegura actualizar la GUI desde el hilo principal)
def log(mensaje):
    txt_log.insert(tk.END, mensaje + "\n")
    txt_log.see(tk.END)

# ------------------------
# Configuración de la Interfaz Tkinter
# ------------------------
ventana = tk.Tk()
ventana.title("Procesador de Archivos")

# Etiqueta y entrada para directorio raíz
lbl_directorio = tk.Label(ventana, text="Directorio raíz:")
lbl_directorio.grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_directorio = tk.Entry(ventana, width=50)
entry_directorio.grid(row=0, column=1, padx=5, pady=5)
btn_directorio = tk.Button(ventana, text="Seleccionar...", command=seleccionar_directorio)
btn_directorio.grid(row=0, column=2, padx=5, pady=5)

# Etiqueta y entrada para extensiones permitidas
lbl_extensiones = tk.Label(ventana, text="Extensiones permitidas (coma separadas):")
lbl_extensiones.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_extensiones = tk.Entry(ventana, width=50)
entry_extensiones.insert(0, ".txt, .log, .js, .css, .html, .sass, .cs, .aspx, .ts,")
entry_extensiones.grid(row=1, column=1, padx=5, pady=5)

# Etiqueta y entrada para tamaño máximo (en MB)
lbl_tamano = tk.Label(ventana, text="Tamaño máximo (MB):")
lbl_tamano.grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_tamano = tk.Entry(ventana, width=50)
entry_tamano.insert(0, "1")
entry_tamano.grid(row=2, column=1, padx=5, pady=5)

# Etiqueta y entrada para omisiones
lbl_omisiones = tk.Label(ventana, text="Omisiones (cadenas separadas por coma):")
lbl_omisiones.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_omisiones = tk.Entry(ventana, width=50)
entry_omisiones.insert(0,"node_modules,.git,")
entry_omisiones.grid(row=3, column=1, padx=5, pady=5)

# Etiqueta y entrada para archivo de salida
lbl_salida = tk.Label(ventana, text="Archivo de salida:")
lbl_salida.grid(row=4, column=0, padx=5, pady=5, sticky="e")
entry_salida = tk.Entry(ventana, width=50)
entry_salida.insert(0, "resultado_final.txt")
entry_salida.grid(row=4, column=1, padx=5, pady=5)
btn_salida = tk.Button(ventana, text="Guardar como...", command=seleccionar_salida)
btn_salida.grid(row=4, column=2, padx=5, pady=5)

# Checkbutton para activar la minificación del contenido
var_minificar = tk.BooleanVar(value=False)
chk_minificar = tk.Checkbutton(ventana, text="Minificar archivo", variable=var_minificar)
chk_minificar.grid(row=5, column=1, padx=5, pady=5, sticky="w")

# Botón para iniciar el proceso
btn_iniciar = tk.Button(ventana, text="Ejecutar", command=iniciar_proceso, bg="lightgreen")
btn_iniciar.grid(row=6, column=1, padx=5, pady=10)

# Área de texto para el log de salida
txt_log = scrolledtext.ScrolledText(ventana, width=80, height=15)
txt_log.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

# Configurar logging para errores en consola (opcional)
logging.basicConfig(level=logging.ERROR)

ventana.mainloop()
