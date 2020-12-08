from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np


class Variable:
    def __init__(self, name, levels=None):
        if levels is None:
            levels = []
        self.name = name
        self.levels = levels

    def add_level(self, level):
        self.levels.append(level)

    def create_antecedent(self):
        graph_min_value = 0
        graph_max_value = self.get_maximum_value()
        graph_step = 1
        antecedent = ctrl.Antecedent(np.arange(graph_min_value, graph_max_value, graph_step), self.name)
        for level in self.levels:
            name = level.get_name()
            antecedent[name] = fuzz.trapmf(antecedent.universe, level.get_abcd())
        return antecedent

    def create_consequent(self):
        graph_min_value = 0
        graph_max_value = self.get_maximum_value()
        graph_step = 1
        consequent = ctrl.Consequent(np.arange(graph_min_value, graph_max_value, graph_step), self.name)
        for level in self.levels:
            name = level.get_name()
            consequent[name] = fuzz.trapmf(consequent.universe, level.get_abcd())
        return consequent

    def get_maximum_value(self):
        """
        Returns the maximum value of all levels. Useful for determining the scale of the grapgh
        """
        current_max = 0
        for level in self.levels:
            current_max = level.get_maximum_value() if level.get_maximum_value() > current_max else current_max
        return current_max
