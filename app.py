# -*- coding:utf-8 -*-
from flask import Flask, render_template, request, flash
import json

app = Flask(__name__)
app.secret_key = 'lisenzzz'


@app.route('/')
def hello_world():
    import random
    # 读取数据
    networkTemp = []
    networkFile = open('static/data/Wiki.txt', 'r')
    # 设置节点数和跳数
    number_of_nodes = 105
    max_hops = 2
    for line in networkFile.readlines():
        linePiece = line.split()
        networkTemp.append([int(linePiece[0]), int(linePiece[1])])
    networkFile.close()
    # 初始化权重矩阵
    networkWeight = []
    for i in range(number_of_nodes):
        networkWeight.append([])
        for j in range(number_of_nodes):
            networkWeight[i].append(0)
    # 设置权重
    for linePiece in networkTemp:
        networkWeight[linePiece[0] - 1][linePiece[1] - 1] = 0.3

    # actived_nodes = []

    # 单个节点影响力计算
    def node_influence(node_number, hop, nodes):
        influence = 0
        for node_no in range(number_of_nodes):
            if networkWeight[node_number][node_no] != 0 and node_no not in nodes:
                if random.random() < networkWeight[node_number][node_no]:
                    nodes.append(node_no)
                    influence = influence + 1 + node_influence(node_no, hop + 1, nodes)
        return influence

    # 一次模拟下集合影响力计算
    def one_set_influence(input_set, nodes):
        nodes = []
        influence = len(input_set)
        for set_node_no in input_set:
            nodes.append(set_node_no)
        for set_node_no in input_set:
            # print(set_node_no)
            influence = influence + node_influence(set_node_no, -1, nodes)
        return influence

    # 一次模拟下集合影响力计算
    def one_set_influence_return_nodes(input_set, nodes):
        influence = len(input_set)
        for set_node_no in input_set:
            nodes.append(set_node_no)
        for set_node_no in input_set:
            # print(set_node_no)
            influence = influence + node_influence(set_node_no, -1, nodes)
        return nodes

    # 一万次模拟下集合影响力计算
    def all_set_influence(input_set, nodes):
        influence = 0
        for i in range(10000):
            influence = influence + one_set_influence(input_set, nodes)
        return influence/10000

    # 贪心求最大化影响力种子集合
    def max_influence(set_size):
        nodes = []
        max_set = []
        temp_set = []
        gap = 0
        temp_gap = 0
        candidate_nodes = []
        for node_no in range(number_of_nodes):
            candidate_nodes.append(node_no)
        iteration = 0
        while iteration < set_size:
            for candidate_node in candidate_nodes:
                temp_set.append(candidate_node)
                temp_gap = all_set_influence(temp_set, nodes) - all_set_influence(max_set, nodes)
                if temp_gap > gap:
                    gap = temp_gap
                    temp_node_no = candidate_node
                temp_set.pop()
            if gap == 0:
                continue
            max_set.append(temp_node_no)
            temp_set.append(temp_node_no)
            gap = 0
            candidate_nodes.remove(temp_node_no)
            iteration = iteration + 1
        return max_set

    actived_nodes = []
    max_set = max_influence(1)
    actived_nodes = one_set_influence_return_nodes(max_set, actived_nodes)
    print actived_nodes
    max_set = json.dumps(max_set)
    actived_nodes = json.dumps(actived_nodes)
    networkWeight = json.dumps(networkWeight)
    return render_template('index.html', number_of_nodes=number_of_nodes, max_set=max_set, actived_nodes=actived_nodes, networkWeight=networkWeight)


if __name__ == '__main__':
    app.run()
