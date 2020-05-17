from FuzzyLogicTool import FuzzyLogicTool
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np

power = ctrl.Antecedent(np.arange(50, 500, 1), 'power')
weight = ctrl.Antecedent(np.arange(700, 2700, 1), 'weight')
year = ctrl.Antecedent(np.arange(1970, 2020, 1), 'year')

economy = ctrl.Consequent(np.arange(3, 25, 1), 'economy')

power['low'] = fuzz.trimf(power.universe, [50, 50, 185])
power['medium'] = fuzz.trimf(power.universe, [125, 275, 425])
power['high'] = fuzz.trimf(power.universe, [350, 500, 500])

weight['light'] = fuzz.trimf(weight.universe, [700, 700, 1300])
weight['medium'] = fuzz.trimf(weight.universe, [1100, 1700, 2200])
weight['heavy'] = fuzz.trimf(weight.universe, [2000, 2700, 3700])

year['old'] = fuzz.trimf(year.universe, [1970, 1970, 1985])
year['normal'] = fuzz.trimf(year.universe, [1980, 1998, 2010])
year['new'] = fuzz.trimf(year.universe, [2005, 2020, 2020])

economy['high'] = fuzz.trimf(economy.universe, [3, 3, 8.704])
economy['medium'] = fuzz.trimf(economy.universe, [6.259, 12, 18])
economy['low'] = fuzz.trimf(economy.universe, [16, 25, 25])

rules = [ctrl.Rule(weight['light'] & year['new'], economy['high']),
         ctrl.Rule(power['low'], economy['high']),
         ctrl.Rule(power['medium'] & ~weight['heavy'], economy['medium']),
         ctrl.Rule(power['medium'] & year['normal'], economy['medium']),
         ctrl.Rule(weight['heavy'] & ~year['new'], economy['low']),
         ctrl.Rule(power['high'], economy['low'])]

economy_ctrl = ctrl.ControlSystem(rules)
economy_prediction = ctrl.ControlSystemSimulation(economy_ctrl)

economy_prediction.input['power'] = 275
economy_prediction.input['weight'] = 1700
economy_prediction.input['year'] = 1995

economy_prediction.compute()
print(economy_prediction.output['economy'])
economy.view(sim=economy_prediction)