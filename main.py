from skfuzzy import control as ctrl
from Parser import Parser

if __name__ == '__main__':
    filename = input("Enter filename:\n")
    defuzz_method = input("Enter defuzzifying method: \n\
        * 'centroid': Centroid of area \n\
        * 'bisector': bisector of area \n\
        * 'mom'     : mean of maximum \n\
        * 'som'     : min of maximum \n\
        * 'lom'     : max of maximum\n")

    parser = Parser(filename, defuzz_method)

    control_system = ctrl.ControlSystem(parser.get_rules())
    simulation = ctrl.ControlSystemSimulation(control_system)
    simulation.inputs(parser.get_values())
    simulation.compute()

    for antecedent in parser.get_all_antecedents():
        antecedent[1].view()

    for consequent_str in parser.get_all_consequents():
        print(f"The calculated value for {consequent_str} is {simulation.output[consequent_str]}.")
        consequent = parser.get_consequent(consequent_str)
        consequent.view(sim=simulation)
