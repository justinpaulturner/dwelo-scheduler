from random import uniform
from time import sleep

def rand_sleep(minimim=.5,maximum=3):
    sleep(uniform(minimim,maximum))
