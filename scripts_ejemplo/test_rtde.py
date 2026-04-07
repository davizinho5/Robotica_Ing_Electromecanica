import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

print("Conectado:", rtde_r.isConnected())
print("Posición articular actual (rad):")
print(rtde_r.getActualQ())

rtde_r.disconnect()
