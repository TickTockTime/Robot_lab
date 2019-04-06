import sys
import socket
sys.path.append("../Include/")
import Include.Sim_Command.Protobuf.zss_debug_pb2 as zss_debug_pb2

class Draw_Graph(object):
    def __init__(self, color, path):
        self.path = path
        self.color = color
        self.draw = zss_debug_pb2.Debug_Msgs()
    
    def send_graph(self):
        address = ('127.0.0.1',20001)
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sk.sendto(self.draw.SerializeToString(),address)
        
    def draw_line(self, start, end):
        messages = self.draw.msgs.add()
        messages.type = 1
        messages.color = self.color
        messages.line.start.x = start[0]
        messages.line.start.y = start[1]
        messages.line.end.x = end[0]
        messages.line.end.y = end[1]
        messages.line.FORWARD=True
        messages.line.BACK=True
        
    def draw_rec(self, start, end):
        self.draw_line(start, [end[0], start[1]])
        self.draw_line([end[0], start[1]], end)
        self.draw_line(end, [start[0], end[1]])
        self.draw_line([start[0], end[1]],start)
    def draw_path(self):
        for i in range(len(self.path)-1):
            self.draw_line(self.path[i],self.path[i+1])
            print(self.path[i])
        self.send_graph()
"""
class Draw_Path(object):
    def ___init__(self, path):
        self.path = path
    def draw_path(self):
        for i in range(len(self.path)):
            draw = Draw_Graph(self.path[i],self.path[i+1],0)
            draw.draw_line()
        draw.send_graph()
"""      
        

def test():
    b= [[2,2],[5,7],[20,-30],[100,180]]
    draw = Draw_Graph(color=0, path=b)
    draw.draw_path()
    """
    draw = Draw_Graph(start=[2,2], end=[30, 30], color=0)
    draw.draw_rec()
    draw.draw_line()
    draw.send_graph()
    """
if __name__=="__main__":
    test()

