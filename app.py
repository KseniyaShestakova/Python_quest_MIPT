from flask import Flask, render_template, request, jsonify
from internal_logic import *
from file_parsing import *
import sys

# ожидается ввод типа <name of the file> <path_to_parameters> <path_to_nodes>
# вязанные файлы, указанные в импортах сверху, должны лежать в той же папке
parser = Parser()
# state = parser.parse('parameters_study.txt', 'study_quest.txt')
state = parser.parse('rules_parameters.txt', 'rules_quest.txt')

app = Flask(__name__)

counter = 0


@app.route("/", methods=['GET', 'POST'])
def selection():
    global counter
    counter = 0
    if request.method == 'GET':
        state.form_for_unaltered()
        return state.html_string
    if request.method == 'POST':
        return state.html_string


@app.route('/api/', methods=['POST', 'GET'])
def redirecting():
    global state
    global counter
    if counter == 0:
        # когда мы впервые оказались по этому адресу
        counter += 1
        sz = len(state.parameters.unaltered_parameters_name)
        for i in range(sz):
            tmp = request.form[state.parameters.unaltered_parameters_name[i]]
            state.set_unaltered_parameter(i, tmp)
        state.activate_node()
        return state.html_string
    if request.method == 'GET':
        state.activate_node()
        return state.html_string
    if request.method == 'POST':
        for i in range(len(state.next_nodes_outputs)):
            if request.form.get(str(i)) == state.next_nodes_outputs[i]:
                state.node_id = state.next_nodes_ids[i % len(state.next_nodes_outputs)]
    if not state.end_of_the_game:
        state.activate_node()
    return state.html_string





