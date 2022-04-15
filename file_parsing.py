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
    action_random = 10

    def __init__(self, _initial_information, _parameters, _unaltered_parameters):
        self.initial_information = _initial_information
        self.parameters = _parameters
        self.unaltered_parameters = _unaltered_parameters
        self.action_lst = []
        self.next_nodes_ids = []
        self.next_nodes_outputs = []
        self.presentation = []

    def parse_text(self, code_string, initial):
        if len(code_string) < 2:
            raise Exception('Syntax error in the line: ' + initial)
        self.presentation.append(code_string[1])
        

    def parse_action(self, code_string, initial):
        if len(code_string) < 2:
            raise Exception('Syntax error in the line: ' + initial)
        # остаток строки должен содержать 2 аргумента и знак операции
        expr = code_string[1].split(' ')
        if len(expr) != 3 or not expr[1] in ['+', '=', '-'] or not expr[0] in self.parameters:
            raise Exception('Syntax error in the line: ' + initial)
        if expr[1] == '+':
            self.action_lst.append(Action(self.action_inc, self.parameters[expr[0]], int(expr[2])))
        if expr[1] == '=':
            self.action_lst.append(Action(self.action_set, self.parameters[expr[0]], int(expr[2])))
        if expr[1] == '-':
            self.action_lst.append(Action(self.action_inc, self.parameters[expr[0]], -int(expr[2])))

    def parse_next(self, code_string, initial):
        if len(code_string) != 3:
            raise Exception('Syntax error in the line: ' + initial)
        self.action_lst.append(Action(self.action_select, len(self.next_nodes_ids), 0))
        self.next_nodes_ids.append(int(code_string[1]))
        self.next_nodes_outputs.append(code_string[2])

    def check(self, expr):
        if expr[1] == '>':
            self.action_lst.append(Action(self.action_gt, self.parameters[expr[0]], int(expr[2])))
        if expr[1] == '<':
            self.action_lst.append(Action(self.action_lt, self.parameters[expr[0]], int(expr[2])))
        if expr[1] == '>=':
            self.action_lst.append(Action(self.action_gt, self.parameters[expr[0]], int(expr[2]) - 1))
        if expr[1] == '<=':
            self.action_lst.append(Action(self.action_lt, self.parameters[expr[0]], int(expr[2]) + 1))

    def check_unaltered(self, expr):
        if expr[1] == '>':
            self.action_lst.append(
                Action(self.action_gt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2])))
        if expr[1] == '<':
            self.action_lst.append(
                Action(self.action_lt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2])))
        if expr[1] == '>=':
            self.action_lst.append(
                Action(self.action_gt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2]) - 1))
        if expr[1] == '<=':
            self.action_lst.append(
                Action(self.action_lt_unaltered, self.unaltered_parameters[expr[0]], int(expr[2]) + 1))

    def parse_optional(self, code_string, initial):
        if len(code_string) < 2:
            raise Exception('Syntax error in the line: ' + initial)
        # убираем флаг
        self.action_lst.append(Action(self.action_true, 0, 0))
        # хотим провести все нужные проверки
        for i in range(2, len(code_string) - 1):
            expr = code_string[i].split(' ')
            if len(expr) != 3 or not expr[1] in ['<', '<=', '>', '>=']:
                raise Exception('Syntax error in the line: ' + initial)
            if expr[0] in list(self.parameters.keys()):
                self.check(expr)
            elif expr[0] in list(self.unaltered_parameters.keys()):
                self.check_unaltered(expr)
            else:
                raise Exception('Syntax error in the line: ' + initial)
        self.action_lst.append(Action(self.action_select_if, len(self.next_nodes_ids), 0))
        self.next_nodes_ids.append(int(code_string[1]))
        self.next_nodes_outputs.append(code_string[len(code_string) - 1])

    def parse_random(self, code_string, initial):
        if len(code_string) != 4:
            raise Exception('Syntax error in the line: ' + initial)
        self.action_lst.append(Action(self.action_random, int(code_string[2]), 0))
        self.action_lst.append(Action(self.action_select_if, len(self.next_nodes_ids), 0))
        self.next_nodes_ids.append(int(code_string[1]))
        self.next_nodes_outputs.append(code_string[len(code_string) - 1])

    def parse_node(self):
        code_strings = self.initial_information.split('\n')
        for code_string in code_strings:
            if len(code_string) < 2:
                continue
            initial = code_string
            code_string = code_string.split(':')

            if code_string[0] == 'text':
                self.parse_text(code_string, initial)
                continue
            if code_string[0] == 'action':
                self.parse_action(code_string, initial)
                continue
            if code_string[0] == 'next':
                self.parse_next(code_string, initial)
                continue
            if code_string[0] == 'optional':
                self.parse_optional(code_string, initial)
                continue
            if code_string[0] == 'random':
                self.parse_random(code_string, initial)
        return Node(self.action_lst, self.presentation, self.next_nodes_ids, self.next_nodes_outputs)


class Parser:
    parameters = dict()
    unaltered_parameters = dict()
    parameter_values = []
    unaltered_parameters_values = []
    flag = True
    node_id = 0
    node_manager = []
    _next_nodes_ids = []
    _next_nodes_outputs = []
    parameters_ = Parameters([], [], [], [])
    main_state = State(parameters_, node_id, _next_nodes_ids, _next_nodes_outputs, NodeManager(node_manager))

    def parse_parameters(self, par_list):

        for j in range(len(par_list)):
            curr = par_list[j]
            if len(curr) == 0:
                continue
            if curr[0] == '*':
                self.flag = False
                continue
            curr = curr.split(' ')
            if self.flag:
                self.parameters[curr[0]] = j
                self.parameter_values.append(int(curr[1]))
                continue
            self.unaltered_parameters[curr[0]] = j - len(self.parameters) - 1
            self.unaltered_parameters_values.append(curr[1])
        return self.parameters, self.unaltered_parameters, self.parameter_values, self.unaltered_parameters_values

    def parse(self, params, poss):

        with open(params) as par:
            par_list = par.read().split('\n')
            construct_tuple = self.parse_parameters(par_list)
        self.main_state.parameters = Parameters(construct_tuple[2], list(construct_tuple[0].keys()), construct_tuple[3],
                                           list(construct_tuple[1].keys()))
        with open(poss) as pos:
            positions = pos.read().split('&')
            for node in positions:
                parser = NodeParser(node, construct_tuple[0], construct_tuple[1])
                current = parser.parse_node()
                self.node_manager.append(current)
            self.main_state.node_manager = NodeManager(self.node_manager)
        return self.main_state
