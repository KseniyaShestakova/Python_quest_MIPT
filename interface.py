from termcolor import cprint


class Outputer:
    # специальный класс, отвечающий за вывод чего-либо
    def __init__(self):
        pass

    def output_string(self, string_to_output, width, color):
        # предполагается, что слова в строке разделяются пробелами
        string = string_to_output.split(" ")
        counter = 0
        while counter < len(string):
            if len(string[counter]) > width - 4:
                cprint("unable to output message", 'red')
                break
            current_string = ""
            while len(current_string) < width - 4:
                if counter >= len(string):
                    break
                if len(current_string) + len(string[counter]) <= width - 4:
                    current_string += string[counter]
                    if len(current_string) < width - 4:
                        current_string += ' '
                    counter += 1
                else:
                    break
            cprint('| ' + current_string + ' ' * (width - 4 - len(current_string)) + ' |', color)

    def output(self, arr_of_strings, color):
        width = 80
        cprint('-' * width, color)
        for string in arr_of_strings:
            self.output_string(string, width, color)
        cprint('-' * width, color)

    def output_error(self, arr_of_strings):
        self.output(arr_of_strings, 'red')

    def output_location(self, arr_of_strings):
        self.output(arr_of_strings, 'magenta')

    def output_parameters(self, arr_of_strings):
        self.output(arr_of_strings, 'blue')

    def output_choice(self, arr_of_strings):
        self.output(arr_of_strings, 'cyan')

    def output_unaltered(self, string):
        cprint(string, 'yellow', attrs=['underline'])

    def output_tmp(self, string):
        cprint(string, 'green')


class Inputer:
    # класс, занимающийся получением ввода от пользователя
    def __init__(self):
        pass

    def input_(self):
        ret = input()
        return ret
