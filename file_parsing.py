from internal_logic import *


class NodeParser:
    parameters = dict()
    unaltered_parameters = dict()
    initial_information = ""
    action_lst = []
    next_nodes_ids = []
    next_nodes_outputs = []
    presentation = ""
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

    def __init__(self, _initial_information, _parameters, _unaltered_parameters):
        self.initial_information = _initial_information
        self.parameters = _parameters
        self.unaltered_parameters = _unaltered_parameters
        self.action_lst = []
        self.next_nodes_ids = []
        self.next_nodes_outputs = []
        self.presentation = []

    def parse_node(self):
        code_strings = self.initial_information.split('\n')
        for code_string in code_strings:
            if len(code_string) < 2:
                continue
            code_string = code_string.split(':')
            if code_string[0] == 'text':
                self.presentation.append(code_string[1])
                continue
            if code_string[0] == 'action':
                # остаток строки должен содержать 2 аргумента и знак операции
                expr = code_string[1].split(' ')
                if expr[1] == '+':
                    self.action_lst.append(Action(self.action_inc, self.parameters[expr[0]], int(expr[2])))
                if expr[1] == '=':
                    self.action_lst.append(Action(self.action_set, self.parameters[expr[0]], int(expr[2])))
                if expr[1] == '-':
                    self.action_lst.append(Action(self.action_inc, self.parameters[expr[0]], int(expr[2])))
                continue
            if code_string[0] == 'next':
                self.action_lst.append(Action(self.action_select, len(self.next_nodes_ids), 0))
                self.next_nodes_ids.append(int(code_string[1]))
                self.next_nodes_outputs.append(code_string[2])
                continue
            if code_string[0] == 'optional':
                # убираем флаг
                self.action_lst.append(Action(self.action_true, 0, 0))
                # хотим провести все нужные проверки
                for i in range(2, len(code_string) - 1):
                    expr = code_string[i].split(' ')
                    if expr[0] in list(self.parameters.keys()):
                        if expr[1] == '>':
                            self.action_lst.append(Action(self.action_gt, self.parameters[expr[0]], int(expr[2])))
                        if expr[1] == '<':
                            self.action_lst.append(Action(self.action_lt, self.parameters[expr[0]], int(expr[2])))
                        if expr[1] == '>=':
                            self.action_lst.append(Action(self.action_gt, self.parameters[expr[0]], int(expr[2]) - 1))
                        if expr[1] == '<=':
                            self.action_lst.append(Action(self.action_lt, self.parameters[expr[0]], int(expr[2]) + 1))
                    if expr[0] in list(self.unaltered_parameters.keys()):
                        if expr[1] == '>':
                            self.action_lst.append(Action(self.action_gt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2])))
                        if expr[1] == '<':
                            self.action_lst.append(Action(self.action_lt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2])))
                        if expr[1] == '>=':
                            self.action_lst.append(Action(self.action_gt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2]) - 1))
                        if expr[1] == '<=':
                            self.action_lst.append(Action(self.action_lt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2]) + 1))
                self.action_lst.append(Action(self.action_select_if, len(self.next_nodes_ids), 0))
                self.next_nodes_ids.append(int(code_string[1]))
                self.next_nodes_outputs.append(code_string[len(code_string) - 1])
        return Node(self.action_lst, self.presentation, self.next_nodes_ids, self.next_nodes_outputs)


def parse(params, poss):
    parameters = dict()
    unaltered_parameters = dict()
    parameter_values = []
    unaltered_parameters_values = []
    node_id = 0
    node_manager = []
    _next_nodes_ids = []
    _next_nodes_outputs = []
    parameters_ = Parameters([], [], [], [])
    main_state = State(parameters_, node_id, _next_nodes_ids, _next_nodes_outputs, node_manager)
    with open(params) as par:
        flag = True
        par_list = par.read().split('\n')
        for j in range(len(par_list)):
            curr = par_list[j]
            if curr[0] == '*':
                flag = False
                continue
            curr = curr.split(' ')
            if flag:
                parameters[curr[0]] = j
                parameter_values.append(int(curr[1]))
                continue
            unaltered_parameters[curr[0]] = j - len(parameters) - 1
            unaltered_parameters_values.append(curr[1])
    main_state.parameters = Parameters(parameter_values, list(parameters.keys()), unaltered_parameters_values,
                                       list(unaltered_parameters.keys()))
    with open(poss) as pos:
        positions = pos.read().split('&')
        for node in positions:
            parser = NodeParser(node, parameters, unaltered_parameters)
            current = parser.parse_node()
            node_manager.append(current)
        main_state.node_manager = node_manager
    return main_state
