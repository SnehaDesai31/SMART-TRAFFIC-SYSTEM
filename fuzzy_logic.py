import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

density = ctrl.Antecedent(np.arange(0, 101, 1), 'density')
waiting = ctrl.Antecedent(np.arange(0, 121, 1), 'waiting')
signal = ctrl.Consequent(np.arange(10, 91, 1), 'signal')

density['low'] = fuzz.trimf(density.universe, [0, 0, 40])
density['medium'] = fuzz.trimf(density.universe, [20, 50, 80])
density['high'] = fuzz.trimf(density.universe, [60, 100, 100])

waiting['short'] = fuzz.trimf(waiting.universe, [0, 0, 40])
waiting['medium'] = fuzz.trimf(waiting.universe, [20, 60, 100])
waiting['long'] = fuzz.trimf(waiting.universe, [80, 120, 120])

signal['short'] = fuzz.trimf(signal.universe, [10, 20, 40])
signal['medium'] = fuzz.trimf(signal.universe, [30, 50, 70])
signal['long'] = fuzz.trimf(signal.universe, [60, 80, 90])

rules = [
    ctrl.Rule(density['low'] & waiting['short'], signal['short']),
    ctrl.Rule(density['medium'] & waiting['medium'], signal['medium']),
    ctrl.Rule(density['high'] & waiting['long'], signal['long']),
]

control = ctrl.ControlSystem(rules)

def compute_signal(d, w):
    sim = ctrl.ControlSystemSimulation(control)
    sim.input['density'] = d
    sim.input['waiting'] = w
    sim.compute()
    return round(sim.output['signal'], 2)