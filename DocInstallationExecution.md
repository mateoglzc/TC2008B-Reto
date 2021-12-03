# Proceso de instalación y ejecución de solución del reto

## Secciones
1. [Programas necesarios](#programas-necesarios)
2. [Instalación de Unity](#instalación-de-unity)
3. [Instalación de repositorio](#instalación-de-repositorio)
4. [Instalación de Conda o Miniconda](#instalación-de-conda-o-miniconda)
5. [Instalación de Cloud Foundry CLI](#instalación-de-cloud-foundry-cli)
6. [Ejecución del programa para el reto usando la nube](#ejecución-del-programa-para-el-reto-usando-la-nube)
7. [Ejecución del programa para el reto usando una instancia local](#ejecución-del-programa-para-el-reto-usando-una-instancia-local)

## Programas necesarios
- Conda o Miniconda (solo necesario si se quieren iniciar instancias locales del proyecto)
- Unity
- Git

## Instalación de Unity
1. Dirigirse a la página https://unity3d.com/get-unity/download
2. Descargar *Unity Hub*
3. Crear una cuenta de Unity
4. Abrir la liga https://unity3d.com/unity/qa/lts-releases
5. Descargar la versión de *Unity* 2020.3.22f1 desde la página web

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

## Instalación de Cloud Foundry CLI
***Esta herramienta es necesaria para la ejecución del programa para el reto utilizando la nube. Al igual cabe mencionar que para la utilización de esta es necesario contar con una cuenta de IBM Cloud.***


1. Dirigirse a la pagina de [Cloud Foundry CLI](https://github.com/cloudfoundry/cli#downloads).
2. Seleccionar el apartado **"Install V8"**.
3. Serás redirigido a una pagina en donde se encuentran las direcciones para instalar el programa en diferentes sistemas operativos. Este se puede instalar por medio de una terminal o por medio de un instalador.

## Ejecución del programa para el reto usando la nube
1. Instalar la herramienta *Cloud Foundry CLI* y contar con una cuenta de *IBM Cloud*.
2. Abrir la terminal de preferencia.
3. Dirigirse al directorio `TC2008B-Reto/TC2008B_Python/reto`.
4. Ingresar el comando `cf api <API-Endpoint>` sustituyendo *API-Endpoint* por algún *url* presentado en la tabla siguiente.

|URL                             |Region          |
|:-------------------------------|:---------------|
| https://api.ng.bluemix.net     | US South       |
| https://api.eu-de.bluemix.net  | Germany        |
| https://api.eu-gb.bluemix.net  | United Kingdom |
| https://api.au-syd.bluemix.net | Sydney         |
  
5. Ya que le proceso anterior se termine, ingresar el comando `cf login`.
6. Ingresar tu usuario y contraseña de tu cuenta de *IBM Cloud*.
7. Ya que le proceso anterior se termine, ingresar el comando `cf push`.
8. Esto iniciara el proceso despliegue a la nube. Al concluir este proceso se te proporcionara con un enlace semejante a `Retotc2008b-resplendent-lynx-pw.mybluemix.net`. 
9. Abrir la escena de *Unity* contenida en `TC2008B-Reto/TC2008B_Unity/Assets/Reto/Scenes`
10. En caso de ser necesario, ingresar al objecto *Controller* de la escena y cambiar la variable *url* a `http://retotc2008b-resplendent-lynx-pw.mybluemix.net/`
11. En el mismo objecto *Controller*, seleccionar el número de coches que se desea visualizar siendo menor o igual al número de destinos de la ciudad
12. Presionar el botón de *Play* que se contiene en la parte superior del editor de *Unity* una vez que se abra la escena 
13. Observar la ejecución de la simulación y pararlo cuando se desee

## Ejecución del programa para el reto usando una instancia local
1. Abrir la terminal de preferencia
2. Dirigirse al archivo de *Python* a ejecutar dentro del directorio `TC2008B-Reto/TC2008B_Python/reto`
3. Activar el ambiente creado en la instalación usando `conda activate <nombre_de_ambiente>`
4. Ingresar el comando `python api.py`
5. Esperar hasta que la instancia de *Flask* este corriendo completamente
6. Abrir la escena de *Unity* contenida en `TC2008B-Reto/TC2008B_Unity/Assets/Reto/Scenes`
7. En caso de ser necesario, ingresar al objecto *Controller* de la escena y cambiar la variable *url* a `http://localhost:8000/`
8. En el mismo objecto *Controller*, seleccionar el número de coches que se desea visualizar siendo menor o igual al número de destinos de la ciudad
9. Presionar el botón de *Play* que se contiene en la parte superior del editor de *Unity* una vez que se abra la escena 
10. Observar la ejecución de la simulación y pararlo cuando se desee

## Variables de desempeño
- Posición inicial de cada agente
- Destino final de cada agente
- Número de movimientos por agente
- Tiempo utilizado para concluir el modelo