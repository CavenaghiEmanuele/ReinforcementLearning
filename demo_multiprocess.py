import gym
import numpy as np
import matplotlib.pyplot as plt
import operator
from IPython.display import clear_output
from time import sleep
import itertools
from argparse import ArgumentParser as parser
from multiprocessing import Pool
import os

import agents.MonteCarloAgent as MCA



'''
Ogni agente viene allenato per n_games partite oguna di n_episodes episodi
'''
def run_agent(epsilon, n_games, n_episodes):

    i_agent_test_result = []
    policy = MCA.create_random_policy(enviroment)

    agent_info ={
            "policy": policy,
            "state_action_table": MCA.create_state_action_dictionary(enviroment, policy),
            "returns": {}
        }

    '''
    Per ogni partita viene effettuato il training dell'agente e vengono poi eseguite 100
    partite di test per controllare la percentuale di vittorie dell'agente.
    Ogni partita è composta da un numero specificabile di episodi, default=100.
    Al termine di ogni test viene salvato il risultato e al termine di tutte
    le partite viene mostrato il grafico relativo.
    '''
    for _ in range(n_games):

        agent_info = MCA.monte_carlo_control_on_policy(
            enviroment,
            episodes = n_episodes,
            policy = agent_info["policy"],
            state_action_table = agent_info["state_action_table"],
            returns = agent_info["returns"],
            epsilon = epsilon
                        )
        #Test dell'agente
        i_agent_test_result.append(MCA.test_policy(agent_info["policy"], enviroment))

    return i_agent_test_result


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
        n_episodes = 100
    else:
        n_episodes = args.n_episodes[0]


    epsilons = args.epsilons_list
    enviroment = gym.make(args.enviroment_name[0]) #Creazione ambiente

    '''
    Per ogni epsilon specificata nella lista epsilons viene creato un agente diverso
    ognuno con il rispettivo valore del parametro epsilon.
    Ogni agente è inizializzato con una policy random, una state_action_table vuota
    e un dizionario di returns vuoto.
    Ogni agente viene associato ad un processo diverso, il numero di processi è limitato
    al numero di core utilizzabili da python
    '''
    #creo una lista con i parametri degli agenti
    params = zip(
        epsilons,
        [n_games] * len(epsilons),
        [n_episodes] * len(epsilons),
    )

    pool = Pool(len(os.sched_getaffinity(0))) #creo un pool di processi
    results = pool.starmap(run_agent, params) #Ogni agente viene affidato ad un processo

    pool.close()
    pool.join() # attendo che tutti gli agenti abbiano terminato il trining per poi prseguire

    #per ogni agente recupero il risultato dei test
    for agent in range(len(epsilons)):

        #Aggiunta della lista dei risultati al grafico
        plt.plot(results[agent])

    #creo la legenda del grafico, un elemento per ogni agente
    legend = []
    for i in range(len(epsilons)):
        legend.append("epsilon = " + str(epsilons[i]))

    plt.ylabel('% wins')
    plt.xlabel('Number of games (each of ' + str(n_episodes) + " episodes)" )
    plt.legend(legend, loc='upper left')
    plt.show()
