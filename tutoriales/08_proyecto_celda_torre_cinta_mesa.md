# Mini‑proyecto: Célula robotizada Torre → Cinta → Mesa con ROS 2

Este tutorial propone un proyecto para integrar los distintos componentes desarrollados a lo largo del curso para construir una **célula robotizada** basada en ROS 2 y un robot UR3/UR3e.

El sistema permite coger piezas desde una **torre**, depositarlas en una **cinta transportadora**, mover esas piezas por la cinta y, finalmente, recogerlas para dejarlas en una **mesa**.

---

## 1. Arquitectura general del sistema

La arquitectura se basa en una **separación clara de responsabilidades**, que puede verses en la figura inferior:

- *Nodos de Driver*: ejecutan acciones sobre el hardware
- *Interfaces*: definen servicios o mensajes creados para la aplicación
- *Aplicación*: decide qué hacer y cuándo ejecutando una máquina de estados

Con esta arquitectura, conseguimos algunas buenas características para el software planteado: 

- Mantener **drivers independientes de la lógica**
- Usar **servicios** para acciones discretas y rápidas
- Centralizar la secuencia en un único nodo de aplicación
- Nombrar claramente estados y funciones

```text
                ┌────────────────────────┐
                │     ur3_interfaces     │
                │  (srv definitions)     │
                │  ConveyorControl.srv   │
                └──────────▲─────────────┘
                           │
                           │ used by
                           │
┌──────────────────────────┴──────────────────────────┐
│                   UR3_driver                        │
│                                                     │
│  ┌────────────────────┐   ┌──────────────────────┐  │
│  │ ur3_motion_node    │   │ ur3_gripper_service  │  │
│  │  moveJ / moveL     │   │  open / close        │  │
│  └────────────────────┘   └──────────────────────┘  │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │ ur3_conveyor_service                          │  │
│  │ uses ConveyorControl.srv                      │  │
│  └───────────────────────────────────────────────┘  │
└──────────────────────────▲──────────────────────────┘
                           │
                           │ service calls / commands
                           │
                ┌──────────┴─────────────┐
                │    ur3_application     │
                │ cell_controller_node   │
                │  (lógica secuencial)   │
                └────────────────────────┘
```

---

## 2. Rol del nodo de aplicación de control de la celda

El nodo **`cell_controller_node`** es el corazón de la célula. Su responsabilidad es **coordinar la secuencia completa** del proceso.
Se propone implementar la siguiente secuencia: 

1. Mover el robot a la torre y abrir pinza (moveJ)
2. Bajar (moveL)
3. Cerrar la pinza (coger pieza) 
4. Subir (moveL)
5. Mover el robot sobre la cinta (moveJ)
6. Ajustar posición (moveL)
7. Abrir la pinza (dejar pieza) en la cinta
8. Esperar 1 segundo
9. Arrancar la cinta
10. Esperar llegada al final (tiempo o sensor)
11. Parar la cinta
12. Mover el robot al final de la cinta y abrir pinza (moveJ)
13. Mover de manera precisa sobre pieza (moveL)
14. Cerrar la pinza y subir (moveL)
15. Mover el robot a la mesa
16. Abrir la pinza
17. Volver a estado inicial

---

## 3. Pseudocódigo del `cell_controller_node`

Se ofrece el siguiente psudocódigo en Python que implementa de manera muy sencilla una máquina de estados. 
Si, para implementar la secuencua anterior necesita más estados, no dude en añadirlos. 

```python
state = IDLE

while rclpy.ok():
    if state == IDLE:
        state = MOVE_TO_TOWER

    elif state == MOVE_TO_TOWER:
        move_robot_to(tower_pose)
        state = GRAB_PIECE

    elif state == GRAB_PIECE:
        call_gripper(close=True)
        state = MOVE_TO_CONVEYOR

    elif state == MOVE_TO_CONVEYOR:
        move_robot_to(conveyor_pose)
        state = PLACE_ON_CONVEYOR

    elif state == PLACE_ON_CONVEYOR:
        call_gripper(close=False)
        state = WAIT_BEFORE_CONVEYOR

    elif state == WAIT_BEFORE_CONVEYOR:
        sleep(1.0)
        call_conveyor(direction=1)
        state = CONVEYOR_RUNNING

    elif state == CONVEYOR_RUNNING:
        sleep(conveyor_time)
        call_conveyor(direction=0)
        state = PICK_FROM_CONVEYOR

    elif state == PICK_FROM_CONVEYOR:
        move_robot_to(conveyor_end_pose)
        call_gripper(close=True)
        state = MOVE_TO_TABLE

    elif state == MOVE_TO_TABLE:
        move_robot_to(table_pose)
        call_gripper(close=False)
        state = IDLE
```

---

## 4. Implementación del paquete `ur3_application`

Se implementará esta aplicación en un nuevo paquete de ROS2 que tendrá la siguiente estructura: 

```text
ur3_application/
├── package.xml
├── setup.py
└── ur3_application/
    ├── __init__.py
    └── cell_controller_node.py
```
---

