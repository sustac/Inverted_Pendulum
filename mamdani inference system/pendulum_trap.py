import time
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

## Simplified Inverted pendulum from chap 12 Fuzzy Systems in Fuzzy Sets and Fuzzy Logic by Klir,Yuan
## Using mamdani(centroid) defuzz, Trapezoid Membership Functions

## If u uncomment the view statements you will get a visualiztion of the fuzzy numbers in the set



def pendulum(pole,change):

    pole_position = ctrl.Antecedent(np.arange(-90,90,1), 'pole_position')
    rate_of_change = ctrl.Antecedent(np.arange(-90,90,1), 'rate_of_change')
    velocity = ctrl.Consequent(np.arange(-15,16,1), 'velocity')



    pole_position['NL'] = fuzz.trapmf(pole_position.universe, [-90,-90, -80,-65])
    pole_position['NM'] = fuzz.trapmf(pole_position.universe, [-80,-65,-55,-35])
    pole_position['NS'] = fuzz.trapmf(pole_position.universe, [-55,-35,-25,-5])
    pole_position['AZ'] = fuzz.trapmf(pole_position.universe, [-25,-5,5,25])
    pole_position['PS'] = fuzz.trapmf(pole_position.universe, [5,25,35,55])
    pole_position['PM'] = fuzz.trapmf(pole_position.universe, [35,55,65,80])
    pole_position['PL'] = fuzz.trapmf(pole_position.universe, [65,80,90,90])
    

    #pole_position.view()


    rate_of_change['NL'] = fuzz.trapmf(rate_of_change.universe, [-90,-90,-80,-65])
    rate_of_change['NM'] = fuzz.trapmf(rate_of_change.universe, [-80,-65,-55,-35])
    rate_of_change['NS'] = fuzz.trapmf(rate_of_change.universe, [-55,-35, -25, -5])
    rate_of_change['AZ'] = fuzz.trapmf(rate_of_change.universe, [-25, -5,5,25])
    rate_of_change['PS'] = fuzz.trapmf(rate_of_change.universe, [5, 25, 35, 55])
    rate_of_change['PM'] = fuzz.trapmf(rate_of_change.universe, [35, 55, 65, 80])
    rate_of_change['PL'] = fuzz.trapmf(rate_of_change.universe, [65,80, 90, 90])
    

    #rate_of_change.view()


    velocity['NL'] = fuzz.trapmf(velocity.universe, [-15, -15, -15, -11])
    velocity['NM'] = fuzz.trapmf(velocity.universe, [-15,-11, -9, -6])
    velocity['NS'] = fuzz.trapmf(velocity.universe, [-9,-6, -4, -1])
    velocity['AZ'] = fuzz.trapmf(velocity.universe, [-4,-1, 1, 4])
    velocity['PS'] = fuzz.trapmf(velocity.universe, [1, 4, 6, 9])
    velocity['PM'] = fuzz.trapmf(velocity.universe, [6, 9, 11, 15])
    velocity['PL'] = fuzz.trapmf(velocity.universe, [11, 15, 15, 15])

    #velocity.view()

    rule1 = ctrl.Rule(pole_position['NM'] , velocity['NM'])
    rule2 = ctrl.Rule(pole_position['NS'] & rate_of_change['PS'], velocity['AZ'])
    rule3 = ctrl.Rule(pole_position['NS'] & rate_of_change['NS'], velocity['NS'])
    rule4 = ctrl.Rule(pole_position['AZ'] , velocity['AZ'])
    rule5 = ctrl.Rule(pole_position['PS'] & rate_of_change['PS'], velocity['PS'])
    rule6 = ctrl.Rule(pole_position['PS'] & rate_of_change['NS'], velocity['AZ'])
    rule7 = ctrl.Rule(pole_position['PM'] , velocity['PM'])


    pendulum_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
    pendulum_velocity = ctrl.ControlSystemSimulation(pendulum_ctrl)

    
    pendulum_velocity.input['pole_position'] = pole
    pendulum_velocity.input['rate_of_change'] = change

    
    pendulum_velocity.compute()

    true_velocity = pendulum_velocity.output['velocity']

    print(true_velocity)


def main():
    x = 0
  
    while x != 1:
        
        pole = input("enter pole position -180 - 180(degrees): ")
        change = input("enter change -180 - 180(degrees per second): ")
        
        print("velocity is  -15 - 15")
        pendulum(pole,change)

        x = input("enter 0 to continue or 1 to quit: ") 

main()
