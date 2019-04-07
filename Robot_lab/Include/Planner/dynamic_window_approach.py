# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 3/31/2019 9:11 AM
# @Author: Yao ChengTao
# @File  : dynamic_window_approach.py

import math
import numpy as np
import Include.Draw.draw_function as draw
import Include.Sim_Command.SocketRead as read
import Include.Serial_Communication.command_generate as cmd_generate
import Include.Serial_Communication.serial_send as send

class DWA(object):

    def __init__(self, goal, obstacle):

        self.goal = goal
        self.obstacle_list = obstacle

        # scope of the vel, vel_acc, w, w_acc
        self.min_v = 0                        #   [cm/s]
        self.max_v = 100                        #   [cm/s]
        self.min_w = -90.0*math.pi/180.0        #   [rad/s]
        self.max_w = 90.0*math.pi/180.0         #   [rad/s]
        self.max_v_a = 100                      #   [cm/(s^2)]
        self.max_w_a = 30*math.pi/180.0       #   [rad/(s^2)]
        self.max_v_orientaion = 100.0*math.pi/180.0

        # resolution ratio of the v & w
        self.v_resolution = 10                #   [cm/s]
        self.w_resolution = 2*math.pi/180.0   #   [rad/s]
        self.orientation_resolution = 1*math.pi/180.0
        # sample time & predict time
        self.sample_time = 0.1                  #   [s]
        self.prediect_time = 0.5                #   [s]

        # cost index of goal & speed
        self.heading_cost = 8
        self.velocity_cost = 0.2
        self.dis_cost = 100

        # robot radius
        self.robot_radius = 15.0                 #   [cm]

    def motion(self, x, u):

        """
        :param x: current position ([x, y, orientation, [v, w, v_orientation]])
        :param u: control command [v, w]
        :return: position after motion
        """

        x[0] += u[0]*math.cos(x[2]-u[2])*self.sample_time
        x[1] += u[0]*math.sin(x[2]-u[2])*self.sample_time
        x[2] += u[1]*self.sample_time
        x[3] = u[0]
        x[4] = u[1]
        x[5] = u[2]

        return x

    def control(self, x, u):

        """
        :param x: current position
        :param u: control command [u, w]
        :return: best trajectory and control command
        """

        vr = self.calc_dynamic_window(x)
        u, trajectory = self.generate_best_trajectory(vr, x, u)

        return u, trajectory

    def calc_dynamic_window(self, x):

        """
        :param x: current position
        :return: velocity scope of dynamic window
        """

        vs = [self.min_v, self.max_v, self.min_w, self.max_w]

        vd = [x[3] - self.max_v_a * self.sample_time,
              x[3] + self.max_v_a * self.sample_time,
              x[4] - self.max_w_a * self.sample_time,
              x[4] + self.max_w_a * self.sample_time]

        vr = [max(vs[0], vd[0]), min(vs[1], vd[1]),
              max(vs[2], vd[2]), min(vs[3], vd[3]),
              -self.max_v_orientaion, self.max_v_orientaion]

        # print(vr)
        return vr

    def get_trajectory(self, x_init, v, w, orientation):

        """
        :param x_init: current position
        :param v: velocity control command
        :param w: angular velocity control command
        :param orientation: velocity orientation
        :return: trajectory in prediction time
        """

        x = np.array(x_init)
        trajectory = np.array(x)
        time = 0
        while time <= self.prediect_time:
            x = self.motion(x, [v, w, orientation])
            trajectory = np.vstack((trajectory, x))
            time += self.sample_time

        return trajectory

    def calc_goal_cost(self, trajectory):

        """
        :param trajectory: trajectory in prediction time
        :return: heading goal cost
        """

        dx = self.goal[0] - trajectory[-1, 0]
        dy = self.goal[1] - trajectory[-1, 1]
        theta = math.atan2(dy, dx)
        # print("theta = ", theta/math.pi*180)

        # dis = math.sqrt(dx**2 + dy**2)

        # cost = self.heading_cost * dis
        cost = self.heading_cost * (math.pi - theta)
        return cost

    def calc_obstacle_cost(self, trajectory):

        """
        :param trajectory: trajectory in prediction time
        :return: obstacle cost (1/distance)
        """

        min_dis = float("Inf")

        for i in range(0, len(trajectory[:, 1])):
            for j in range(len(self.obstacle_list[:, 0])):
                ob_x = self.obstacle_list[j, 0]
                ob_y = self.obstacle_list[j, 1]
                dx = trajectory[i, 0] - ob_x
                dy = trajectory[i, 1] - ob_y

                temp_dis = math.sqrt(dx**2 + dy**2)
                if temp_dis <= 2*self.robot_radius:
                    return float("Inf")
                #if trajectory[i, 0]>250 or trajectory[i, 0] < -250 or trajectory[i, 1]>180 or trajectory[i, 1]<-180:
                #    return float("Inf")
                if min_dis >= temp_dis:
                    min_dis = temp_dis

        return 1.0 / min_dis

    def generate_best_trajectory(self, vr, x, u):

        """
        :param vr: velocity
        :param x: current position
        :param u: control command [v, w]
        :return: best trajectory in prediction time and control command
        """

        x_init = x[:]

        final_cost = 10000.0
        final_u = u
        best_trajectory = np.array([x])

        for v in np.arange(vr[0], vr[1], self.v_resolution):
            for w in np.arange(vr[2], vr[3], self.w_resolution):
                for orientation in np.arange(vr[4], vr[5], self.orientation_resolution):
                    temp_trajectory = self.get_trajectory(x_init, v, w, orientation)

                    obstacle_cost = self.dis_cost*self.calc_obstacle_cost(temp_trajectory)
                    goal_cost = self.calc_goal_cost(temp_trajectory)
                    vel_cost = self.velocity_cost*(self.max_v-temp_trajectory[-1, 3])
                    print("obstacle = ",obstacle_cost)
                    print("goal_cost = ", goal_cost)
                    print("vel = ", vel_cost)

                    temp_cost = goal_cost + vel_cost + obstacle_cost
                    # temp_cost = goal_cost

                    if final_cost >= temp_cost:
                        final_cost = temp_cost
                        final_u = [v, w, orientation]
                        best_trajectory = temp_trajectory

        print("final_cost = " ,final_cost)
        return final_u, best_trajectory


def dynamic_windwo_approach(x, u, goal, ob, path, id, serial, isYellow):
    dwa = DWA(goal, ob)
    trajectory = np.array(x)
    get_read = read.socket_read()
    while True:
        u, best_trajectory = dwa.control(x, u)
        draw.draw_trajectory(best_trajectory, x, goal, ob, is_dynamic=True, path=path)
        # print(best_trajectory)
        # x = dwa.motion(x, u)
        cmd = cmd_generate.command_raw(robot_id=id, v=u[0], w=u[1], orientation=u[2])
        # robot_cmd = send.ser_command(com = 'COM3', baud = 115200)
        serial.send_cmd(cmd)
        print(u)
        x = get_read.get_position(id, isYellow)
        x.append(u[0])
        x.append(u[1])
        x.append(u[2])
        # print("x = ", x)
        trajectory = np.vstack((trajectory, x))

        if math.sqrt((x[0]-goal[0])**2 + (x[1]-goal[1])**2) <= 50:
            print("goal")
            break
    return x


def main():
    x = np.array([0.0, 0.0, math.pi/2.0, 0.2, 0.0, 0.0])
    u = [0.2, 0.0, 0.0]
    goal = [10, 10]
    ob = np.array([[-1, -1],
                   [0, 2],
                   [4.0, 2.0],
                   [5.0, 4.0],
                   [5.0, 5.0],
                   [5.0, 6.0],
                   [5.0, 9.0],
                   [8.0, 9.0],
                   [7.0, 9.0],
                   [12.0, 12.0]])
    dwa = DWA(goal, ob)
    trajectory = np.array(x)

    for i in range(1000):
        print("1")
        u, best_trajectory = dwa.control(x, u)
        x = dwa.motion(x, u)
        trajectory = np.vstack((trajectory, x))
        draw.draw_trajectory(best_trajectory, x, goal, ob, is_dynamic=True)
        if math.sqrt((x[0]-goal[0])**2 + (x[1]-goal[1])**2) <= dwa.robot_radius:
            print("goal")
            break
    draw.draw_trajectory(trajectory, x, goal, ob, is_dynamic=False)


if __name__ == '__main__':
    main()
