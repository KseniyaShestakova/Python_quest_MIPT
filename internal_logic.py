import keyboard
import random
from interface import *


class NodeManager:
    node_manager = []

    def __init__(self, arr):
        self.node_manager = arr

    def get_node_by_id(self, identifier):
        return self.node_manager[identifier]


class Parameters:
    unaltered_parameters_name = []
    unaltered_parameters_value = []
    parameter_value = []
    parameter_name = []

    def __init__(self, val, names, unaltered_val, unaltered_names):
        self.unaltered_parameters_value = unaltered_val
        self.unaltered_parameters_name = unaltered_names
        self.parameter_value = val
        self.parameter_name = names

    def increase(self, number, difference):
        self.parameter_value[number] += difference

    def set(self, number, value):
        self.parameter_value[number] = value

    def set_unaltered(self, number, value):
        self.unaltered_parameters_value[number] = value

    def get(self, number):
        return self.parameter_value[number]

    def get_name(self, number):
        return self.parameter_name[number]

    def get_unaltered(self, number):
        return self.unaltered_parameters_value[number]

    def get_unaltered_name(self, number):
        return self.unaltered_parameters_name[number]


class Action:
    action_id = 0
    first_arg = 0
    second_arg = 0

    def __init__(self, id, f_arg, s_arg):
        self.action_id = id
        self.first_arg = f_arg
        self.second_arg = s_arg


class Node:
    # хранит в себе список действий, которые надо сделать, положений, в которые можно перейти,
    # и строки, их описывающие (ну и строку, которая выводится, когда мы заходим в это положение)
    action_list = []
    presentation = []
    next_nodes = []
    next_nodes_output = []

    def __init__(self, action_list_, presentation_, next_nodes_, next_nodes_output_):
        self.action_list = action_list_
        self.presentation = presentation_

        self.next_nodes = next_nodes_
        self.next_nodes_output = next_nodes_output_


class State:
    flag = True
    parameters = Parameters([], [], [], [])
    node_id = 0
    next_nodes_ids = []
    next_nodes_outputs = []
    node_manager = NodeManager([])  # универсальный список, хранящий все ноды
    end_of_the_game = False

    action_select = 0
    action_select_if = 1
    action_gt = 2
    action_lt = 3
    action_neg = 4
    action_true = 5
    action_set = 6
    action_inc = 7
    action_gt_unaltered = 8
    action_lt_unaltered = 9
    action_random = 10

    outputer = Outputer()
    inputer = Inputer()

    def __init__(self, parameters_, node_id_, next_nodes_ids, next_nodes_outputs_, node_manager_):
        self.parameters = parameters_
        self.node_id = node_id_
        self.next_nodes_ids = next_nodes_ids
        self.next_nodes_outputs = next_nodes_outputs_
        self.node_manager = node_manager_

    def set_parameter(self, parameter_id, val):
        self.parameters.set(parameter_id, val)

    def set_unaltered_parameter(self, parameter_id, val):
        self.parameters.set_unaltered(parameter_id, val)

    def increase_parameter(self, parameter_id, val):
        self.parameters.increase(parameter_id, val)

    def greater(self, parameter_id, val):
        self.flag = (self.flag and self.parameters.get(parameter_id) > val)

    def less(self, parameter_id, val):
        self.flag = (self.flag and self.parameters.get(parameter_id) < val)

    def greater_unaltered(self, parameter_id, val):
        self.flag = (self.flag and int(self.parameters.get_unaltered(parameter_id)) > val)

    def less_unaltered(self, parameter_id, val):
        self.flag = (self.flag and int(self.parameters.get_unaltered(parameter_id)) < val)

    def add_node(self, node_identifier):
        current_node = self.node_manager.get_node_by_id(self.node_id)
        self.next_nodes_ids.append(current_node.next_nodes[node_identifier])
        self.next_nodes_outputs.append(current_node.next_nodes_output[node_identifier])

    def randomize(self, probability):
        x = random.randint(0, probability)
        if x == 0:
            self.flag = True
        else:
            self.flag = False

    def show_parameters(self):

        arr_of_strings = ["Current characteristics: "]\
                         + [self.parameters.get_name(i) + ": " + str(self.parameters.get(i))
                            for i in range(len(self.parameters.parameter_value))]
        self.outputer.output_parameters(arr_of_strings)

    def perform_selection(self):
        arr_of_strings = ["You need to choose something from the options: "] + self.next_nodes_outputs
        self.outputer.output_choice(arr_of_strings)
        c = 0

        for i in range(10):
            if i == 9:
                arr_of_strings = ["Maximum number of calls reached.",
                                  "Stay on the choice: " + self.next_nodes_outputs[c % len(self.next_nodes_outputs)]]
                self.outputer.output_error(arr_of_strings)
                break
            if keyboard.read_key() == 'ctrl':
                c += 1
                self.outputer.output_tmp("Now on choice: " + self.next_nodes_outputs[c % len(self.next_nodes_outputs)])

            if keyboard.read_key() == 'enter':
                break

        self.node_id = self.next_nodes_ids[c % len(self.next_nodes_outputs)]

    def activate_node(self):
        current_node = self.node_manager.get_node_by_id(self.node_id)
        self.outputer.output_location(current_node.presentation)
        if len(current_node.action_list) == 0:
            self.end_of_the_game = True
        self.next_nodes_ids.clear()
        self.next_nodes_outputs.clear()
        self.flag = True
        for i in current_node.action_list:
            if i.action_id == self.action_select:
                self.add_node(i.first_arg)
                continue
            if i.action_id == self.action_select_if:
                if self.flag:
                    self.add_node(i.first_arg)
                continue
            if i.action_id == self.action_gt:
                self.greater(i.first_arg, i.second_arg)
                continue
            if i.action_id == self.action_lt:
                self.less(i.first_arg, i.second_arg)
            if i.action_id == self.action_neg:
                if self.flag:
                    self.flag = False
                else:
                    self.flag = True
                continue
            if i.action_id == self.action_true:
                self.flag = True
                continue
            if i.action_id == self.action_set:
                self.set_parameter(i.first_arg, i.second_arg)
                continue
            if i.action_id == self.action_inc:
                self.increase_parameter(i.first_arg, i.second_arg)
                continue
            if i.action_id == self.action_gt_unaltered:
                self.greater_unaltered(i.first_arg, i.second_arg)
                continue
            if i.action_id == self.action_lt_unaltered:
                self.less_unaltered(i.first_arg, i.second_arg)
            if i.action_id == self.action_random:
                self.randomize(i.first_arg)
        self.show_parameters()
        if not self.end_of_the_game:
            self.perform_selection()

    def start(self):
        for i in range(len(self.parameters.unaltered_parameters_name)):
            self.outputer.output_unaltered("Choose " + self.parameters.get_unaltered_name(i) + ": ")
            val = self.inputer.input_()
            self.set_unaltered_parameter(i, val)

        while not self.end_of_the_game:
            self.activate_node()
