# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 3/31/2019 12:07 AM
# @Author: Yao Chengtao
# @File  : extra_rapidly_exploring_random_tree.py

import matplotlib.pyplot as plt
import math
import copy
import random

class ERRT_Node(object):
    """
    :param position(x,y)
    :param parent
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.parent = None

class ERRT_Plan(object):
    """
    ERRT planning
    """
    def __init__(self, start, goal, obstacle, map_scope):
        """
        :param start: start position (ERRT_Node)
        :param goal: goal position  (ERRT_Node)
        :param obstacle: obstacle_list ([x,y,size])
        :param map_scope:
        """
        self.start = ERRT_Node(start[0], start[1])
        self.goal = ERRT_Node(goal[0], goal[1])
        self.map_scope = map_scope
        self.q = 0.3
        self.p = 0.4
        self.step_distance = 2
        self.obstacle_list = obstacle
        self.node_list = [self.start]

    def generate_random_node(self):
        rand_x = random.randint(self.map_scope[0], self.map_scope[1])
        rand_y = random.randint(self.map_scope[2], self.map_scope[3])
        rand_node = [rand_x, rand_y]
        return rand_node

    @staticmethod
    def isCollision(new_node, obstacle):
        status = False
        for ob in obstacle:
            dx = new_node.x - ob[0]
            dy = new_node.y - ob[1]
            d = math.sqrt(dx**2 + dy**2)
            if d<ob[2]:
                status = True
        return status

    @staticmethod
    def get_nearest_node(rand_node, node_list):
        distance_list = []
        for node in node_list:
            dx = node.x - rand_node[0]
            dy = node.y - rand_node[1]
            distance_list.append((dx**2 + dy**2))
        min_index = distance_list.index(min(distance_list))
        return min_index

    def errt_planning(self):
        while True:
            # generate random node
            rnd = random.random()
            if rnd > self.p:
                rand_node = self.generate_random_node()
            else:
                rand_node = [self.goal.x, self.goal.y]

            # find the nearest node
            min_dis_index = self.get_nearest_node(rand_node, self.node_list)
            nearest_node = self.node_list[min_dis_index]

            # generate new node
            theta = math.atan2(rand_node[1] - nearest_node.y, rand_node[0] - nearest_node.x)
            new_node = copy.deepcopy(nearest_node)
            new_node.x += self.step_distance * math.cos(theta)
            new_node.y += self.step_distance * math.sin(theta)
            new_node.parent = min_dis_index

            # check whether collision
            if self.isCollision(new_node, self.obstacle_list):
                continue

            # add new node to path
            self.node_list.append(new_node)

            # check whether arrive the goal
            dx = new_node.x - self.goal.x
            dy = new_node.y - self.goal.y
            d = math.sqrt(dx**2 + dy**2)
            if d <= self.step_distance:
                print("Find the path!")
                break

        # fina and return the path
        path = [[self.goal.x, self.goal.y]]
        index = len(self.node_list) - 1
        while self.node_list[index].parent is not None:
            node = self.node_list[index]
            path.append([node.x, node.y])
            index = node.parent
        path.append([self.start.x, self.start.y])

        return path

def main():
    """
    Example about ERRT planning
    :return:
    """
    obstacle  =[[5, 1, 1],
                [3, 6, 2],
                [3, 8, 2],
                [1, 1, 2],
                [3, 5, 2],
                [9, 5, 2],
                [3, 0, 3]]
    errt = ERRT_Plan(start = [0, 0], goal = [100, 210], map_scope = [-450, 450, -600, 600],  obstacle=obstacle)
    path = errt.errt_planning()
    print(path[::-1])

if __name__=="__main__":
    main()





