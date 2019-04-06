import socket
import Include.Sim_Command.Protobuf.grSim_Packet_pb2 as grSim_Packet_pb2
import Include.Sim_Command.Protobuf.grSim_Commands_pb2 as grSim_Commands_pb2
import Include.Sim_Command.Protobuf.grSim_Replacement_pb2 as grSim_Replacement_pb2


def Control_Command(packet):
    packet.commands.timestamp=int(input("Enter timestamp: "))
    packet.commands.isteamyellow=bool(int(input("Enter team (isyellow?): ")))
    control_command=packet.commands.robot_commands.add()
    control_command.id=int(input("Enter robot id: "))
    control_command.kickspeedx=float(input("Enter robot kick speed x: "))
    control_command.kickspeedz=float(input("Enter robot kick speed z: "))
    control_command.veltangent=float(input("Enter robot veltangent: "))
    control_command.velnormal=float(input("Enter robot velnormal: "))
    control_command.velangular=float(input("Enter robot velangular: "))
    control_command.spinner=bool(int(input("Enter spinner: ")))
    control_command.wheelsspeed=bool(int(input("Enter wheelsspeed: ")))
    
girsim_packet = grSim_Packet_pb2.grSim_Packet()
Control_Command(girsim_packet)
print(girsim_packet)

address = ('127.0.0.1', 20011)  
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sk.sendto(girsim_packet.SerializeToString(), address)
while True:
    if input("Command(Y or N ?)：")=="Y":
        Control_Command(girsim_packet)
        print(girsim_packet)
        sk.sendto(girsim_packet.SerializeToString(), address)   
sk.close()
