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

