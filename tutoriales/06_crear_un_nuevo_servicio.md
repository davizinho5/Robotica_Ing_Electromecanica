# 06 – Crear un nuevo servicio en ROS 2

En este tutorial se explica **paso a paso cómo crear un servicio ROS 2 propio**, definiendo su interfaz y utilizándolo desde un nodo Python.

Para ello, se va a generar un paquete que albergue esta nueva interfaz, y donde se recomienda alojar las interfaces que necesite generar alrededor del proyecto del UR3. Es común, en un proyecto mediano, tener un paquete con las interfaces que se han generado, es la **arquitectura recomendada** en proyectos ROS 2 profesionales.

El paquete de interfaces será independiente de la lógica y del hardware, lo que permite:

- Reutilizar interfaces en varios paquetes
- Mantener el código limpio y modular
- Escalar el proyecto fácilmente

El servicio se declarará **dentro del paquete `UR3_driver`**, siguiendo las buenas prácticas de ROS 2, y servirá como base para controlar dispositivos discretos como:
- pinzas,
- cintas transportadoras,
- actuadores on/off,
- sistemas auxiliares.

---

## 🎯 Objetivos de aprendizaje

Al finalizar este tutorial, el estudiante será capaz de:

- Comprender por qué separar interfaces y lógica en ROS 2
- Crear un paquete ROS 2 de tipo **ament_cmake** para interfaces
- Definir un servicio propio (`.srv`)
- Compilar y generar correctamente las interfaces
- Preparar el paquete para albergar futuras interfaces

---


## 1. Arquitectura propuesta

La estructura recomendada es la siguiente:

```text
ros2_ws/src/
├── ur3_interfaces/        # Paquete SOLO de interfaces
│   ├── package.xml
│   ├── CMakeLists.txt
│   └── srv/
│       └── ConveyorControl.srv
│
└── UR3_driver/            # Paquete de lógica/hardware
    └── ...
```

El paquete `ur3_interfaces` **no contendrá nodos**, únicamente definiciones de:
- servicios (`.srv`)
- mensajes (`.msg`) en el futuro
- acciones (`.action`) en el futuro

---

## 2. Crear el paquete de interfaces

Desde la carpeta `src` del workspace:

```bash
cd ~/ros2_ws/src
ros2 pkg create ur3_interfaces --build-type ament_cmake
```

Esto crea la estructura básica del paquete. Una vez creado, el paquete `ur3_interfaces` debe organizarse así:

```text
ur3_interfaces/
├── package.xml
├── CMakeLists.txt
├── srv/
│   └── ConveyorControl.srv
└── (msg/, action/ en el futuro)
```

---

## 3. Definir el servicio de la cinta transportadora

Vamos a creal el archivo que contiene la definición de la petición y la respuesta. 
Primero se crea la carpeta `srv`.

```bash
mkdir ur3_interfaces/srv
```

Esta carpeta contendrá **todas las definiciones de servicios del proyecto**.

Después se gerera el archivo `ConveyorControl.srv` dentro de la carpeta `srv`, siendo su contenido: 

```text
# Dirección del movimiento de la cinta
#  1  -> adelante
# -1  -> atrás
#  0  -> parada
int8 direction
---
bool success
string message
```

En la parte superior de las tres lineas horizontales están los datos que se deben enviar en la petición, mientras que en la parte inferior están los datos que forman parte de la respuesta.


### Semántica del servicio

- `direction = 1`  → mover la cinta hacia adelante
- `direction = -1` → mover la cinta hacia atrás
- `direction = 0`  → parar la cinta

---

## 4. Modificar `package.xml`

Edita el archivo `ur3_interfaces/package.xml` para que incluya:

```xml
<build_depend>rosidl_default_generators</build_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
```

Y añade antes del cierre del paquete:

```xml
<member_of_group>rosidl_interface_packages</member_of_group>
```

Esto indica a ROS 2 que este paquete genera interfaces para topics o servicios.

---

## 5. Modificar `CMakeLists.txt`

En este fichero, incluye, después de la linea 9: `find_package(ament_cmake REQUIRED)`:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/ConveyorControl.srv"
)
```

Además, al final del archivo `CMakeLists.txt` deben aparecer las 2 siguientes lineas: 

```cmake
ament_export_dependencies(rosidl_default_runtime)
ament_package()
```

Este archivo puede ampliarse fácilmente cuando se añadan más servicios o mensajes.

---

## 6. Compilar y verificar el paquete de interfaces

Desde la raíz del workspace, la sigueinte linea compila solo el paquete de las interfaces:

```bash
colcon build --packages-select ur3_interfaces
source install/setup.bash
```

Comprueba que ROS 2 reconoce el nuevo servicio:

```bash
ros2 interface show ur3_interfaces/srv/ConveyorControl
```

Si la definición aparece correctamente, el paquete está listo.

---

## 8. Uso del paquete en otros nodos

A partir de este punto, cualquier otro paquete (por ejemplo `UR3_driver`) puede:

- Añadir una dependencia a `ur3_interfaces`. Esto se hace modificando el archivo `package.xm` añadiendo la linea:

```text
<depend>ur3_interfaces</depend>
```
  
- Importar el servicio en Python o C++. En el caso de Python, se importa añadiendo la linea:
```python
from ur3_interfaces.srv import ConveyorControl
```

## 9. Ejercicios propuestos
- Dentro del paquete `UR3_driver`, genere un nodo encargado de mover la cinta tranportadora. Recuerde que la cinta se mueve en 2 direcciones. Debe utilizar el nuevo servicio que acaba de crear.
  
- Haga otro nodo de ROS2 2 que active la cinta cuando hay una nueva pieza situzada en ella (leyendo el sensor correspondiente), y la pare cuando el objeto que transporte llegue al final (usando el sensor de la cinta).

Cuando haya lanzado el nodo que controla la cinta, debe de poder probar el servicio con una llamada de este tipo: 

```bash
ros2 service call /ur3/conveyor ur3_interfaces/srv/ConveyorControl "{direction: 1}"
```

---

## 10. Conclusión

Separar las interfaces en un paquete dedicado es una **práctica profesional** en ROS 2.

Este enfoque facilita:
- el mantenimiento del código
- la reutilización
- la escalabilidad del sistema

El paquete `ur3_interfaces` servirá como base para añadir, en el futuro:
- nuevos servicios
- mensajes personalizados
- acciones ROS 2

---

