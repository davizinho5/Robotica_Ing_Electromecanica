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
time.sleep(2.0)

print("Estado DO:", rtde_r.getDigitalOutState(DO_PIN))

rtde_i.disconnect()
rtde_r.disconnect()
