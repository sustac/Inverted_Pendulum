import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

## Simplified Inverted pendulum from chap 12 Fuzzy Systems in Fuzzy Sets and Fuzzy Logic by Klir,Yuan
## Using mamdani(centroid) defuzz, Triangle Membership Functions

## If u uncomment the view statements you will get a visualiztion of the fuzzy numbers in the set



def pendulum(pole,change):

    pole_position = ctrl.Antecedent(np.arange(-90,90,1), 'pole_position')
    rate_of_change = ctrl.Antecedent(np.arange(-90,90,1), 'rate_of_change')
    velocity = ctrl.Consequent(np.arange(-15,16,1), 'velocity')



    pole_position['NL'] = fuzz.trimf(pole_position.universe, [-90,-90,-60])
    pole_position['NM'] = fuzz.trimf(pole_position.universe, [-90,-60,-30])
    pole_position['NS'] = fuzz.trimf(pole_position.universe, [-60,-30,0])
    pole_position['AZ'] = fuzz.trimf(pole_position.universe, [-30,0,30])
    pole_position['PS'] = fuzz.trimf(pole_position.universe, [0,30,60])
    pole_position['PM'] = fuzz.trimf(pole_position.universe, [30,60,90])
    pole_position['PL'] = fuzz.trimf(pole_position.universe, [60,90,90])
    

    #pole_position.view()


    rate_of_change['NL'] = fuzz.trimf(rate_of_change.universe, [-90,-90,-60])
    rate_of_change['NM'] = fuzz.trimf(rate_of_change.universe, [-90,-60,-30])
    rate_of_change['NS'] = fuzz.trimf(rate_of_change.universe, [-60,-30,0])
    rate_of_change['AZ'] = fuzz.trimf(rate_of_change.universe, [-30,0,30])
    rate_of_change['PS'] = fuzz.trimf(rate_of_change.universe, [0,30,60])
    rate_of_change['PM'] = fuzz.trimf(rate_of_change.universe, [30,60,90])
    rate_of_change['PL'] = fuzz.trimf(rate_of_change.universe, [60,90,90])
    


    #rate_of_change.view()


    velocity['NL'] = fuzz.trimf(velocity.universe, [-15,-15,-10])
    velocity['NM'] = fuzz.trimf(velocity.universe, [-15,-10,-5])
    velocity['NS'] = fuzz.trimf(velocity.universe, [-10,-5,0])
    velocity['AZ'] = fuzz.trimf(velocity.universe, [-5,0,5])
    velocity['PS'] = fuzz.trimf(velocity.universe, [0,5,10])
    velocity['PM'] = fuzz.trimf(velocity.universe, [5,10,15])
    velocity['PL'] = fuzz.trimf(velocity.universe, [10,15,15])

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
