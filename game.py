"""
CONWAY'S GAME OF LIFE
    The Game of Life, also known simply as Life, is a cellular automaton devised by the British mathematician John Horton Conway in 1970.
    The game is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input.
    One interacts with the Game of Life by creating an initial configuration and observing how it evolves.
Rules:
        1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
        2. Any live cell with two or three live neighbors lives on to the next generation.
        3. Any live cell with more than three live neighbors dies, as if by overpopulation.
        4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm

plt.style.use('dark_background')
plt.rcParams['toolbar'] = 'None'


# Set up the initial state of the game
def initialize_game(width, height):
    """
    initialize the game state assigning a random value to each cell in the grid (0 or 1) with a 90% chance of a cell being dead
    :param width: The width of the game board
    :param height: The height of the game board
    :return: The initial state of the game
    """
    game_state = np.random.choice([0, 1], size=(width, height), p=[0.8, 0.2])
    return game_state

# Update the game state based on the rules of Conway's Game of Life
def update_game_state(game_state):
    """
    Update the game state based on the rules of Conway's Game of Life
    :param game_state: The current state of the game
    :return: The updated state of the game expressed as a boolean array (True = alive, False = dead)
    """
    # Count the number of neighbors for each cell in the grid (wrapping around the edges, so that the grid is topologically a torus)
    neighbors_count = sum(np.roll(np.roll(game_state, i, 0), j, 1)
                          for i in (-1, 0, 1) for j in (-1, 0, 1)
                          if (i != 0 or j != 0))
    # Apply the rules of Conway's Game of Life
    # 1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
    # 2. Any live cell with two or three live neighbors lives on to the next generation.
    # 3. Any live cell with more than three live neighbors dies, as if by overpopulation.
    # 4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
    game_state = (neighbors_count == 3) | (game_state & (neighbors_count == 2))

    #create global variable to store the number of live neighbors
    live_neighbors = neighbors_count
    
    return game_state

# Generate the animation frames
def generate_frames(game_state):
    while True:
        yield game_state
        game_state = update_game_state(game_state)

def get_updated_colors(game_state):
    """
    Update the color and transparency of the scatter markers:
    Transparent - dead
    Translucent - alive
    Coloured squares/cells depending on the the number of neighbours
    """

    neighbors_count = sum(np.roll(np.roll(game_state, i, 0), j, 1)
                          for i in (-1, 0, 1) for j in (-1, 0, 1)
                          if (i != 0 or j != 0))

    #compute the colors for each cell to be inferno colored
    cmap = plt.colormaps['inferno']
    rescale = neighbors_count / 8  # Maximum of 8 neighbors
    colors = [cmap(neighbors) for neighbors in rescale.flatten()]
    #extract the colors for the live cells
    colors = [color for color, is_live in zip(colors, game_state.flatten()) if is_live]

    return colors

# Create the animation
def create_animation(game_state):
    #define figure and axis
    fig, ax = plt.subplots()
    # hide the axes
    ax.set_axis_off()
    #avoid autoscaling
    # ax.set_xlim(-5, 55)
    # ax.set_ylim(-5, 55)

    #set the size in pixels to be 1920x1080
    fig.set_size_inches(19.20, 10.80)
    #set aspect to be equal
    ax.set_aspect('equal')


    def update(frame):
        """
        Update the animation
        :param frame: The current frame of the animation
        :return: The updated scatter plot
        """
        #clear the plot but not the axis
        ax.clear()
        ax.set_axis_off()
        # ax.set_xlim(-5, 55)
        # ax.set_ylim(-5, 55)
        ax.set_aspect('equal')

        #update the game state


        #get the updated colors
        colors = get_updated_colors(frame)
        scatter = ax.scatter(np.where(frame)[0], np.where(frame)[1], color=colors, s=70)
        return scatter

    #arguments are: figure, update function, frames (the input to the update function), interval (the delay between frames in milliseconds)
    anim = animation.FuncAnimation(fig, update, frames=generate_frames(game_state), interval=100)
    plt.show()

# Main function
def main():
    width = 200
    height = 100
    game_state = initialize_game(width, height)
    create_animation(game_state)

if __name__ == '__main__':
    main()
