import agent as libagent
import sokoban
from tqdm import tqdm

def training():
    
    # --- Initialisation --- #
    game = sokoban.Sokoban(['levels/microban_0.json', 'levels/microban_1.json'])
    agent = libagent.Agent(input_size=49, decay=0.9995)
    saving_weights_each_steps = 1000
    print("\n >>> Begin Epsilon = " + str(agent.epsilon))
    print(" >>> Decay = " + str(agent.decay))

    # -- Old params --
    weights = "test"
    episodes = 10
    
    # -- Episode LOOP -- #
    for i in tqdm(range(episodes)):
        # - Game and Board reset - #
        done = False
        game.nextLevel()
        game.initGrid()
        previous_state = game.computeState()

        while not done:
            # fetch all the next possible states.
            possible_future_states = game.futurePossibleStates()
            # the agent then decide the next action
            action, actual_state = agent.act_train(possible_future_states)

            # Performs the action
            reward, done = game.updateGrid(action)

            # Saves the move in memory
            agent.fill_memory(previous_state, actual_state, reward, done)

            # Resets iteration for the next move
            previous_state = actual_state

        # train the weights of the NN after the episode
        agent.training_montage()

        if i % saving_weights_each_steps == 0:
            agent.save(f"weights_temp_{i}.h5")
    agent.save(f"{weights}.h5")

    print("\n >>> End Epsilon = " + str(agent.epsilon))


if __name__ == "__main__":
    training()