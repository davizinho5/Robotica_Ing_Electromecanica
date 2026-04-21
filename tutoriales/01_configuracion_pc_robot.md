# 01 – Configuración del PC y del robot UR3e para comunicación RTDE con ROS 2

Este tutorial describe **paso a paso** cómo preparar el **PC externo** y el **robot UR3e** para que puedan comunicarse correctamente usando **RTDE** y el paquete Python **`ur_rtde`**, que será la base de todo el curso, junto con ROS2.

---

## 🎯 Objetivos de aprendizaje

Al finalizar este tutorial, el estudiante deberá ser capaz de:

- Verificar la conectividad IP entre PC y robot.
- Configurar correctamente el robot para control remoto.
- Instalar y validar la librería `ur_rtde`.
- Ejecutar scripts sencillos de prueba de comunicación.

---

## 1. Arquitectura general del sistema

En este tutorial **NO** se ejecuta ningún nodo de ROS2, si no que se comunica directamente con el robot. En cualquier caso, la arquitectura adoptada a lo largo del curso es la siguiente:

```text
┌──────────────────────────┐        Ethernet        ┌──────────────────────┐
│ PC externo               │ <------------------->  │ UR3e                 │
│ Ubuntu 22.04             │                        │ Control Box          │
│ ROS 2 Humble             │                        │ RTDE Server          │
│ Python3 + ur_rtde        │                        │                      │
└──────────────────────────┘                        └──────────────────────┘
```

- El **PC** ejecuta ROS 2 y los nodos Python.
- El **robot** expone una interfaz RTDE vía TCP/IP.
- La comunicación se realiza mediante Ethernet.

---

## 2. Requisitos previos

### 2.1 En el PC

- Ubuntu **22.04 LTS**
- ROS 2 **Humble** correctamente instalado
- Python **3.10** o superior
- Acceso de administrador (`sudo`)

Comprobar instalación de ROS 2:

```bash
ros2 --version
```

---

### 2.2 En el robot UR3 / UR3e

- Robot encendido y sin errores
- Sin parada de emergencia (E‑Stop)
- Modo normal de funcionamiento
- Conectado por Ethernet **directamente** al PC

> ⚠️ **Nota**: este curso asume el uso de un robot real. En URSim algunos menús pueden variar.

---

## 3. Configuración de red (PC ↔ Robot)

### 3.1 Direccionamiento IP recomendado

Se recomienda una **red directa PC–robot**, sin DHCP.

| Dispositivo | IP              | Máscara           |
|-------------|-----------------|-------------------|
| PC          | 192.168.56.1    | 255.255.255.0     |
| Robot       | 192.168.56.2    | 255.255.255.0     |

---

### 3.2 Configurar IP en el PC (Ubuntu 22.04)

Ruta gráfica:

```
Ajustes → Red → Cableada → IPv4 → Manual
```

O comprobar desde terminal:

```bash
ifconfig
```

---

### 3.3 Configurar IP en el robot

En el teach pendant abrir el menú en las 3 líneas horizontales de arriba a la derecha:

```
Ajustes → Sistema → Red
```

Acciones:
- Desactivar DHCP
- Asignar dirección IP estática:
  - Dirección IP: 192.168.56.2
  - Máscara Subred: 255.255.255.0
  - Puerta de enlace: 192.168.56.1
  - Servidores DNS: 0.0.0.0
- Guardar configuración

> ![📷](/../main/imagenes/config_red.jpg)
---

## 4. Verificación de conectividad

Desde el PC:

```bash
ping 192.168.56.2
```

Debe recibir como respuesta textos parecidos al siguiente, en el que el tiempo de respuesta debe ser muy pequeño, medido en milisegundos. Resultado esperado:

```text
64 bytes from 192.168.56.2: icmp_seq=1 ttl=64 time=0.3 ms
```

Si no hay respuesta:
- Revisar cable Ethernet
- Revisar IPs y máscara
- Desactivar temporalmente firewall

---

## 5. Configuración del robot para control remoto

### 5.1 Remote Control (UR3e)

En el teach pendant abrir el menú en las 3 líneas horizontales de arriba a la derecha:

```
Ajustes → Sistema → Control Remoto
```

- Habilitar el **Control Remoto**

> ⚠️ Sin el Control Remoto habilitado, los comandos RTDE de control no funcionarán.

---

### 5.2 URCap External Control (solo UR3e)

1. Instalar URCap *External Control* (debería estar hecho ya). Si no, puede [descargarlo aquí](https://github.com/UniversalRobots/Universal_Robots_ExternalControl_URCap/releases).
2. Crear un programa nuevo
3. Añadir el nodo External Control
4. Revisa que la información de la IP del PC es correcta.
5. Selecciona el icono de la tablet arriba a la derecha, con subtítulo **Local** y, a continuación, seleccione **Control Remoto**

> ![📷](/../main/imagenes/control_externo.jpg) 

---

## 6. Instalación de la librería `ur_rtde`

Instalación:

```bash
pip3 install ur_rtde
```

Para verificar que la instalción es correcta, escriba el siguiente comando en un temrinal:

```bash
python3 -c "import rtde_control, rtde_receive, rtde_io; print('ur_rtde OK')"
```

---

## 7. Primer test de comunicación (sin movimiento)

A continuación, vamos a comprobar que la comunicación por RTDE funciona correctamente. Para ello, puede descargar el siguiente arhivo de código Python: [test_rtde.py](https://github.com/davizinho5/Robotica_master/blob/main/scripts_ejemplo/test_rtde.py), o puede generar el script en su PC. 

```python
import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

print("Conectado:", rtde_r.isConnected())
print("Posición articular actual (rad):")
print(rtde_r.getActualQ())

rtde_r.disconnect()
```

Para la ejecución del script, con un terminal situado en la carpeta donde ha guardado el script: 

```bash
python3 test_rtde.py
```

---

## 8. Problemas típicos

| Problema | Causa probable |
|--------|---------------|
| No conecta | IP o red incorrecta |
| Conecta pero no controla | Remote Control desactivado |
| Error RTDE | Robot en parada o error |

---

## 9. Checklist final

- ✅ Ping correcto
- ✅ `ur_rtde` instalado
- ✅ Robot en Remote Control
- ✅ Script de prueba funciona

---

## 10. Conclusión

El sistema está listo para avanzar al [siguiente tutorial](/tutoriales/02_tests_ur_rtde.md), donde se profundizará en el uso de las interfaces `rtde_receive`, `rtde_control` y `rtde_io`. 
