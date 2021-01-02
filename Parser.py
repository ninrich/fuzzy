from Level import Level
from Variable import Variable
from skfuzzy import control as ctrl


class Parser:

    def __init__(self, filename, defuzz_method):
        with open(filename, 'r') as file:
            # remove newline characters
            all_lines = [line.strip() for line in file.readlines()]
            self.rulebase_name = all_lines[0].replace("Rulebase", "")
            # remove empty lines
            self.all_lines = [line for line in all_lines[1:] if len(line) > 0]

        self.defuzz_method = defuzz_method
        self.rules = []
        self.values = {}
        self.variables = {}
        self.antecedents = {}
        self.consequents = {}
        self.parse()

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

        self.parse_values(values)
        self.parse_variables(variables)
        self.parse_rules(rules)

    def parse_rules(self, rules_lines):
        for rule_line in rules_lines:
            antecedents_str, consequent_str = rule_line.replace("(", " ( ").replace(")", " ) ").split(" then ")

            consequent_name, consequent_value = consequent_str.replace(" ( ", "").replace(" ( ", "").split(" is ")
            consequent = self.get_consequent(consequent_name)[consequent_value]

            antecedents_strings = antecedents_str.split()
            string_to_eval = ""
            for index, string in enumerate(antecedents_strings):
                if string == "(" or string == ")":
                    string_to_eval += string
                elif string == "and":
                    string_to_eval += "&"
                elif string == "or":
                    string_to_eval += "|"
                elif string == "is":
                    antecedent_name = antecedents_strings[index - 1]
                    if antecedents_strings[index + 1] == "not":
                        antecedent_value = antecedents_strings[index + 2]
                        antecedent_str = f"~self.get_antecedent('{antecedent_name}')['{antecedent_value}']"
                    else:
                        antecedent_value = antecedents_strings[index + 1]
                        antecedent_str = f"self.get_antecedent('{antecedent_name}')['{antecedent_value}']"
                    string_to_eval += antecedent_str
            self.rules.append(ctrl.Rule(eval(string_to_eval), consequent))

    def parse_values(self, values):
        for line in values:
            operands = line.replace(" ", "").split("=")
            name = operands[0]
            value = operands[1]
            self.values[name] = int(value)

    def parse_variables(self, input):
        current_levels = []
        for line in reversed(input):
            if line.count(" ") > 0:
                words = line.split(" ")
                current_levels.append(Level(*words))
            else:
                variable_name = line
                self.variables[variable_name] = Variable(variable_name, current_levels)
                current_levels = []

    def get_antecedent(self, antecedent_name):
        # create new antecedent if it does not already exist
        if antecedent_name not in self.antecedents:
            self.antecedents[antecedent_name] = self.variables[antecedent_name].create_antecedent()
        return self.antecedents[antecedent_name]

    def get_consequent(self, consequent_name):
        # create new consequent if it does not already exist
        if consequent_name not in self.consequents:
            self.consequents[consequent_name] = self.variables[consequent_name].create_consequent(self.defuzz_method)
        return self.consequents[consequent_name]

    def get_rules(self):
        return self.rules

    def get_values(self):
        return self.values

    def get_all_antecedents(self):
        return self.antecedents.items()

    def get_all_consequents(self):
        return self.consequents.keys()
