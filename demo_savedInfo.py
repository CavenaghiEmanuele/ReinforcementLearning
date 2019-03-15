import gym
import numpy as np
import matplotlib.pyplot as plt
import operator
from IPython.display import clear_output
from time import sleep
import itertools
from argparse import ArgumentParser as parser

import agents.MonteCarloAgentWithSavedInfo as MCA


if __name__ == '__main__':

    parser = parser(prog='Demo', description='demo for agent')
    parser.add_argument('-n_g', '--n_games', metavar='n_games', type=int, nargs=1, help='Number of games')
    parser.add_argument('-n_e', '--n_episodes', metavar='n_episodes', type=int, nargs=1, help='Number of episodes for each game')
    parser.add_argument('-e_l', '--epsilons_list', metavar='epsilons_list', type=float, nargs="*", default=[0.01], help='Epsilons value for agents (one for each agent)')
    parser.add_argument('-e', '--enviroment_name', metavar='enviroment_name', type=str, nargs=1, required=True, help='Enviroment name')


    args = parser.parse_args()

    if not args.n_games:
        n_games = 100
    else:
        n_games = args.n_games[0]

    if not args.n_episodes:
        n_episodes = 1000
    else:
        n_episodes = args.n_episodes[0]


    epsilons = args.epsilons_list
    tests_result = np.zeros((len(epsilons), n_games)) #Creazione della matrice dei risultati
    enviroment = gym.make(args.enviroment_name[0]) #Creazione ambiente

    '''
    Per ogni epsilon specificata nella lista epsilons viene creato un agente diverso
    ognuno con il rispettivo valore del parametro epsilon.
    Ogni agente è inizializzato con una policy random, una state_action_table vuota
    e un dizionario di returns vuoto.
    '''
    for agent in range(len(epsilons)):

        dict_result = MCA.policy_iterator(
            enviroment,
            n_games,
            n_episodes,
            epsilon = epsilons[agent]
            )

        tests_result = dict_result["tests_result"]

        plt.plot(tests_result)



    legend = []
    for i in range(len(epsilons)):
        legend.append("epsilon = " + str(epsilons[i]))

    plt.ylabel('% wins')
    plt.xlabel('Number of games (each of ' + str(n_episodes) + " episodes)" )
    plt.legend(legend, loc='upper left')
    plt.show()
