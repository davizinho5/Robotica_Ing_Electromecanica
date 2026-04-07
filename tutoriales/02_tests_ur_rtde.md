# 02 – Tests del paquete ur_rtde

En este tutorial se realizan **pruebas prácticas y controladas** de las tres interfaces principales del paquete **ur_rtde**, que permiten comunicarse con un robot UR3/UR3e mediante RTDE:

- `rtde_receive` → lectura del estado del robot, información de sensores y de la controladora
- `rtde_control` → configuración y envío de movimientos al robot
- `rtde_io` → control de entradas y salidas analógicas y digitales

El objetivo es que el estudiante **entienda claramente para qué sirve cada interfaz**, cómo se usa y qué precauciones tomar.

---

## ⚠️ Advertencia de seguridad

En este tutorial **SÍ se realizan movimientos del robot**.

Antes de continuar, asegúrate de que:
- El robot está en un entorno despejado
- Existe acceso inmediato al botón de parada de emergencia
- Se entiende cada comando antes de ejecutarlo

---

## 1. Test de la interfaz rtde_receive

La interfaz `rtde_receive` se utiliza para **leer el estado actual del robot**. Permite obtener, entre otros:
- Posición articular
- Pose TCP (posición y orientación de la herramienta)
- Velocidades de los motores
- Fuerzas medidas por el sensor de la muñeca
- Estados de IO

### 1.1 Script de prueba

A continuación, vamos a comprobar que la interfaz de recepción de información del estado del robot  funciona correctamente. Para ello, puede descargar el siguiente arhivo de código Python: [test_rtde_receive.py](https://github.com/davizinho5/Robotica_master/blob/main/scripts_ejemplo/test_rtde_receive.py), o puede generar el script en su PC. En este código, se establece la conexión ocn el robot y se leen las posiciones de cada uno de los motores, la posición y orientación (Pose) de la herramienta,m y las fuerzas medidas por el sensor de fuerza/par situado en la muñeca del brazo robótico.

```python
import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

print("Conectado:", rtde_r.isConnected())
print("Posición articular (rad):", rtde_r.getActualQ())
print("Pose TCP [x,y,z,rx,ry,rz]:", rtde_r.getActualTCPPose())
print("Fuerza TCP:", rtde_r.getActualTCPForce())

rtde_r.disconnect()
```

Ejecución:

```bash
python3 test_rtde_receive.py
```

Resultado esperado:
- No hay errores
- Se muestran datos numéricos coherentes
- El robot NO se mueve

> ![📷](/../main/imagenes/test_receive.png) 
---

## 2. Test de la interfaz rtde_io

La interfaz `rtde_io` permite **escribir salidas** digitales, analógicas estántar o de la herramienta.
Uha vez hecho el cambio, se puede usar la interfaz `rtde_receive` para leer el estado de la salida y comprobar si se ha efectuado correctamente. Además, en la tablet del robot, en la **pestaña E/S**, se puede observar cómo se activa y se desactiva dicha señal.

### 2.1 Script de prueba de IO digital

```python
import time
import rtde_io
import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_i = rtde_io.RTDEIOInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

DO_PIN = 1

print("Activando salida digital", DO_PIN)
rtde_i.setStandardDigitalOut(DO_PIN, True)
time.sleep(2.0)

print("Estado DO:", rtde_r.getDigitalOutState(DO_PIN))

print("Desactivando salida digital", DO_PIN)
rtde_i.setStandardDigitalOut(DO_PIN, False)
time.sleep(1.0)

print("Estado DO:", rtde_r.getDigitalOutState(DO_PIN))

rtde_i.disconnect()
rtde_r.disconnect()
```

Ejecución:

```bash
python3 test_rtde_io.py
```

Resultado esperado:
- Cambio de estado en la salida digital estándar 1, se activa durante 2 segundos, y luego se desactiva. 
> ![📷](/../main/imagenes/pestanaES.jpg) 

### 2.2 Ejercicios propuestos
- Cambie los pines de la salida digital que se está activando para mover la cinta transportadora hacia delante y hacia atrás.
- Use la función de la interfez de IO `setToolDigitalOut(num, estado)` para abrir y cerrar la pinza controlando las salidas digitales de la herramienta. num será el númeor de la salida (que puede ser 0 o 1), y estado se usa para activa o desactivar la salida (True o False)

---

## 3. Test de la interfaz rtde_control

La interfaz `rtde_control` permite configurar y **enviar comandos de movimiento** al robot. En los brazos robóticos podemos distinguir fundamentalmente 2 tipos de movimientos: 
- Movimientos articulares, de los motores del brazo, en el que se envían posiciones objetivo para los motores.
- Movimientos cartesianoso lineales, se envía un posición y orientación objetivo de la herramienta.

> ⚠️ **Nota**: siempre que esté haciendo movimientos de prueba en el robot, utilice **velocidades bajas**.


### 3.1 Movimiento articular simple (moveJ)

En la primera prueba se va utilizar el movimiento articular, que siempre es más seguro. Para ello, se van a leer las posiciones actuales del brazo robótico y se va a aumentar la posición de uno de los motores en 10 grados. Para el ejemplo se ha elegido el sexto motor del brazo, que será el motor de la muñeca, ya que es el más seguro
El script de ejemplo lo puede desrcargar o crearlo en su ordenador: [test_rtde_control_moveJ.py](https://github.com/davizinho5/Robotica_master/blob/main/scripts_ejemplo/test_rtde_control_moveJ.py), o puede generar el script en su PC. 

```python
import time
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

delta = -10 * 3.141592653589793 / 180.0

q_actual = rtde_r.getActualQ()
q_target = list(q_actual)
q_target[5] += delta  # pequeño movimiento

print("Moviendo robot...")
rtde_c.moveJ(q_target, speed=0.2, acceleration=0.1)

print("Movimiento finalizado")

rtde_c.disconnect()
rtde_r.disconnect()
```

Ejecución:

```bash
python3 test_rtde_control_moveJ.py
```

Resultado esperado:
- El robot realiza un pequeño movimiento en la muñeca a la velocidad pedida.


### 3.1 Movimiento lineal simple (moveL)
En esta prueba se va a mover el robot a una pose (posición y orientación) conocida cercana a la actual. Para ello, se va a leer la pose actual del brazo brazo robótico. Después, se calculará la pose objectivo como la misma pose actual, pero con un incremento en el eje Z de 2 cm. Por lo tanto, el brazo debería subir hacir arriba. Por último, se leerá la pose actual del robot para comprobar que, efectivamente, se ha movido el brazo robótico. 

El script de ejemplo lo puede desrcargar o crearlo en su ordenador: [test_rtde_control_moveL.py](https://github.com/davizinho5/Robotica_master/blob/main/scripts_ejemplo/test_rtde_control_moveL.py), o puede generar el script en su PC. 

```python
import time
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.56.2"   # Cambia por la dirección de tu robot

# --- Crear interfaces RTDE ---
rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

# --- Leer la pose actual del TCP ---
tcp_pose = rtde_r.getActualTCPPose()
print("Pose actual del TCP:", tcp_pose)

# tcp_pose es un vector: [x, y, z, rx, ry, rz]
# Subimos 2 cm en el eje Z → 0.02 m
target_pose = tcp_pose.copy()
target_pose[2] += 0.02    # elevar Z

print("Nueva pose objetivo:", target_pose)

# --- Movimiento lineal moveL ---
speed = 0.15        # m/s  (valor seguro)
acceleration = 0.25 # m/s² (valor seguro)

print("Ejecutando movimiento lineal hacia arriba 2 cm...")
rtde_c.moveL(target_pose, speed, acceleration)

print("Movimiento completado.")

# --- Leer la pose actual del TCP ---
tcp_pose = rtde_r.getActualTCPPose()
print("Pose actual del TCP:", tcp_pose)

# --- Desconectar ---
rtde_c.disconnect()
rtde_r.disconnect()
```

Ejecución:

```bash
python3 test_rtde_control_moveL.py
```

Resultado esperado:
- El robot realiza un pequeño movimiento subiendo la herramienta en vertical, 2 cm en el eje Z. 


### 3.3 Ejercicios propuestos

- Realice modificaciones en los ejemplos anteriores para entender bien qué movimientos puede mandar hacer al robot. Tenga en cuenta que los cambios en orientación del robot no son evidentes, luego no use moveL para cambiar la orientación sin consultar con el profesor. 

---

## 4. Checklist final

- ✅ rtde_receive funciona correctamente
- ✅ rtde_io controla salidas digitales
- ✅ rtde_control mueve el robot de forma segura
- ✅ Se entiende la diferencia entre interfaces

---

## 5. Conclusión

Tras este tutorial, el estudiante conoce y ha probado todas las interfaces principales de `ur_rtde`, quedando preparado para integrarlas dentro de nodos ROS 2. 

Está listo para avanzar al [siguiente tutorial](https://github.com/davizinho5/Robotica_master/blob/main/tutoriales/03_paquete_UR3_driver.md), donde se integragan algunas interfaces de rtde en ROS2. 
