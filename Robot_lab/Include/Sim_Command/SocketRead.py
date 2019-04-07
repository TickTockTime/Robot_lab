import socket
import Include.Sim_Command.Protobuf.vision_detection_pb2 as vision_detection_pb2
import Include.Draw.draw_function as draw


class socket_read(object):
    def __init__(self):
        self.ip_port = ('127.0.0.1', 23333)
        self.frame = vision_detection_pb2.Vision_DetectionFrame()
        self.size = 2*15

    def get_obstacle(self, id, isYellow):
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sk.bind(self.ip_port)
        msg = sk.recv(4096)
        self.frame.ParseFromString(msg)
        obstacle = []
        if isYellow == True:
            for blue in self.frame.robots_blue:
                obstacle.append([blue.x / 10, blue.y / 10, self.size])
            for yellow in self.frame.robots_yellow:
                if yellow.robot_id != id:
                    obstacle.append([yellow.x / 10, yellow.y / 10, self.size])
        else:
            for blue in self.frame.robots_blue:
                if blue.robot_id != id:
                    obstacle.append([blue.x / 10, blue.y / 10, self.size])
            for yellow in self.frame.robots_yellow:
                    obstacle.append([yellow.x / 10, yellow.y / 10, self.size])

        return obstacle

    def get_position(self, id, isYellow):

        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sk.bind(self.ip_port)
        msg = sk.recv(4096)
        self.frame.ParseFromString(msg)

        if isYellow == True:
            for yellow in self.frame.robots_yellow:
                if yellow.robot_id == id:
                    start = [yellow.x / 10, yellow.y / 10, yellow.orientation]
        else:
            for blue in self.frame.robots_blue:
                if blue.robot_id == id:
                    start = [blue.x / 10, blue.y / 10, blue.orientation]

        print("start =", start)

        return start

    """
    def get_time_info(self):
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sk.bind(self.ip_port)
        msg = sk.recv(4096)
        self.frame.ParseFromString(msg)
        temp = self.frame.robots_yellow[0]
        info = [temp.x / 10, temp.y / 10, temp.orientation]
        return info
    """

def test():
    read = socket_read()
    obstacle = read.get_obstacle(0, True)
    x = read.get_position(0, True)
    goal = [-240, 170]
    # draw.draw_path([[0, 0]], x, goal, obstacle)
    # print(x)
    # read.get_position()
    # info = read.get_time_info()
    # print(info)


if __name__ == "__main__":
    test()
