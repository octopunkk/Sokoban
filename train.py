import agent as libagent
import sokoban
import matplotlib.pyplot as plt
from tqdm import tqdm
from statistics import mean


def training():

    # --- Initialisation --- #
    game = sokoban.Sokoban(['levels/microban_simple.json'])
    agent = libagent.Agent(input_size=3, epsilon=0.8, decay=0.9995, mem=2000)
    print("\n >>> Begin Epsilon = " + str(agent.epsilon))
    print(" >>> Decay = " + str(agent.decay))

    # -- Old params --
    weights = "test"
    episodes = 2500
    episode_limit = 30

    list_reward = []
    list_average_reward = []
    list_epsilon = []
    # -- Episode LOOP -- #
    for i in tqdm(range(episodes)):
        # - Game and Board reset - #
        done = False
        game.nextLevel()
        game.initGrid()
        previous_state = game.computeStateDist(game.grid)
        # show the last episodes
        if i > episodes-100:
            game.paintGrid()
        total = 0

        while not done and game.count_move < episode_limit:
            # fetch all the next possible states.
            possible_future_states = game.futurePossibleStates()

            # show the last episodes
            if i > episodes-100:
                game.paintGrid()
            
            # the agent then decide the next action
            action, actual_state = agent.act_train(possible_future_states)

            # Performs the action
            reward, done = game.updateGrid(action)
            total += reward
            if reward == 100 and episode_limit > game.count_move:
                episode_limit = game.count_move + 5

            # Saves the move in memory
            agent.fill_memory(previous_state, actual_state, reward, done)

            # Resets iteration for the next move
            previous_state = actual_state

        list_reward.append(total)
        if i % 50 == 0:
            list_average_reward.append(mean(list_reward))
            list_epsilon.append(i)
            print(f'\nEpisode {i}/{episodes}')
            print(f'Reward: {total}')
            print(f'Average Reward: {list_average_reward[-1]}')
            print(f'Epsilon: {agent.epsilon}')
            print('\n')
            list_reward = []
        
        # train the weights of the NN after the episode
        agent.training_montage()

    # generate the graph
    plt.figure(figsize=(8, 8))
    plt.plot(list_epsilon, list_average_reward, label="Training Accuracy")
    plt.ylim(-35, 80)
    plt.title("Average Reward depending of the episode")
    plt.show()

    # save the weights
    agent.save(f"{weights}.h5")

    print("\n >>> End Epsilon = " + str(agent.epsilon))


if __name__ == "__main__":
    training()
