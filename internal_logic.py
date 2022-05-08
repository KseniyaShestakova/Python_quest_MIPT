import random


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
    html_string = ""
    classical_beginning = '''
<!DOCTYPE HTML>

<HTML>
	<head>
		<title>Beautiful page</title>
		<meta http-equiv="content-type" content="text/HTML" charset="UTF-8"/>
	</head>
	<body style="background-color: #eaaf9d">
	<center>
'''
    classical_end = '''
    </center>
	</body>
</HTML>
'''

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
        try:
            self.flag = (self.flag and int(self.parameters.get_unaltered(parameter_id)) > val)
        except ValueError:
            self.flag = False

    def less_unaltered(self, parameter_id, val):
        try:
            self.flag = (self.flag and int(self.parameters.get_unaltered(parameter_id)) < val)
        except ValueError:
            self.flag = False

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
        self.html_string += '\n' + "<div style=\"border: 5px solid #f38b58; background-color: #f5e2a7\">"
        self.html_string += '\n' + "<p>Current characteristics: </p>"
        for i in range(len(self.parameters.parameter_value)):
            self.html_string += ('\n' + "<p>" + self.parameters.get_name(i) + ": " + str(self.parameters.get(i)) + "</p>")
        self.html_string += '\n' + "</div>"

    def perform_selection(self):
        self.html_string += '\n' + "<form method=\"post\" action=\"/api/\" style=\"\">"
        for i in range(len(self.next_nodes_outputs)):
            self.html_string += "<p>\n</p>"
            self.html_string += "<input type=\"submit\" value=\"" + self.next_nodes_outputs[i] + \
                                "\" name=\"" + str(i) + "\" style=\"height:50px; font-size:25px; \
                                                        background-color: #ef844e; \
                                                        border: none\
                                                        -webkit-border-radius: 20px; \
                                                        border-radius: 20px\"/>"

    def activate_node(self):
        current_node = self.node_manager.get_node_by_id(self.node_id)
        self.html_string = ""
        self.html_string += self.classical_beginning

        for i in range(len(current_node.presentation)):
            self.html_string += ('\n' + "<div style=\"background-color: #ef844e; font-size: 30px; \
                                        border: 5px solid #ef6722\" \
                                        >" + current_node.presentation[i] + "</div>")

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

        self.html_string += ('\n' + self.classical_end)

    def form_for_unaltered(self):
        self.html_string = '''<HTML>
	<head>
		<title>Beautiful page</title>
		<meta http-equiv="content-type" content="text/HTML" charset="UTF-8"/>
	</head>
<body style="background-color: paleturquoise">
<center>
     <form method = 'POST' action = '/api/' size=\"100\">'''
        for i in range(len(self.parameters.unaltered_parameters_name)):
            self.html_string += '\n' + "<label style=\"font-size:25px\" for=\"" + self.parameters.get_unaltered_name(i) + \
                                "\">" + self.parameters.get_unaltered_name(i) + "</label><br>"
            self.html_string += '\n' + "<input type=\"text\" id=\"" + self.parameters.get_unaltered_name(i) + \
                                "\" name=\"" + self.parameters.get_unaltered_name(i) + \
                                "\" style=\"height:40px; width:500px; font-size:25px\"" + "\"><br>"
        self.html_string += '''
        <input type="submit" value="Submit" style="height:50px; width:100px; font-size:25px;
         background-color: lightskyblue; color: darkslateblue">
</form>
</center>
</body>'''





