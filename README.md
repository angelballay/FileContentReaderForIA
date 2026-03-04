# FileContentReaderForIA

An open-source desktop tool designed to consolidate, filter, and minify entire codebases into a single plain text file. 

The philosophy behind this project is to **facilitate and optimize AI-assisted development**. Automated agents and integrated IDE tools often require more expensive subscriptions. This application allows any developer to extract the exact context of their project (whether it's a backend, frontend, or full-stack development) and package it into an optimized *payload*. This resulting file can be pasted directly into any standard conversational large language model (LLM), maximizing the context window and reducing token consumption.

## Main Features

* **Native Graphical User Interface (GUI)**
* **High-Performance Concurrent Processing**
* **Optional Code Minification**
* **Configuration Template System**
* **AI-Friendly Structure**

## 🛠️ Requirements and Installation

The tool is built using exclusively the Python standard library, so it does not require the installation of heavy external dependencies via `pip`.

1. Ensure you have **Python 3.x** installed on your system.
2. Clone this repository:
   ```bash
   git clone [https://github.com/angelballay/FileContentReaderForIA.git](https://github.com/angelballay/FileContentReaderForIA.git)
   cd FileContentReaderForIA



3. Run the application:
```bash
python init.py

```



## ⚙️ Usage and Configuration

Upon opening the application, you will find a control panel where you can adjust the following parameters:

* **Root Directory:** The main folder of your project that will be scanned recursively.
* **Extensions:** Comma-separated list of allowed formats (e.g., `.cs, .ts, .html, .json`).
* **Max Size (MB):** Filter to automatically exclude files that exceed a certain size (e.g., `1` or `25` MB), preventing the output file from being saturated with heavy *assets*.
* **Omissions:** Names of folders or files that will be completely ignored. This is vital for excluding build directories or dependencies like `node_modules`, `.git`, `bin`, `obj`, or `venv`.

### Included Template Examples

The `file_merger_configs.json` file comes with predefined configurations:

* **C# Backend:** Configured to read `.cs`, `.json` and omit `bin`, `obj`, `wwwroot`, and `logs`.
* **Angular:** Configured to read `.ts`, `.html`, `.scss` and omit `.angular`, `node_modules`, and `package-lock.json`.

Once the merging process is finished, the application will automatically open the system folder (compatible with Windows, macOS, and Linux) where your `resultado_final.txt` has been generated, ready to be sent to the AI.

## 🤝 Contributions

This project was born with the idea of being a free tool for the community. If you have ideas to improve the partitioning of very large files, add support for calculating token estimates, or improve the interface, contributions via *Pull Requests* are more than welcome!

---
# FileContentReaderForIA

Una herramienta de escritorio de código abierto diseñada para consolidar, filtrar y minificar bases de código completas en un único archivo de texto plano. 

La filosofía detrás de este proyecto es **facilitar y optimizar el desarrollo asistido por IA**. Los agentes automatizados y las herramientas integradas en los IDEs suelen requerir suscripciones mas costosas. Esta aplicación permite a cualquier desarrollador extraer el contexto exacto de su proyecto (ya sea un backend, un frontend o un desarrollo full-stack) y empaquetarlo en un *payload* optimizado. Este archivo resultante puede ser pegado directamente en cualquier modelo de lenguaje grande (LLM) conversacional estándar, maximizando la ventana de contexto y reduciendo el consumo de tokens.

## Características Principales

* **Interfaz Gráfica Nativa (GUI)**
* **Procesamiento Concurrente de Alto Rendimiento** 
* **Minificación de Código Opcional**
* **Sistema de Plantillas de Configuración** 
* **Estructura Amigable para la IA** 

## 🛠️ Requisitos e Instalación

La herramienta está construida utilizando exclusivamente la biblioteca estándar de Python, por lo que no requiere la instalación de dependencias externas pesadas mediante `pip`.

1. Asegúrate de tener **Python 3.x** instalado en tu sistema.
2. Clona este repositorio:
   ```bash
   git clone [https://github.com/angelballay/FileContentReaderForIA.git](https://github.com/angelballay/FileContentReaderForIA.git)
   cd FileContentReaderForIA

```

3. Ejecuta la aplicación:
```bash
python init.py

```



## ⚙️ Uso y Configuración

Al abrir la aplicación, te encontrarás con un panel de control donde puedes ajustar los siguientes parámetros:

* **Directorio Raíz:** La carpeta principal de tu proyecto que será escaneada recursivamente.
* **Extensiones:** Lista separada por comas de los formatos permitidos (ej. `.cs, .ts, .html, .json`).
* **Max Tamaño (MB):** Filtro para excluir automáticamente archivos que superen un peso determinado (ej. `1` o `25` MB), evitando saturar el archivo de salida con *assets* pesados.
* **Omisiones:** Nombres de carpetas o archivos que serán ignorados por completo. Es vital para excluir directorios de compilación o dependencias como `node_modules`, `.git`, `bin`, `obj` o `venv`.


Una vez finalizado el proceso de fusión, la aplicación abrirá automáticamente la carpeta del sistema (compatible con Windows, macOS y Linux) donde se ha generado tu `resultado_final.txt`, listo para ser enviado a la IA.

## 🤝 Contribuciones

Este proyecto nace con la idea de ser una herramienta libre para la comunidad. Si tienes ideas para mejorar el particionado de archivos muy grandes, añadir soporte para calcular estimaciones de tokens, o mejorar la interfaz, ¡las contribuciones mediante *Pull Requests* son más que bienvenidas!

