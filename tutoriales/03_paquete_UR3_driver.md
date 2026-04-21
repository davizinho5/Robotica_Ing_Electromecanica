# 03 – Creación del paquete ROS 2 `UR3_driver`

En este tutorial se crea un **paquete ROS 2 en Python** llamado **`UR3_driver`**, cuyo objetivo es actuar como un informador del estado de los sensores del robot UR3e utilizando la librería **`ur_rtde`**.

El paquete permitirá:

- Leer el estado del robot mediante RTDE
- Publicar el estado en **topics ROS 2 estándar**
- Sentar las bases para el control del robot en los siguientes tutoriales

---

## 🎯 Objetivos de aprendizaje

Al finalizar este tutorial, el estudiante será capaz de:

- Crear un paquete ROS 2 de tipo `ament_python`
- Diseñar la arquitectura básica de un nodo informador del estado del robot
- Publicar información del robot en topics estándar:
  - `sensor_msgs/JointState`
  - `geometry_msgs/PoseStamped`
  - `geometry_msgs/WrenchStamped`
- Integrar `ur_rtde` dentro de nodos ROS 2

Tenga en cuenta que ROS2 tiene muchas más mensajes estándar ya creados. Si tiene interés, puede consultar en los siguientes enlaces los mensajes que hay en las librerías:  [sensor_msgs](https://docs.ros.org/en/humble/p/sensor_msgs/__message_definitions.html) y [geometry_msgs](https://docs.ros.org/en/humble/p/geometry_msgs/__message_definitions.html).

---

## 1. Arquitectura del paquete UR3_driver

La arquitectura propuesta es la siguiente:

```text
UR3_driver (paquete ROS 2)
│
├── ur3_state_publisher_node.py
│     ├── RTDEReceiveInterface
│     ├── /joint_states        (JointState)
│     ├── /ur3/tcp_pose        (PoseStamped)
│     └── /ur3/tcp_force       (WrenchStamped)
└── 
```

- El nodo **solo lee el estado** para hacerlo público en ROS2 (no mueve el robot)
- El nodo publica continuamente el estado real del robot

---

## 2. Creación del paquete ROS 2

Abra un terminal en la carpeta donde esté su espacio de trabajo de ROS2, dentro de la carpeta de código (`ros2_ws/src`):

```bash
ros2 pkg create UR3_driver   --build-type ament_python   --dependencies rclpy sensor_msgs geometry_msgs
```

Estructura inicial generada:

```text
UR3_driver/
├── package.xml
├── setup.cfg
├── setup.py
├── resource/UR3_driver
├── test/
└── UR3_driver/
    └── __init__.py
```

---

## 3. Diseño del nodo `ur3_state_publisher`

El nodo propuesto realizar debe conectarse al robot usando la interfaz `rtde_receive` y después, cíclicamente: 

- Lee periódicamente el estado del robot
- Publica los datos en topics ROS estándar

### Topics publicados

| Topic | Tipo | Descripción |
|------|------|------------|
| `/joint_states` | sensor_msgs/JointState | Posición articular |
| `/ur3/tcp_pose` | geometry_msgs/PoseStamped | Pose del TCP |
| `/ur3/tcp_force` | sensor_msgs/WrenchStamped | Fuerza/par en TCP |

---

## 4. Implementación del nodo

Genere en la carpeta que se indica el siguiente archivo: 

Archivo: `UR3_driver/ur3_state_publisher_node.py`

```python
import rclpy
from rclpy.node import Node

from scipy.spatial.transform import Rotation as R

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import WrenchStamped

import rtde_receive

class UR3StatePublisher(Node):

    def __init__(self):
        super().__init__('ur3_state_publisher')

        self.declare_parameter('robot_ip', '192.168.56.2')
        robot_ip = self.get_parameter('robot_ip').value

        self.rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)

        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.pose_pub = self.create_publisher(PoseStamped, '/tcp_pose', 10)
        self.force_pub = self.create_publisher(WrenchStamped, '/tcp_force', 10)

        self.timer = self.create_timer(0.02, self.update)  # 50 Hz

        self.get_logger().info('UR3 state publisher iniciado')

    def update(self):
        # Joint positions
        q = self.rtde_r.getActualQ()

        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = [
            'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint',
            'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint'
        ]
        js.position = q
        self.joint_pub.publish(js)

        # TCP pose
        tcp = self.rtde_r.getActualTCPPose()

        pose = PoseStamped()
        pose.header.stamp = js.header.stamp
        pose.header.frame_id = 'base'
	# Posición
        pose.pose.position.x = tcp[0]
        pose.pose.position.y = tcp[1]
        pose.pose.position.z = tcp[2]
        
        # Orientación (rotvec → quaternion)
        rot = R.from_rotvec([tcp[3], tcp[4], tcp[5]])
        q = rot.as_quat()  # devuelve [x, y, z, w]
        pose.pose.orientation.x = q[0]
        pose.pose.orientation.y = q[1]
        pose.pose.orientation.z = q[2]
        pose.pose.orientation.w = q[3]

        self.pose_pub.publish(pose)

        # TCP force
        wrench = self.rtde_r.getActualTCPForce()

        fp = WrenchStamped()
        fp.header.stamp = js.header.stamp
        fp.wrench.force.x = wrench[0]
        fp.wrench.force.y = wrench[1]
        fp.wrench.force.z = wrench[2]                
        fp.wrench.torque.x = wrench[3]
        fp.wrench.torque.y = wrench[4]        
        fp.wrench.torque.z = wrench[5]        
        self.force_pub.publish(fp)


def main():
    rclpy.init()
    node = UR3StatePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

---

## 5. Registrar el nodo en setup.py

Ahora, vamos a registrar el nodo en el archivo `setup.py` de manera que las herramientas de compilación y lanzamiento de ROS2 encuentre en nodo:

```python
entry_points={
    'console_scripts': [
        'ur3_state_publisher = UR3_driver.ur3_state_publisher_node:main',
    ],
},
```

---

## 6. Compilación y ejecución

Desde el workspace:

```bash
colcon build
source install/setup.bash
```

Ejecutar el nodo:

```bash
ros2 run UR3_driver ur3_state_publisher
```

Comprobar topics:

```bash
ros2 topic list
ros2 topic echo /joint_states
```
> ![📷 Resultado del lanzamiento del state_publisher: ](/../main/imagenes/run_state_publisher.png) 

> ![📷 Resultado del topic list: ](/../main/imagenes/ros_topic_list.png)
---

## 7. Ejercicios propuestos

- Pruebe a, mientras está lanzado `ros2 topic echo /joint_states` en un temrinal, lanzar en otro el ejemplo del tutorial anterior que realiza un pequeño movimiento de la muñeca. Debería de que cómo cambia el valor de ese motor.

- Revise las opciones de la [interfaz `rtde_receive`](https://sdurobotics.gitlab.io/ur_rtde/api/api.html#_CPPv4N7ur_rtde20RTDEReceiveInterfaceE). Aprenda a leer la velocidad y la corriente de los motores. Además, revise la definición del mensaje `sensor_msgs/JointState` y mire cómo puede añadir esa información al publicador. 

---

## 8. Checklist final

- ✅ Paquete UR3_driver creado
- ✅ Nodo compila correctamente
- ✅ Topics estándar publicados


---

## 9. Conclusión

Este paquete constituye un **un informador del estado de los sensores del robot UR3e**, mínimo pero funcional, en ROS 2.

En el [siguiente tutorial](/tutoriales/04_visualizacion_RVIZ.md) se utilizará este nodo para **visualizar el robot en RViz**.
