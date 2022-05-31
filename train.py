import agent as libagent
import sokoban
from tqdm import tqdm
from statistics import mean


def training():

    # --- Initialisation --- #
    game = sokoban.Sokoban(['levels/microban_simple.json'])
    agent = libagent.Agent(input_size=49, epsilon=0.8, decay=0.995, mem=6000)
    saving_weights_each_steps = 1000
    print("\n >>> Begin Epsilon = " + str(agent.epsilon))
    print(" >>> Decay = " + str(agent.decay))

    # -- Old params --
    weights = "test"
    episodes = 200

    list_reward = []
    # -- Episode LOOP -- #
    for i in tqdm(range(episodes)):
        # - Game and Board reset - #
        done = False
        game.nextLevel()
        game.initGrid()
        previous_state = game.computeState(game.grid)
        if i > 90:
            game.paintGrid()
        total = 0

        while not done and game.count_move < 30:
            # fetch all the next possible states.
            possible_future_states = game.futurePossibleStates()
            # print(possible_future_states)
            # if i > 90:
            game.paintGrid()
            # the agent then decide the next action
            action, actual_state = agent.act_train(possible_future_states)

            # Performs the action
            reward, done = game.updateGrid(action)
            total += reward
            print(" Reward = " + str(reward))
            # print(f'done {done}')

            # Saves the move in memory
            agent.fill_memory(previous_state, actual_state, reward, done)

            # Resets iteration for the next move
            previous_state = actual_state

        list_reward.append(total)
        if i % 20 == 0:
            print(f'\nEpisode {i}/{episodes}')
            print(f'Reward: {total}')
            print(f'Average Reward: {mean(list_reward)}')
            print(f'Epsilon: {agent.epsilon}')
            print(f'Decay: {agent.decay}')
            print('\n')
            list_reward = []
        # train the weights of the NN after the episode
        agent.training_montage()

        if i % saving_weights_each_steps == 0:
            agent.save(f"weights_temp_{i}.h5")
    agent.save(f"{weights}.h5")

    print("\n >>> End Epsilon = " + str(agent.epsilon))


if __name__ == "__main__":
    training()