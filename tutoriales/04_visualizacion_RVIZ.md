# 04 – Visualización del robot UR3 en RViz2 (URDF y TF en ROS 2)

En este tutorial se explica cómo **visualizar el estado del robot UR3e en RViz**, integrando correctamente:

- El **modelo del robot (URDF/Xacro)**
- El **árbol de transformaciones (TF)**
- Los **datos de articulaciones** publicados desde ROS 2

El objetivo es que el estudiante vea el robot **moverse en RViz de forma coherente con el robot real**, aunque en este tutorial **no se controlará el movimiento**.

---

## 🎯 Objetivos de aprendizaje

Al finalizar este tutorial, el estudiante será capaz de:

- Entender el papel del URDF en ROS 2
- Comprender qué es TF y cómo se construye el árbol de frames
- Integrar `robot_state_publisher` con datos reales del UR3
- Visualizar el robot en RViz2 con sus mallas 3D

---

## 1. Conceptos clave: URDF, Joint States y TF

### 1.1 URDF (Unified Robot Description Format)

**RViz** es una herramienta de visualización de robots y de datos de sensores. Es una herramienta muy útil para visualizar el estado de tu robot y ver si los datos obtenidos por algunos sensores tienen sentido. De forma sencilla se pueden representar modelos 3D hechos con mallas, así como diversos tipos de sensores para los cuales tiene previsualizaciones preparadas. 

---

### 1.2 Joint States

El estado articular del robot, según se ha hecho en el tutorial anterior, se publica en el topic:

```
/joint_states   (sensor_msgs/JointState)
```
Este mensaje contiene:
- Nombre de las articulaciones
- Posición (rad)
- Velocidad (opcional)

---

### 1.3 TF (Transformations)


**TF** es el sistema de ROS 2 que **gestiona las transformaciones entre los distintos sistemas de coordenadas (frames)** de un robot. Permite saber, en cualquier instante:

- dónde está cada parte del robot,
- cómo se orienta,
- y cómo se relacionan sus frames entre sí (por ejemplo: base_link → wrist_3_link → tool0).

TF no mueve nada: solo mantiene y actualiza el árbol de transformaciones para que otros nodos puedan usarlo (RViz, planificadores, controladores…).


Para un brazo robótico UR3e es común tener la siguiente lista de eslabones:

```text
base_link
 └── shoulder_link
     └── upper_arm_link
         └── forearm_link
             └── wrist_1_link
                 └── wrist_2_link
                     └── wrist_3_link
                         └── tool0
```

TF **se calcula automáticamente** a partir de la descripción del robot dada en el `URDF` y lainformación que se publica en el topic `/joint_states`.

---

## 2. Paquetes necesarios

Instalar los paquetes de descripción `URDF` del robot UR:

```bash
sudo apt install ros-humble-ur-description
```

Este paquete incluye:
- URDF/Xacro del UR3
- Mallas 3D oficiales

---

## 3. robot_state_publisher

El nodo `robot_state_publisher` se encarga de leer la estructura inicial estática del robot y, en un bucle, escuchar:

- Escucha el topic `/joint_states`
- Publica la posición de los sistemas de referencia usando TF (`/tf` y `/tf_static`)

---

## 4. URDF

**URDF** (Unified Robot Description Format) es un formato en XML que describe la estructura física (una la descripción estática de su geometría y conexiones) de un robot a través de un listado de sus:
- eslabones (links),
- articulaciones (joints)
- dimensiones
- propiedades visuales (mallas o polígonos sencillos)
- y de colisión (mallas o polígonos sencillos). Las propiedades de colisición no tiene por qué ser las mismas que las visuales.

Para que se pueda reutilizar la descripción básica de un robor y parametrizarla (dado que todos los brazos de UR son parecidos), el URDF de un robot UR3e se define mediante **Xacro**, un archivo con macros XML utilizado en ROS para simplificar la creación de archivos URDF.

---

## 5. Integración con el nodo UR3_driver

El nodo creado en el tutorial 03 publica el topic:

- `/joint_states`

Este topic contiene la información suficiente para que `robot_state_publisher` genere todo el árbol TF.

Arquitectura completa:

```text
UR3_state  --->  /joint_states  --->  robot_state_publisher  --->  TF
```

---

## 6. Lanzar la visualización del robot

Para lanzar la visualización del robot en el programa que ROS2 usa para esto, se deben lanzar muchos nodos, cada uno en un temrinal. 
En el primer terminal, ejecute los 2 siguiente comandos, cada uno de ellos: 
- Genera la descripción URDF del robot UR3e a través del XACRO
- Carga la descripción URDF del robot UR3e recién generada
- 
```
ros2 run xacro xacro /opt/ros/humble/share/ur_description/urdf/ur.urdf.xacro name:=ur ur_type:=ur3e > /tmp/ur3.urdf
ros2 run robot_state_publisher robot_state_publisher /tmp/ur3.urdf
```

En otro terminal, lance el un nodo `robot_state_publisher`, que ya está hecho en ROS2, que publica el TF y TF_static, usado para colocar los modelos 3D del robot en el mundo. 

```
ros2 run robot_state_publisher robot_state_publisher /tmp/ur3.urdf
```

En otro terminal, lance el nodo `ur3_state_publisher`que realizó anteriormente y que publica la información de la posición de los motores del robot.

[ros2 run UR3_driver ur3_state_publisher]: # 

Por último, lance el programa visualizador de ROS2, Rviz2, y cargue la configuración que permite ver el robot: 

```bash
rviz2 -d /opt/ros/humble/share/ur_description/rviz/view_ur.rviz
```

La vista del visualizador debe ser parecida a esta. 

> ![📷](/../main/imagenes/rviz2_ur3.png) 

---

## 7. Comprobaciones útiles

- Pruebe, con el visualizador abierto, a lanzar en otro terminal el ejemplo del tutorial anterior que realiza un pequeño movimiento de la muñeca. Debería de ver se mueve en el visualizador.

Si, en ROS2, quiere listar el arbol de transformaciones geométricas que define su robot, el siguiente comando lo analiza, lo muestra en el terminal, y genera un PDF en el que vienen indicadas las tranformaciones. 

```bash
ros2 run tf2_tools view_frames
```

Además, ROS2 tiene una herramienta gráfica que permite visualizar los nodos (circulos) y los topics (cajas) que se han lanzado en su ordenador. Esta herramienta se lanza desde el temrinal: 

```bash
rqt_graph
```

---
## 8. Checklist final

- ✅ URDF cargado correctamente
- ✅ TF generado automáticamente
- ✅ Robot visible en RViz2

---

## 9. Conclusión

En este tutorial se ha integrado por primera vez el **robot real con su representación virtual**, utilizando los mecanismos estándar de ROS 2. Quizá este visualizador no le sea útil ahora, pero es un estándar muy interesante para hacer representaciones 3D de los robots y sus sensores.

En el [siguiente tutorial](/tutoriales/05_servicio_pinza.md) se añadirá **interacción**, comenzando por el control de la pinza mediante servicios.

---


