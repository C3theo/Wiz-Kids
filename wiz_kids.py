"""
Wiz Kids

Wizarding battle. Players boost up Brain power to cast spells.


"""

import logging
import os
from random import randint, choice

import time

from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement, audio

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


## Handling difficulty
##Threaded Timer/Countdown
##make 'easy' etc a session attribute


##https://softwareengineering.stackexchange.com/questions/182093/why-store-a-function-inside-a-python-dictionary?newreg=f012e0e85d934164ae4726adc4419154
## Math Functions

def add(difficulty):
    'Return an addition problem based off the chosen difficulty.'
    
    if difficulty == 'easy':
        x = randint(0,5)
        y = randint(1,9)
    elif difficulty == 'medium':
        x = randint(10,20)
        y = randint(5,12)
    elif difficulty == 'hard':
        x = randint(20,50)
        y = randint(10,25)
          
    return (x, y), x + y 

def subtract(difficulty):
    'Return a subtraction problem based off the chosen difficulty.'
    
    if difficulty == 'easy':
        x = randint(0,5)
        y = randint(0,9)
        numbers = sorted([x,y])
        difference = numbers[1] - numbers[0]
    elif difficulty == 'medium':
        x = randint(10,20)
        y = randint(5,20)
        numbers = sorted([x,y])
        difference = numbers[1] - numbers[0]
## Answer can be negative
    elif difficulty == 'hard':
        x = randint(20,50)
        y = randint(6,20)
        numbers = [x,y]
        difference = numbers[1] - numbers[0]
        
    return (numbers[1],numbers[0]),difference

def multiply(difficulty):
    'Return a multiplication question based off the chosen difficulty.'
    if difficulty == 'easy':
        x = randint(0,5)
        y = randint(2,9)
    elif difficulty == 'medium':
        x = randint(2,10)
        y = randint(2,5)
    elif difficulty == 'hard':
        x = randint(2,10)
        y = randint(11,20)
    product = x * y
    
    return (x,y),product

def divide(difficulty):
    'Return a division problem based off the chosen difficulty'
    
    if difficulty == 'easy':
        x = randint(1,5)
        y = randint(1,9)
    elif difficulty == 'medium':
        x = randint(5,20)
        y = randint(2,10)
    elif difficulty == 'hard':
        x = randint(20,90)
        y = randint(3,15)
    if y == 0:
        assert("Cannot divide by zero")
    else:
        dividend = x * y
        divisor = choice([x,y])
        quotient =  dividend / divisor
        
    return (dividend,divisor),int(quotient)

def square(difficulty):
    'Return a squared math problem based off the difficulty'

    if difficulty == 'easy':
        x = randint(2,6)
    elif difficulty == 'medium':
        x = randint(6,9)
    elif difficulty == 'hard':
        x = randint(10,15)
        
    return x, x**2
    
def random_Math(difficulty):
    "Return the operation, variables, and answer to a random math question based off the difficulty "
    
    if difficulty == 'easy':
        operation = choice(spell_strength[difficulty]['operations'])
        variables, answer = math_operations[operation](difficulty)
        
    elif difficulty == 'medium':
        operation = choice(spell_strength[difficulty]['operations'])
        variables, answer = math_operations[operation](difficulty)

    elif difficulty == 'hard':
        operation = choice(spell_strength[difficulty]['operations'])
        variables, answer = math_operations[operation](difficulty)

    return operation, variables, answer


## Gameplay Functions

def change_turns():
    'Change player turns.'
    next_turn = [player for player in list(players_dict.keys()) if player != session.attributes['turn']]
    session.attributes['turn'] = next_turn[0]



## Question Dictionaries
    
math_operations = {'add': add,
                   'subtract':subtract,
                   'multiply':multiply,
                   'divide':divide,
                   'square':square}


## used to control different operatons for different difficulties

spell_strength = {'easy':{'operations':list(math_operations.keys())[0:3],
                          'damage':1,
                          'timer':20
                          },
                   'medium':{'operations':list(math_operations.keys())[0:5],
                             'damage':2,
                             'timer':15
                             },
                   'hard':{'operations':list(math_operations.keys()),
                           'damage':3,
                           'timer':10
                           },
                   }

operation_speech = dict(zip(math_operations.keys(),
                           ['plus','minus','times','divided by','squared']))

def ask_question():
    'Return a question prompt '
    operation = session.attributes['math'][0]
    variables = session.attributes['math'][1]
 
    if operation is 'square':
        questionPrompt = ', what is {} {}?'.format(variables, operation_speech[operation] )
    else:
        questionPrompt = ', what is {} {} {}?'.format(variables[0], operation_speech[operation],variables[1])

    return questionPrompt


def check_win():
    'Check whether a player has won or not'
    if session.attributes['players'][PLAYER_ONE]['health'] <= 0:
        session.attributes['win'] = True
        return '{} wins'.format(PLAYER_TWO)
    elif session.attributes['players'][PLAYER_TWO]['health'] <= 0:
        session.attributes['win'] = True
        return '{} wins'.format(PLAYER_ONE)
    else: session.attributes['win'] = False

 ## Alexa

##No Timer at the moment
## Setup game

## Get Player Name and age
## Choose first players turn


players_dict = {"player one":{'health':10}, "player two":{'health':10}}

PLAYER_ONE = list(players_dict.keys())[0]
PLAYER_TWO = list(players_dict.keys())[1]

@ask.launch
def launch():
    "Set up session attributes and either start game or explain game"
    session.attributes['turn'] = choice(list(players_dict.keys()))
    session.attributes['players'] = players_dict
    session.attributes['spell'] = False
    msg = 'Entering the Arcranium. Do you want to play?'.format(session.attributes['turn'])
    return question(msg)


@ask.intent('SetupGameIntent')
def setup_game():
    'Setup session attributes and explain game.'
    
    session.attributes['turn'] = choice(list(players_dict.keys()))
    session.attributes['spell'] = False

    session.attributes['players']
    players_dict = {
          "player1":{'health':10},
          "player2":{'health':10}
          }
##    
    statement('{} goes first'.format(session.attributes['turn']))
    
    cast_spell() #starts game loop

## Ask if player is ready between turns>
@ask.intent("StartYesIntent")
def next_round():
    "Get the random question"
    turn = session.attributes['turn']
    difficulty = 'easy' ## randomize or ask player
## Get random math question
    session.attributes['math'] = random_Math(difficulty)
    session.attributes['damage'] = spell_strength[difficulty]['damage']
    msg1 = ask_question()
    msg2 = turn + msg1
    
    return question(msg2)

@ask.intent('AnswerIntent', convert={'player_answer':int})
def answer(player_answer):
    "Cast or block spell based off the game state and whether answer is correct."

    turn = session.attributes['turn'] ## current player
    right_answer = session.attributes['math'][2]

    winner = check_win()
    if session.attributes['win']:
        return statement(winner)
    
## Block Spell
    if session.attributes['spell'] == True: 
        session.attributes['spell'] = False
        change_turns()
        
        if player_answer == right_answer:        
            blocked_msg = '{} blocks the spell...'.format(session.attributes['turn'])
            blocked_msg2 = '{} are you ready?'.format(session.attributes['turn'])
            msg = blocked_msg + blocked_msg2
            return question(msg)
        
        else:
            blocked_msg = '{} takes {} damage...'.format(session.attributes['turn'], session.attributes['damage'])
            blocked_msg2 = 'Player one has {} health. Player two has {} health'.format(session.attributes['players']['player one']['health'],
                                                                                       session.attributes['players']['player two']['health'])
            blocked_msg3 = '{} are you ready?'.format(session.attributes['turn'])
            msg = blocked_msg +blocked_msg2 + blocked_msg3
            
            return question(msg)
    
 ## Cast Spell
    elif session.attributes['spell'] == False and player_answer == right_answer: 
        session.attributes['spell'] = True
        change_turns() 
        session.attributes['players'][session.attributes['turn']]['health'] = session.attributes['players'][session.attributes['turn']]['health'] - session.attributes['damage']
        msg1 = '{} casts a spell for {} damage to {}...'.format(turn, session.attributes['damage'], session.attributes['turn'])
##        play sound clip
        msg2 = '{} has {} health...'.format(session.attributes['turn'], session.attributes['players'][session.attributes['turn']]['health'])
        msg3 = '{} answer this question to block the spell?'.format(session.attributes['turn'])
        msg = msg1+msg2+msg3 ## use join()
        return question(msg)
 
    else:
        change_turns()
        msg = 'Wrong answer... {} are you ready?'.format(session.attributes['turn'])
        return question(msg) 
    


##@ask.intent('YesExplainGameIntent')
##def explain_game():
##    pass
##    
# Intent for each Player??
##@ask.intent('GetPlayerIntent', mapping= {'age':int})
##def get_player_name(name, age):
##    ## Get both player's name and age
##    
##    msg = "What is {} {} and age ".format(player, name, age)
##    
##    return question(msg)

## Timer for Quiz
##https://stackoverflow.com/questions/2933399/how-to-set-time-limit-on-raw-input
##https://stackoverflow.com/questions/492519/timeout-on-a-function-call



##@ask.intent('AMAZON.HelpIntent')
##def help():
##    help_text = render_template('help')
##    game_reprompt_text = render_template('game_reprompt')
##    return question(help_text).reprompt(list_cities_reprompt_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    msg = 'Leaving the arena.'
    return statement(msg)


##@ask.intent('AMAZON.CancelIntent')
##def cancel():
##    bye_text = render_template('bye')
##    return statement(bye_text)

        
@ask.session_ended
def session_ended():
    return "", 200



if __name__ == '__main__':
##    if 'ASK_VERIFY_REQUESTS' in os.environ:
##        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
##        if verify == 'false':
##            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)



    




        
