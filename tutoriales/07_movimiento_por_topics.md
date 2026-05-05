# 07 – Movimiento del UR3 mediante topics ROS 2 (moveJ y moveL)

En este tutorial se implementa el **control del movimiento del robot UR3e mediante topics ROS 2**, utilizando internamente la interfaz **`rtde_control`**. El objetivo es usar un mecanismo **simple e intuitivo**, adecuado para primeros prototipos y para comprender las limitaciones de los topics cuando se controla el movimiento de un brazo robótico.

---

## 🎯 Objetivos de aprendizaje

- Enviar movimientos al robot usando **topics ROS 2**
- Diferenciar movimientos **articulares (moveJ)** y **cartesianos (moveL)**
- Implementar **exclusividad**: un solo movimiento activo a la vez
- Rechazar comandos mientras el robot está en movimiento

---

## ⚠️ Advertencia de seguridad

- Usa **velocidades y aceleraciones bajas**
- Mantén el entorno despejado
- Ten siempre acceso al botón de emergencia
- Usa solo el movimiento **cartesianos (moveL)** para movimientos muy pequeños y controlados
---

## 1. Arquitectura del sistema

```text
Nodo publicador  ──▶  /ur3/movej   (tipo de mensaje: sensor_msgs/JointState)
                 └─▶  /ur3/movel   (tipo de mensaje: geometry_msgs/PoseStamped)

Nodo ur3_motion_topics
   └─▶ rtde_control ──▶ Robot UR3
```
---

## 2. Nodo de movimiento por topics

En el paquete creado anterirmente, implemete el nodo que controla los topics en el siguiente : `UR3_driver/ur3_motion_topics.py`

```python
import threading
import rclpy
from rclpy.node import Node

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped

import rtde_control
import rtde_receive

from scipy.spatial.transform import Rotation as R
import numpy as np

class UR3MotionTopics(Node):

    def __init__(self):
        super().__init__('ur3_motion_topics')

        self.declare_parameter('robot_ip', '192.168.56.2')
        self.declare_parameter('speed', 0.2)
        self.declare_parameter('acceleration', 0.2)

        robot_ip = self.get_parameter('robot_ip').value
        self.speed = self.get_parameter('speed').value
        self.accel = self.get_parameter('acceleration').value

        self.rtde_c = rtde_control.RTDEControlInterface(robot_ip)
        self.rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

        # Usado para marcar cuando el robot se está moviemtno y no debe aceptar nuevas órdenes
        self.busy = False
        self.lock = threading.Lock()

        self.create_subscription(JointState, '/ur3/movej', self.movej_cb, 10)
        self.create_subscription(PoseStamped, '/ur3/movel', self.movel_cb, 10)

        self.get_logger().info('Nodo de movimiento por topics iniciado')

    # -------------------------------
    # Callback del movimiento articular
    # MOVEJ
    # espera posiciones en radianes
    # -------------------------------

    def movej_cb(self, msg):
        with self.lock:
            if self.busy:
                self.get_logger().warn('Robot ocupado, moveJ ignorado')
                return
            self.busy = True

        try:
            # lee posiciones angulares
            q = list(msg.position)
            # envia movimiento
            self.rtde_c.moveJ(q, self.speed, self.accel)
        finally:
            self.busy = False

    # -------------------------------
    # Callback del movimiento lineal
    # MOVEL - Para la orientación
    # Si el usuario manda un quaternion (0,0,0,0) → NO es válido → se mantiene la orientación actual.
    # -------------------------------

    def movel_cb(self, msg):
        with self.lock:
            if self.busy:
                self.get_logger().warn('Robot ocupado, moveL ignorado')
                return
            self.busy = True

        try:
            # ---- Lee posición objetivo ----
            p = msg.pose.position

            # ---- Lee orientación actual y la pone como objetivo ----
            tcp_pose = self.rtde_r.getActualTCPPose()          
            quat_input = np.array([tcp_pose.orientation.x, tcp_pose.orientation.y, tcp_pose.orientation.z, tcp_pose.orientation.w])

            # ¿El usuario envió orientación válida?
            if np.allclose(quat_input, np.zeros(4), atol=1e-6):
                # No hay orientación en el mensaje → usar orientación actual del robot
                tcp = self.rtde_r.getActualTCPPose()
                rotvec = np.array([tcp[3], tcp[4], tcp[5]])
            else:
                # Usuario envió orientación → convertir cuaternión → rotvec
                rot = R.from_quat(quat_input)
                rotvec = rot.as_rotvec()

            p = msg.pose.position
            target = [p.x, p.y, p.z, rotvec[0], rotvec[1], rotvec[2] ]

            # envia movimiento
            self.rtde_c.moveL(target, self.speed, self.accel)
        finally:
            self.busy = False


def main():
    rclpy.init()
    node = UR3MotionTopics()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

---

## 3. Registrar el nodo en setup.py

Añadir en `entry_points`:

```python
entry_points={
    'console_scripts': [
        'ur3_state_publisher = UR3_driver.ur3_state_publisher_node:main',
        'ur3_motion_topics = UR3_driver.ur3_motion_topics:main',
        'ur3_gripper_service = UR3_driver.gripper_service:main',
    ],
},

```

---

## 4. Compilación y ejecución

Desde el workspace ROS 2:

```bash
colcon build
source install/setup.bash
```

Ejecutar el nodo:

```bash
ros2 run UR3_driver ur3_motion_topics
```

---

## 5. Pruebas desde terminal
En un terminal, puedes probar a hacer movimientos, procura que la primera vez sean movimientos muy pequeños. Compruena primero en qué posiciones se encuentra el robot para escribir una posición objetivo en el terminal. 

### moveJ
```bash
ros2 topic pub --once /ur3/movej sensor_msgs/msg/JointState "{position: [0, -1.57, 1.57, -1.57, -1.57, 0]}"
```

### moveL
```bash
ros2 topic pub --once /ur3/movel geometry_msgs/msg/PoseStamped "{pose: {position: {x: 0.3, y: 0.0, z: 0.3}}}"
```

---

## 6. Limitaciones del uso de topics
Cuando usamos topics para relizar movimientos, hay una serie de limitaciones por haber elegido topics para hacerlo. 

- No hay feedback de progreso
- No se puede cancelar un movimiento
- La gestión de la exclusividad es manual


---

## 7. Checklist final

- ✅ El robot se mueve con moveJ
- ✅ El robot se mueve con moveL
- ✅ Comandos simultáneos son ignorados
- ✅ El sistema es estable

---

## 8. Ejercicio
- Realice un nodo que use estos topics de la siguiente manera: al lanzarlo se lee la posición actual, y hace moverse al robot 2 cm en el eje X manteniendo la orientación. 

