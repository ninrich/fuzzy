import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
from Level import Level
from Variable import Variable

driving = Variable("Driving",
         [Level("bad", 0, 30, 0, 20),
          Level("average", 50, 50, 20, 20),
          Level("good", 80, 100, 20, 0)]
         )

time = Variable("Journey time",
         [Level("short", 0, 0, 0, 10),
          Level("medium", 10, 10, 5, 5),
          Level("long", 20, 20, 10, 0)]
         )

tip = Variable("Tip",
         [Level("small", 50, 50, 50, 50),
          Level("moderate", 100, 100, 50, 50),
          Level("big", 150, 150, 50, 50)]
         )

"""
driving_ant = ctrl.Antecedent(np.arange(0, 100, 1), 'Driving')
driving_ant['bad'] = fuzz.trapmf(driving_ant.universe, driving_ant['bad'])

service = ctrl.Antecedent(np.arange(0, 11, 1), 'service')
#tip = ctrl.Consequent(np.arange(0, 26, 1), 'tip')

driving_ant['bad'] = fuzz.trapmf(driving_ant.universe, driving['bad'].get_abcd())
driving_ant['average'] = fuzz.trapmf(driving_ant.universe, driving['average'].get_abcd())
driving_ant['good'] = fuzz.trapmf(driving_ant.universe, driving['good'].get_abcd())

journey_time_ant['short'] = fuzz.trapmf(journey_time.universe, journey_time['short'].get_abcd())
journey_time_ant['short'] = fuzz.trapmf(journey_time.universe, journey_time['short'].get_abcd())
journey_time['short'] = fuzz.trapmf(journey_time.universe, journey_time['short'].get_abcd())
# Auto-membership function population is possible with .automf(3, 5, or 7)
# quality.automf(3)
service.automf(3)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
tip['low'] = fuzz.trimf(tip.universe, [0, 0, 13])
tip['medium'] = fuzz.trimf(tip.universe, [0, 13, 25])
tip['high'] = fuzz.trimf(tip.universe, [13, 25, 25])
"""
driving_antecedent = driving.create_antecedent()
time_antecedent = time.create_antecedent()
tip_consequent = tip.create_consequent()

rule1 = ctrl.Rule(driving_antecedent['bad'] | time_antecedent['long'], tip_consequent['small'])
rule2 = ctrl.Rule(driving_antecedent['average'], tip_consequent['moderate'])
rule3 = ctrl.Rule(driving_antecedent['good'] | time_antecedent['short'], tip_consequent['big'])

tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
tipping.input['Driving'] = 65
tipping.input['Journey time'] = 9

# Crunch the numbers
tipping.compute()

print(tipping.output['Tip'])
tip_consequent.view(sim=tipping)
