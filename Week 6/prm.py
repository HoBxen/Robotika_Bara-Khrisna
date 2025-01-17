#!#usr/bin/env python3
import matplotlib.pyplot as plt
import rospy
import numpy as np
import math

class Point:
    def __init__(self, x, y):  # Perbaikan dari _init_
        self.x = x
        self.y = y

class Node:
    def __init__(self, x, y, node_id):  # Perbaikan dari _init_
        self.point = Point(x, y)
        self.node_id = node_id
        self.neighbors = []

class PRM:
    def __init__(self, x_max, x_min, y_max, y_min, numNodes):  # Perbaikan dari _init_
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.numNodes = numNodes
        self.nodes = []
        self.nodes.append(Node(0, 0, 0))  # Start node
        self.nodes.append(Node(18, 18, 1))  # Goal node

    def generateRandomPoints(self, obsVec):
        total = 0
        while total < self.numNodes:
            p = Node(np.random.uniform(self.x_min, self.x_max),
                     np.random.uniform(self.y_min, self.y_max), total + 2)
            if not self.intersectsObs(p.point, p.point, obsVec) and self.isWithinWorld(p.point):
                self.nodes.append(p)
                total += 1

    def computeNeighborGraph(self, obsVec):
        for i in self.nodes:
            distanceMap = []
            for j in self.nodes:
                if i.node_id != j.node_id and not self.intersectsObs(i.point, j.point, obsVec):
                    distanceMap.append((self.getEuclideanDistance(i.point, j.point), j))
            distanceMap = sorted(distanceMap, key=lambda x: x[0])
            for count, pair in enumerate(distanceMap):
                if count >= 10:
                    break
                i.neighbors.append(pair[1])

    def solveShortestPath(self):
        dist = [float('inf')] * (self.numNodes + 2)
        dist[0] = 0
        prev = [-1] * (self.numNodes + 2)
        vset = [True] * (self.numNodes + 2)
        while any(vset):
            u = min((d, i) for i, d in enumerate(dist) if vset[i])[1]
            vset[u] = False
            for v in self.getById(u).neighbors:
                alt = dist[u] + self.getEuclideanDistance(self.getById(u).point, v.point)
                if alt < dist[v.node_id]:
                    dist[v.node_id] = alt
                    prev[v.node_id] = u
        path = []
        node = 1
        while node != -1:
            path.append(node)
            node = prev[node]
        return path[::-1]  # Reverse the path to start from the start node

    def getEuclideanDistance(self, p1, p2):
        return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)  # Menggunakan **2 untuk kuadrat

    def isWithinWorld(self, p):
        return self.x_min <= p.x <= self.x_max and self.y_min <= p.y <= self.y_max

    def intersectsObs(self, p1, p2, obsVec):
        return False  # Simplified for now

    def getById(self, node_id):
        return next((node for node in self.nodes if node.node_id == node_id), None)

    def plotGraph(self, path=None):
        plt.figure()

        # Plot all edges in the PRM
        for node in self.nodes:
            for neighbor in node.neighbors:
                plt.plot([node.point.x, neighbor.point.x], [node.point.y, neighbor.point.y], 'r-', alpha=0.3)

        # Plot the nodes
        for node in self.nodes:
            plt.plot(node.point.x, node.point.y, 'bo')  # Blue circles for nodes

        # Mark the start and goal nodes
        plt.plot(self.nodes[0].point.x, self.nodes[0].point.y, 'go', markersize=10, label="Start")  # Green for start
        plt.plot(self.nodes[1].point.x, self.nodes[1].point.y, 'ro', markersize=10, label="Goal")   # Red for goal

        # If there's a path, plot it in a different color
        if path is not None:
            for i in range(len(path) - 1):
                p1 = self.getById(path[i]).point
                p2 = self.getById(path[i + 1]).point
                plt.plot([p1.x, p2.x], [p1.y, p2.y], 'y-', linewidth=2)  # Yellow for shortest path

        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.title("Probabilistic Roadmap (PRM) with Shortest Path")
        plt.show()

if __name__ == "__main__":
    rospy.init_node('prm_node', anonymous=True)
    x_max = rospy.get_param('~x_max', 20)
    x_min = rospy.get_param('~x_min', 0)
    y_max = rospy.get_param('~y_max', 20)
    y_min = rospy.get_param('~y_min', 0)
    numNodes = rospy.get_param('~numNodes', 50)

    prm = PRM(x_max, x_min, y_max, y_min, numNodes)
    obsVec = []  # No obstacles for simplicity
    prm.generateRandomPoints(obsVec)
    prm.computeNeighborGraph(obsVec)

    path = prm.solveShortestPath()
    rospy.loginfo("Shortest path found: %s", path)

    # Plot the graph and shortest path
    prm.plotGraph(path)
