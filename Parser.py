from Level import Level
from Variable import Variable


class Parser:

    def __init__(self, filename):
        with open(filename, 'r') as file:
            # remove newline characters
            all_lines = [line.strip() for line in file.readlines()]
            self.rulebase_name = all_lines[0].replace("Rulebase", "")
            # remove empty lines
            self.all_lines = [line for line in all_lines[1:] if len(line) > 0]

        self.rules = []
        self.values = {}
        self.variables = []

    def parse(self):
        rules = []
        values = []
        variables = []
        for index, line in enumerate(self.all_lines):
            if ":" in line:
                rules.append(line)
            elif "=" in line:
                values.append(line)
            else:
                variables.append(line)
        
        self.parse_rules(rules)
        self.parse_values(values)
        self.parse_variables(variables)
        print("fajne")
        
    def parse_rules(self, rules):
        pass

    def parse_values(self, values):
        for line in values:
            operands = line.replace(" ", "").split("=")
            name = operands[0]
            value = operands[1]
            self.values[name] = int(value)
        print(self.values)

    def parse_variables(self, input):
        current_levels = []
        for line in reversed(input):
            if line.count(" ") > 0:
                words = line.split(" ")
                current_levels.append(Level(*words))
            else:
                variable_name = line
                self.variables.append(Variable(variable_name, current_levels))
                current_levels = []


    def parse_levels(self, level_line):
        level_line.split()

if __name__ == '__main__':
    Parser("example.txt").parse()
