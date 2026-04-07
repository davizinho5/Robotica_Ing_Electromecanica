import rtde_receive

ROBOT_IP = "192.168.56.2"

rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

print("Conectado:", rtde_r.isConnected())
print("Posición articular (rad):", rtde_r.getActualQ())
print("Pose TCP [x,y,z,rx,ry,rz]:", rtde_r.getActualTCPPose())
print("Fuerza TCP:", rtde_r.getActualTCPForce())

rtde_r.disconnect()
