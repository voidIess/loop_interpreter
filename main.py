import re
import sys


def read_variable(name: str) -> int:
    if name in state:
        return state.get(name)
    else:
        return 0


def write_varible(name, value):
    state[name] = value


def call(pc):
    current_line = lines[pc]
    if re.match("\w+:=\w+[+,-][0-9]+", current_line):
        print("value assignment")
        # get all 3 varying expressions
        rhs = re.sub("\w+:=(\w+)[+,-][0-9]+", "\\1", current_line)
        lhs = re.sub("(\w+):=\w+[+,-][0-9]+", "\\1", current_line)
        summand = int(re.sub("\w+:=\w+([+,-][0-9]+)", "\\1", current_line))

        # do the desired calculation
        write_varible(lhs, max(read_variable(rhs) + summand, 0))


    elif re.match("LOOP \w+ DO", current_line):
        print("LOOP Header")

        inner_limit = pc
        while (lines[inner_limit+1] != "END"):
            inner_limit += 1

        for i in range(pc + 1, inner_limit + 1):
            call(i)

    else:
        print("SyntaxError in line {}:".format(pc))
        print(current_line)
        exit(1)


if __name__ == '__main__':
    # read the file
    with open(sys.argv[1], "r") as file_dc:
        lines = file_dc.read().split("\n")
        file_dc.close()

    # all our variables
    state = {
        "x": 5,
        "y": 3
    }
    print(lines)
    print(state)
    call(0)
    print(state)
