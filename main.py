import re
import sys


def read_variable(name: str) -> int:
    if name in state:
        return state.get(name)
    else:
        return 0


def write_variable(name, value):
    state[name] = value

def parse_variable(expression:str):
    if re.match("\w+=[0-9]+", expression):
        name = re.sub("(\w+)=[0-9]+","\\1", expression)
        value = int(re.sub("\w+=([0-9]+)","\\1", expression))
        write_variable(name, value)
    else:
        print("Invalid Argument: {}".format(expression))
        exit(1)


def call(pc) -> int:
    current_line = lines[pc]
    if re.match("\w+:=\w+[+,-][0-9]+", current_line):
        # get all 3 varying expressions
        rhs = re.sub("\w+:=(\w+)[+,-][0-9]+", "\\1", current_line)
        lhs = re.sub("(\w+):=\w+[+,-][0-9]+", "\\1", current_line)
        summand = int(re.sub("\w+:=\w+([+,-][0-9]+)", "\\1", current_line))

        # do the desired calculation
        write_variable(lhs, max(read_variable(rhs) + summand, 0))
        return pc + 1


    elif re.match("LOOP \w+ DO", current_line):
        repetitions = read_variable(re.sub("LOOP (\w+) DO", "\\1", current_line))

        inner_limit = pc
        while (lines[inner_limit] != "END"):
            inner_limit += 1

        # execute the inner commands 'repetitions' times
        for i in range(repetitions):
            next_instruction = pc + 1
            while (lines[next_instruction] != "END"):
                next_instruction = call(next_instruction)

        # return after the "END" statement
        return inner_limit + 1


    else:
        print("SyntaxError in line {}:".format(pc))
        print(current_line)
        exit(1)


if __name__ == '__main__':
    # read the file
    with open(sys.argv[1], "r") as file_dc:
        lines = file_dc.read().split("\n")
        file_dc.close()

    # remove tabs and spaces before the lines and empty lines
    lines = filter((lambda x: x != '') ,lines)
    lines = list(map((lambda x: re.sub("^[ ,\t]*(.*)$", "\\1", x)), lines))
    print(lines)

    # initialise all variables
    state = {}
    for i in range(2, len(sys.argv)):
        parse_variable(sys.argv[i])

    program_length = len(lines)
    next_instruction = 0
    while (next_instruction < program_length):
        next_instruction = call(next_instruction)

    print("Result: {}".format(read_variable("z")))