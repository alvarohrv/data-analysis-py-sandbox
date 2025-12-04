# Base image
FROM python:3.12-slim
# Linux Debian Slim
# Con Python 3.12
# En arquitectura x86_64
# Muy liviana (sin herramientas como gcc, git, curl, etc.)

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app
# /app no es una ruta real de tu sistema WSL
# /app existe únicamente dentro del contenedor Docker

# Evitar que Python genere .pyc y mejorar logs en contenedor
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copiar requirements.txt al contenedor
COPY requirements.txt .
# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r /app/requirements.txt (otra forma de hacerlo, pero se definio WORKDIR)

# Copiamos el resto del proyecto
COPY . .
# Origen (tu PC Win11/Linux/Mac)
# Destino (contenedor) dentro de /app
# si se usa "COPY . ." quiere decir copiar todo el contexto de construcción (donde está el Dockerfile) eso incluye las carpetas ocultas .git, .vscode, etc.

# Puerto típico de JupyterLab
EXPOSE 8888

# Comando por defecto (puedes cambiarlo después)
CMD ["python", "src/main.py"]
# Puedes tener CMD para Python y aun así ejecutar Jupyter cuando quieras.
# define qué hace el contenedor automáticamente cuando lo ejecutas sin especificar un comando como:
# $ docker run --rm caso_estudio_01:v01 /// en lugar de $ docker run caso_estudio_01:v01 python src/main.py (Nota: comando no recomendable para proyectos reales (usar para verificar que la imagen quedó bien), ver las notas de como levantar el contenedor)

# Instalar dependencias del sistema necesarias (ejemplo típico)
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     git \
#     && rm -rf /var/lib/apt/lists/*
# Dejas comentado si: no necesitas dependencias del sistema adicionales, Solo usas librerías puras de Python (ej: pandas, matplotlib, etc), no necesitas Git dentro del contenedor, etc.
# Pero si al construir (docker build) te aparece algo como:
# error: gcc not found
# error: unable to execute 'gcc'
# → Entonces sí debes descomentarlas.

# # Comando por defecto (ejemplo: lanzar JupyterLab)
# CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
# -----------------------------------

# FROM : Define la imagen base desde la cual se construye la nueva imagen.
# WORKDIR : Establece el directorio de trabajo por defecto dentro del contenedor. Si no existe, lo crea.
# PATH: Es una variable del sistema que indica dónde buscar programas ejecutables.
# COPY : Sirve para copiar archivos desde tu proyecto (Windows/Git) hacia el sistema de archivos interno del contenedor.
# ENV : Define variables de entorno dentro del contenedor.

# -----------------------------------
# ---------------------------------- 
    
## Construir la imagen (mejor que “venv)
# $ docker build -t caso_estudio:v01 .
# $ docker build -t ds_hf_st_lab:i1125v1 .

# Docker busca el archivo Dockerfile en el directorio actual (.)
# -t permite dar un nombre o tag a la imagen (aquí: caso_estudio_01)
# Esto se ejecuta una sola vez, crea la imagen y la guarda en Docker o cuando instalas nuevas librerías en requirements.txt
# Docker hace:
# Descarga Python 3.12
# Crea /app dentro del contenedor
# Copia tu requirements.txt
# Instala pandas, numpy, ipython, matplotlib, etc dentro del contenedor
# Copia todo tu proyecto
# Guarda esa imagen en el sistema de Docker (en WSL2)

# ---------------------------------- 

## Ejecutar tu proyecto .py dentro del contenedor (sin Jupyter) y abrir un bash
### Para correr un archivo Python: (opcion01 - 01a y 01b)
#01a #PowerShell $ docker run -it --rm -v %cd%:/app caso_estudio_01:v01
# Este comando USA el CMD del Dockerfile (python src/main.py) <3
#01b #PowerShell $ docker run -it --rm -v %cd%:/app caso_estudio_01:v01 python src/otro.py 
# Ignora el CMD del Dockerfile y ejecuta python src/main.py o el que se indique
# Monta tu carpeta actual a /app
# Ejecuta python src/main.py dentro del contenedor
### Ruta absoluta en Windows: (opcion02)
# $ docker run -it --rm -v "C:/Users/alvar/Dropbox/_Programacion_/____AnalisisDatos(py)/caso_estudio_01":/app caso_estudio_01:v01 python src/main.py
# (nota: las rutas con paréntesis en su nombre deben ir entre comillas.)
# Es el equivalente de hacer esto en tu PC: python src/main.py
# Se usa para entrar “a mano” al contenedor
# No es el comando de trabajo diario.
# este comando hace:
# Crea un contenedor basado en la imagen caso_estudio_01
# Ejecuta python src/main.py dentro del contenedor
# %cd% → variable de entorno de PowerShell en Windows que representa el directorio actual (current directory). Útil cuando ya estás en la carpeta del proyecto y quieres montar exactamente ese lugar. Monta tu carpeta actual (%cd%) en Windows a /app dentro del contenedor
### Usar Git Bash o WSL (opcion03) $ docker run -it --rm -v $(pwd):/app caso_estudio_01:v01 python src/main.py

### Explicación de opciones comunes de docker run:
# -it : modo interactivo con terminal, permite ver salidas y escribir comandos (Mantiene vivo el proceso)
# --rm : elimina el contenedor al salir, para no llenar el disco con contenedores parados (nunca elimina la imagen base, solo el contenedor temporal y puede luego crear nuevas instancia) /// para deterner el contenedor: Ctrl + C o escribir exit en la terminal del contenedor (dado que se uso --rm).
# -d : modo “desapegado” (detached) (Devuelve el control), corre en segundo plano (no interactivo),El proceso del contenedor sigue corriendo, pero la terminal queda libre para otros comandos. Docker imprime el ID del contenedor y devuelve el control a la consola.
## Si el contenedor está en segundo plano (-d), puedes ver su estado con:
## docker ps
## docker stop miapp # detiene el contenedor
## docker rm miapp # elimina el contenedor detenido

# ---name xxxx: da un nombre al contenedor (opcional, para referenciarlo luego más fácilmente)
# -p : mapea puertos entre el contenedor y el host; NOTA: Sintaxis: -p <puerto_host>:<puerto_contenedor> //// Ejemplo: -p 8888:8888 para acceder a JupyterLab desde el navegador del host, o para exponer servicios web, APIs, etc.
# -v : monta volúmenes (carpetas) entre el host y el contenedor; NOTA: Sintaxis: -v <ruta_host>:<ruta_contenedor> ///  Ejemplo: -v C:\proyecto:/app para que el código local esté disponible dentro del contenedor y los cambios se persistan.
## Puerto del host (el primero): 8888 (el que usas en tu navegador o cliente).
## Puerto del contenedor (el segundo): 8888 (donde el servicio escucha dentro del contenedor).
## Cada servicio (Apache, Nginx, JupyterLab) dentro del contenedor escucha en un puerto específico, que se define en su configuración o es el puerto por defecto:
## Apache: por defecto escucha en el puerto 80 (HTTP) o 443 (HTTPS).
## Nginx: por defecto también escucha en el puerto 80 o 443.
## JupyterLab: por defecto escucha en el puerto 8888.
## PERO, Si quieres exponer Apache en el puerto 8888 de tu máquina: $ docker run -p 8888:80 httpd ///// pero se accede desde http://localhost:8888

# -d e -it se pueden usar juntos, pero conceptualmente se contraponen:
# - -it: quiere mantener la terminal **adjunta** al contenedor.
# - -d: quiere mantener el contenedor **despegado** de la terminal.
# El profe dice "Una vez que el contenedor se está ejecutando (gracias a -it), el d hace que Docker devuelva el control a su terminal principal de Windows/WSL" lo que es cierto, pero en la práctica rara vez se usan juntos.

# ---------------------------------- 

## Iniciar Jupyter Lab dentro del contenedor
### Ruta absoluta en Windows: (opcion01)
# $ docker run --rm -p 8888:8888 -v "C:/Users/alvar/Dropbox/_Programacion_/____AnalisisDatos(py)/caso_estudio_01":/app caso_estudio_01:v01 jupyter lab --ip=0.0.0.0 --allow-root
# (Nota: En Windows PowerShell y CMD, el símbolo ^ sirve para indicar que la línea continúa en la siguiente, similar a \ en Linux aunque no se usa en este caso.)
### Si estás ya en la carpeta del proyecto en PowerShell (Windows): (opcion02)
# $ docker run --rm -p 8888:8888 -v %cd%:/app caso_estudio_01:v01 jupyter lab --ip=0.0.0.0 --allow-root

# este comando hace:
# Crea un contenedor basado en la imagen caso_estudio_01:v01
# Mapea el puerto 8888 del contenedor al puerto 8888 de tu máquina
# Monta tu carpeta actual (%cd%) en Windows a /app dentro del contenedor
# Inicia el contenedor y ejecuta el comando por defecto (lanzar JupyterLab)
# NOTA: En Linux/Mac usar -v $(pwd):/app en lugar de -v %cd%:/app
# NOTA: Si usas VSCode, instala la extensión "Remote - Containers" para trabajar directamente dentro del contenedor.

# Y abres:
# http://localhost:8888/
# Todo lo que hagas en los notebooks se guardará en tu carpeta de Windows.


# otra nota:
#  ¿Por qué NO debes usar ese comando para tus proyectos? ❌❌❌❌
# $ docker run caso_estudio_01:v01 python script.py   #(ya no es python script.py)
# $ docker run caso_estudio_01:v01 script.py  ///Solo tu Dockerfile tiene: CMD ["python", "script.py"]
# Respuesta: Porque no monta tu carpeta de proyecto, por tanto: vo puedes guardar cambios, No puedes editar notebooks, No puedes acceder a tus datos, El archivo script.py debe estar dentro de la imagen, no en Windowss, No verás tus notebooks o outputs en tu máquina.
# Docker ejecuta (python src/main.py) dentro del contenedor, pero no tiene acceso a tu código o datos en Windows.
# El comando "sencillo" solo sirve para pruebas o demos rápidas.
# EJ # $ docker run python:3.11 python -c "print(2+2)"