# Curso de Control de Robots UR3 con ROS 2 y Python (ur_rtde)

Este repositorio contiene un conjunto de tutoriales diseñados para aprender a controlar un robot **UR3 / UR3e** desde un PC externo utilizando **ROS 2 Humble (Ubuntu 22.04)** y el paquete Python [**ur_rtde**](https://pypi.org/project/ur-rtde/).  

El objetivo es que el estudiante aprenda algunas de las funcionalidades principales presentadas por la librería **ur_rtde**, que usa el protocolo de comunicación en tiempo real llamado [**RTDE**](https://www.universal-robots.com/developer/communication-protocol/rtde/) e implementado en las controladoras de los robots de Universal Robots. , el desarrollo de nodos ROS 2, la visualización del robot y el control básico de una pinza.

---

## 🎯 ¿Qué vas a aprender?

- Configurar un PC con Ubuntu 22.04 y ROS 2 Humble para controlar externamente un robot UR3.  
- Configurar la caja controladora del robot (red, URCap, Remote Control, RTDE).  
- Probar las interfaces principales de la librería `ur_rtde` usando Python:
  - **rtde_receive** → lectura del estado del robot, información de sensores y de la controladora
  - **rtde_control** → configuración y envío de movimientos al robot  
  - **rtde_io** → control de entradas y salidas analógicas y digitales  
- Crear paquete ROS 2 con algunas funcionalidades de interés:
  - Publicar el estado del robot en topics estándar  
  - Controlar la pinza vía un servicio de ROS2
  - Otros...
- Visualizar el estado del robot en **RViz2** con modelos URDF.  
- Comprender las bases de una arquitectura modular para robots UR + ROS 2.

---

## 🧰 Hardware y Software necesario

- ✅ Un robot **UR3e** con:
- ✅ Caja de control con firmware compatible con RTDE
- ✅ Pinza eléctrica simple conectada a la herramienta (I/O Tool) de la marca Zimmer
- ✅ Cable Ethernet directo o red local estable (se usará de manera directa en este laboratorio)
- ✅ Extensión URCap *ExternalControl* instalada en el robot (solo e-Series)
  
- ✅ Un PC con:
  - **Ubuntu 22.04 LTS**
  - **ROS 2 Humble**
  - Python 3.10+
  - Paquete de Python `ur_rtde` (instalación vía pip):
  ```bash
  pip3 install ur_rtde

---
  
## 📚 Índice del curso

Este curso está organizado como una secuencia progresiva de tutoriales prácticos,
centrados en el control de un robot **UR3 / UR3e** mediante **ROS 2 Humble** y **Python**.

Cada tutorial se encuentra en la carpeta tutoriales.

---

### 🔹 Bloque 1 – Preparación y comunicación con el robot

1. [**Configuración del PC y del robot**](https://github.com/davizinho5/Robotica_Ing_Electromecanica/blob/main/tutoriales/01_configuracion_pc_robot.md)
   Configuración de red, RTDE, Remote Control y primer test de comunicación.

2. [**Tests del paquete `ur_rtde`**](https://github.com/davizinho5/Robotica_Ing_Electromecanica/blob/main/tutoriales/02_tests_ur_rtde.md)
   Pruebas independientes de `rtde_receive`, `rtde_control` y `rtde_io`.

---

