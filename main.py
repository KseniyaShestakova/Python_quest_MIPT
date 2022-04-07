from internal_logic import *
from file_parsing import *
import sys

# ожидается ввод типа <name of the file> <path_to_parameters> <path_to_nodes>
# вязанные файлы, указанные в импортах сверху, должны лежать в той же папке
state = parse(sys.argv[1], sys.argv[2])
state.start()
