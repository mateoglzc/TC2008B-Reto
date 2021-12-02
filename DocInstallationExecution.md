# Proceso de instalación y ejecución de solución del reto

## Programas necesarios
- Conda o Miniconda (solo necesario si se quieren iniciar instancias locales del proyecto)
- Unity
- Git

## Instalación de Unity
1. Dirigirse a la página https://unity3d.com/get-unity/download
2. Descargar *Unity Hub*
3. Crear una cuenta de Unity
4. Descargar la versión de *Unity* 2020.3.22f1

## Instalación de repositorio
1. Abrir la terminal de preferencia
2. Dirigirse al directorio en el que se quiera almacenar el repositorio
3. Ingresar el comando `git clone https://github.com/mateoglzc/TC2008B-Reto.git` o `git clone git@github.com:mateoglzc/TC2008B-Reto.git`, de acuerdo a lo que se tenga configurado

## Instalación de Conda o Miniconda
1. Dirigirse a la página https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html
2. Descargar ya sea *Conda* o *Miniconda*, de acuerdo a las preferencias
3. En caso de no tenerlo, agregar el directorio del *bin* de *Conda* o *Miniconda* a las variables de ambiente del ordenador
4. Abrir la terminal de preferencia e ingresar al directorio raíz del repositorio local del proyecto
5. Ingresar el comando `conda create --name <nombre_de_ambiente> python=3.8 --file requirements.txt`
6. Ingresar `conda env list` para verificar que se haya creado correctamente el ambiente

## Ejecución del programa para el reto usando la nube
1. Abrir la escena de *Unity* contenida en `TC2008B-Reto/TC2008B_Unity/Assets/Reto/Scenes`
2. En caso de ser necesario, ingresar al objecto *Controller* de la escena y cambiar la variable *url* a `http://retotc2008b-resplendent-lynx-pw.mybluemix.net/`
3. Presionar el botón de *Play* que se contiene en la parte superior del editor de *Unity* una vez que se abra la escena 
4. Observar la ejecución de la simulación y pararlo cuando se desee

## Ejecución del programa para el reto usando una instancia local
1. Abrir la terminal de preferencia
2. Dirigirse al archivo de *Python* a ejecutar dentro del directorio `TC2008B-Reto/TC2008B_Python/reto`
3. Activar el ambiente creado en la instalación usando `conda activate <nombre_de_ambiente>`
4. Ingresar el comando `python api.py`
5. Esperar hasta que la instancia de *Flask* este corriendo completamente
6. Abrir la escena de *Unity* contenida en `TC2008B-Reto/TC2008B_Unity/Assets/Reto/Scenes`
7. En caso de ser necesario, ingresar al objecto *Controller* de la escena y cambiar la variable *url* a `http://localhost:8000/`
8. Presionar el botón de *Play* que se contiene en la parte superior del editor de *Unity* una vez que se abra la escena 
9. Observar la ejecución de la simulación y pararlo cuando se desee