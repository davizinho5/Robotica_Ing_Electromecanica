import time
import rtde_control
import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

delta = -10 * 3.141592653589793 / 180.0

q_actual = rtde_r.getActualQ()
q_target = list(q_actual)
q_target[4] += delta  # pequeño movimiento

print("Moviendo robot...")
rtde_c.moveJ(q_target, speed=0.2, acceleration=0.1)

print("Movimiento finalizado")

rtde_c.disconnect()
rtde_r.disconnect()
