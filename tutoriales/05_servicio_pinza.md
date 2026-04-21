# 05 – Servicio ROS 2 para control de la pinza del UR3

En este tutorial se implementa un **servicio ROS 2** que permite **abrir y cerrar una pinza eléctrica** conectada a la **salida digital de la herramienta del UR3**, utilizando la librería **`ur_rtde`**.

El objetivo es introducir el uso de **servicios ROS 2** para control discreto de actuadores, siguiendo un patrónde clinte/servidor que permitar hacer una petición de apertura/cierre.

---

## 🎯 Objetivos de aprendizaje

Al finalizar este tutorial, el estudiante será capaz de:

- Controlar salidas digitales del UR3 mediante `ur_rtde`
- Implementar un **servicio ROS 2 tipo Booleano**
- Integrar el control de una pinza en la arquitectura ROS 2 existente

---

## ⚠️ Consideraciones de hardware

Se asume la siguiente configuración:

- Pinza eléctrica conectada a la **herramienta del UR3**
- Uso de la **salida digital TOOL DO0** para cerrar
- Uso de la **salida digital TOOL DO1** para abrir
    
Convención utilizada para la petición del servicio:

| Valor | Acción |
|------|--------|
| `0 / False` | Abrir pinza |
| `1 / True`  | Cerrar pinza |

> 📌 Ajusta el número de pin de salida de la herramienta si tu robot está configurado de otra manera.

---

## 1. ¿Por qué usar un servicio ROS 2?

Un **servicio** es adecuado cuando:

- Se desea una acción **discreta**
- Se espera una **respuesta inmediata**
- No es necesario feedback continuo

Ejemplos típicos:
- Abrir / cerrar una pinza
- Activar una bomba de vacío
- Resetear un sistema

---

## 2. Arquitectura del sistema

```text
Cliente ROS 2
   │
   │  (SetBool)
   ▼
Servicio /ur3/gripper
   │
   │  ur_rtde
   ▼
Salida digital TOOL DO0  ──► Pinza
```
---

## 3. Tipo de servicio utilizado

Se utilizará el servicio estándar:

```
std_srvs/srv/SetBool
```

Estructura:

```text
bool data      # True = cerrar, False = abrir
---
bool success
string message
```

---

## 4. Implementación del nodo de servicio

En el mismo paquete que se generó anteriormente, en la carpeta de código, genere un nuevo nodo que abre y cierra la pinza según se le indique: `UR3_driver/gripper_service.py`

```python
import rclpy
from rclpy.node import Node

from std_srvs.srv import SetBool
import rtde_io

import time

class GripperService(Node):

    def __init__(self):
        super().__init__('ur3_gripper_service')

        self.declare_parameter('robot_ip', '192.168.56.2')
        self.declare_parameter('tool_digital_pin', 0)

        robot_ip = self.get_parameter('robot_ip').value
        self.rtde_io = rtde_io.RTDEIOInterface(robot_ip)

        self.srv = self.create_service(
            SetBool,
            '/ur3/gripper',
            self.handle_gripper
        )

        self.get_logger().info('Servicio de pinza UR3 listo')

    def handle_gripper(self, request, response):
        try:
            # cerrar
            if request.data:
                self.rtde_io.setToolDigitalOut(1, True)
                time.sleep(0.1)
                self.rtde_io.setToolDigitalOut(1, False)
                response.message = 'Pinza cerrada'
            else: # abrir
                self.rtde_io.setToolDigitalOut(0, True)
                time.sleep(0.1)
                self.rtde_io.setToolDigitalOut(0, False)
                response.message = 'Pinza abierta'

            response.success = True

        except Exception as e:
            response.success = False
            response.message = f'Error: {e}'

        return response


def main():
    rclpy.init()
    node = GripperService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

---

## 5. Registrar el nodo en `setup.py`

Añadir en `entry_points`:

```python
entry_points={
    'console_scripts': [
        'ur3_gripper_service = UR3_driver.gripper_service:main',
    ],
},
```

---

## 6. Compilación y ejecución

Desde el workspace ROS 2:

```bash
colcon build
source install/setup.bash
```

Ejecutar el servicio:

```bash
ros2 run UR3_driver ur3_gripper_service
```

---

## 7. Pruebas del servicio

Abrir la pinza:

```bash
ros2 service call /ur3/gripper std_srvs/srv/SetBool "{data: false}" 
```

Cerrar la pinza:

```bash
ros2 service call /ur3/gripper std_srvs/srv/SetBool "{data: true}" 
```

Resultado esperado:
- La pinza se abre o se cierra
- El servicio responde con `success: true`

---

## 8. Checklist final

- ✅ Servicio ROS 2 creado
- ✅ Salida digital TOOL controlada
- ✅ Pinza responde correctamente
- ✅ Servicio probado desde terminal

---

➡️ En el próximo tutorial se crea un nuevo servicio para controlar la cinta transportadora: [Nuevo servicio.](/tutoriales/06_crear_un_nuevo_servicio.md)
