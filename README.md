# TC2008B-Reto

Carpeta de *Python* contiene carpetas para actividad integradora y reto final

Carpeta de *Assets* de *Unity* contiene carpetas para actividad integradora y reto final

Equipo:
- Diego Mejía - A01024228
- Enrique Mondelli - A01379363
- Mateo González Cosío - A01023938

## Fortalezas y áreas de oportunidad

- **Mateo:** Mi principal fortaleza es la programación en Python ya que es el lenguaje con el que mas familiarizado estoy. Al igual me considero una persona bastante flexible, lo que me permite adaptarme facilmente a diferentes estilos de trabajo y aprender nuevas herramientas con facilidad. Otra fortaleza que se me hace relevante es la comunicación efectiva que tengo con los integrantes del equipo. Dentro de mis areas de oportunidad se encuentra mejorar mis habilidades con Unity y C#, ya que aunque ya los he utilizado previamente, no tengo la experiencia necesaria para lo que nos pide el proyecto. 

- **Enrique:** En mi opinion, mis fortalezas son la programacion en python, ya que es el lenguaje que mas tiempo he usado, ademas me considero una persona flexible a estilos de trabajo por lo cual me hace bueno al colaborar con integrantes de mi equipo. Un area de oportunidad es mi nivel de conocimiento de C# especificamente en Unity ya que no tengo mucha experiencia con esta herramienta. Otra area de oportunidad es el manejo de aplicaciones en la nube porque no he tenido muchas oportunidades para deployear cosas a la nube.

- **Diego:** Considero que mis principales fortalezas son la programación tanto en Python como en C#. A pesar de que no estoy a un nivel experto de ambos de estos lenguajes, creo que tengo la capacidad de ser flexible y adaptarme a nuevos conocimientos sobre estos lenguajes, ya sea algo totalmente nuevo o una adaptación sobre lo que ya conozco. Junto con esto, pienso tengo la habilidad de trabajar en equipo y en parte ser un líder cuando sea necesario. A pesar de esto, la principal área de oportunidad que tengo es que tiendo a invertir mucho tiempo fuera de clase en trabajos y proyectos, lo cual lleva a afectar el tiempo libre que tengo durante el día, además de que resulta en poca energía para trabajar en otras tareas. 

## Expectativas

- **Mateo:**  Mi mayor expectativa de este bloque es conocer a fondo las base de los temas que se tocaran durante el transcurso del curso del bloque. Con esto poder obtener una buena base de conocimiento que me permita adentrarme a cada area de estudio con mas facilidad. Al igual, una de mis gran expectativas es poder llevar el proyecto de una manera ordenada, lo cual nos permitira llegar al objetivo final sin problema alguno. Digo esto, ya que en bloques pasados hemos tenido problema siguiendo una estructura de trabajo.

- **Enrique:** En el transcurso del bloque espero poder desarrollar mis conocimientos en el area de Inteligencia Artificial, ya que es una de las areas que considero de mayor interes. Tambien espero aprender las bases sobre graficas computaiconales para poder generar una visualizacion adecuada del modelo multiagentes que se desarrollara. Ademas de esto espero poder aprender a usar herramientas como la nube para poder hostear la aplicacion creada para la solucion del reto, pero tambien para futuros proyectos, ya sean personales y professionales, que requieran de este tipo de servicio.

- **Diego:** Durante el lapso de tiempo del bloque en el que se desarrolla el proyecto, me gustaría reforzar mis habilidades de programación tanto en Python como en C# de Unity. En adición a esto, me gustaría llevarme un mayor aprendizaje sobre el desarrollo de inteligencias artificiales, sus acciones metódicas y sus implicaciones que tienen en la sociedad de la actualidad. Como último punto, espero aprender sobre los procesos que se llevan a cabo para la realización de gráficas computacionales, en adición a sus propiedades y como son utilizadas en ejemplos de la vida real. 

## Expectativas y compromisos del equipo

**Lista de logros:**
- Finalizar el proyecto en su totalidad dentro del tiempo limite.
- Aprender sobre las implicaciones de las interacciones de los agentes reactivos.
- Lograr que nuestro agente se comporte de la manera deseada.
- Reforzar nuestras habilidades en ambos lenguajes de programación.
- Complementar el proyecto de manera visual a través de Unity.
- Impulsar nuestra capacidad de pensamiento critico dentro del desarrollo del proyecto.
- Lograr reforzar nuestras áreas de oportunidad definidas por cada integrante. 
- Destacar los elementos visuales del proyecto concluido.

**Compromisos:**
- Atender a todas las clases remotas.
- Implementar una estructura de trabajo.
- Definir herramientas a ser utlizadas.
- Atender asesorías cuando sea necesario.
- Tener una documentación consistente a lo largo del desarrollo.
- Implementar código que sea sencillo de comprender.
- Si es que el tiempo nos lo permite, llevar a cabo mejoras a los diversos componentes del proyecto.

## Descripción del reto

Durante las últimas décadas, ha existido una tendencia alarmante de un incremento en el uso de automóviles en México. Los Kilómetros-Auto Recorridos (VKT por sus siglas en Inglés) se han triplicado, de 106 millones en 1990, a 339 millones en 2010. Ésto se correlaciona simultáneamente con un incremento en los impactos negativos asociados a los autos, como el smog, accidentes, enfermedades y congestión vehicular.

Para que México pueda estar entre las economías más grandes del mundo, es necesario mejorar la movilidad en sus ciudades, lo que es crítico para las actividades económicas y la calidad de vida de millones de personas.

El principal propósito del reto consiste en proponer una solución al problema de movilidad urbana en México, mediante un enfoque que reduzca la contgestión vehicular.

Para esto, es necesario implementar una simulación de sistemas multiagentes de un cruce vial a través de agentes reactivos representados por automóviles que tomen decisiones dependiendo del su respectivo ambiente. Dichos agentes tienen la posibilidad de seguir su trayectoria definida o detenerse de acuerdo a la situación, en adición a como se definan sus comportamientos.

## Identificación de agentes involucrados

- **Principal agente:** Automóvil 
- **Descripción:** A pesar de que en ejemplos pasados se han hecho uso de diversos agentes que solo tienen la funcionalidad de existir en el modelo con ciertas propiedades, el único agente que realiza las interacciones y decisiones reactivas es el agente que representa un automóvil.
- **Relaciones**: Van a existir varias instancias de este agente en el modelo. Estas instancias se van a tener que comunicar entre ellas para prevenir colisiones, por lo cual van a contar con un sistema de luces intermitentes para comunicar sus futuros pasos a vehiculos cercanos. Además de esto, van a tener acciones reactivas a su entorno, por ejemplo, detenerse si hay un automovil entfrente, detenerse en semaforos con luz roja, avanzar cuando el semaforo cambia a luz verde.
- **Variables de desempeño:**
  - si llega a su destino
  - número de colisiones
  - tiempo en llegar al destino
  - velocidad promedio

## Plan de trabajo

El equipo de trabajo estableció que el plan de trabajo hará uso de la metodología AGILE. Dicha metodología tiene la fundación de realizar ciclos en disntintas etapas del proyecto hasta que el equipo de trabajo decida que el producto este listo para su lanzamieto y posible publicación.

Las etapas fuera del ciclo son la planeación y el lanzamiento del proyecto, y por dentro de los ciclos se encuentran; el diseño, desarrollo, pruebas, despliegue y revisión.

### Actividades 

- [x] **Configuración de repositorio**
  - **Descripción:** crear el repositorio con todas las carpetas y archivos necesarios
  - **Lapso de tiempo**: 11/11/2021 - 11/11/2021
  - **Fecha esperada:** 11/11/2021
  - **Responsable/s:** Equipo de trabajo
  - **Intervalo de esfuerzo estimado:** Bajo

- [x] **Definición de modelo**
  - **Descripción:** establecer el modelo del sistema multiagente a implementar
  - **Lapso de tiempo**: 12/11/2021 - 25/11/2021
  - **Fecha esperada:** 25/11/2021
  - **Responsable/s:** Equipo de trabajo
  - **Intervalo de esfuerzo estimado:** Intermedio

- [x] **Desarrollo de sistema multiagente**
  - **Descripción:** construcción del modelo con los respectivos agentes reactivos
  - **Lapso de tiempo**: 17/11/2021 - 01/12/2021
  - **Fecha esperada:** 01/12/2021
  - **Responsable/s:** Diego, Enrique
  - **Intervalo de esfuerzo estimado:** Alto

- [x] **Implementación de la nube**
  - **Descripción:** Conexión del modelo hacia una liga en la nube
  - **Lapso de tiempo**: 17/11/2021 - 01/12/2021
  - **Fecha esperada:** 01/12/2021
  - **Responsable/s:** Enrique, Mateo
  - **Intervalo de esfuerzo estimado:** Intermedio

- [x] **Visualización de Unity**
  - **Descripción:** Aplicar gráficas computacionales para la visualización de la simulación
  - **Lapso de tiempo**: 22/11/2021 - 01/12/2021
  - **Fecha esperada:** 01/12/2021
  - **Responsable/s:** Diego, Mateo
  - **Intervalo de esfuerzo estimado:** Alto

## Aprendizajes adquiridos

### Sistemas multiagentes

- Nueva perspectiva sobre la inteligencia artificial y sus implicaciones en la vida real
- Diferentes tipos sistemas inteligentes que pueden actuar o pensar como humanos o racionalmente 
- Racionalidad y sus distintats características en relación a la inteligencia artificial
- Distintas arquitecturas de agentes y sus distintas metodologías
- Diferentes objetivos y caminos utilizados por agentes que impactan su ambiente
- Implementación de modelo multiagentes a través de Python

### Gráficas computacionales

- Transformaciones de figuras 3D a través de sus vectores
- Matemáticas involucradas en las transformaciones de figuras
- Modelación de figuras 3D a través de herramientas computacionales
- Uso de Unity y C# para la modelación y movimiento de figuras 3D
- Iluminación en un ambiente 3D y sus interacciones con distintas superficies
- Conexión del sistema multiagente haciendo uso de gráficas
- Traslación y rotación de modelos 3D