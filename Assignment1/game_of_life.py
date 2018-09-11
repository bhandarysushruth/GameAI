import argparse 
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation 


ALIVE = 1
DEAD = 0 

## defines a Random Grid to initialize the simulation with a 1:9 ratio of Alive to Dead cells
def randomGrid(N):
	return np.random.choice([ALIVE,DEAD], N*N, p=[0.1, 0.9]).reshape(N, N) 

## creates a glider pattern(the pattern mentioned in Part C point 4)
def pattern(pattern_type, i, j, grid):
	
	if pattern_type == 'glider':

		pattern = np.array([[0, 0, 0, 0, 0],
						[0, 0, 1, 0, 0],
						[0, 0, 0, 1, 0],
						[0, 1, 1, 1, 0],
						[0, 0, 0, 0, 0]])

		grid[i:i+5, j:j+5] = pattern

## checks if the board contains only 0s and 1s and returns a boolean 
def is_valid_board(grid):

	valid = True

	for i in range(N):
		for j in range(N):
			if grid[i,j] != DEAD and grid[i,j]!= ALIVE:
				valid = False
				print ("invalid value : " + str(grid[i,j]))
				break
		if valid ==False:
			break

	return valid

## updates the board and returns the board corresponding to the enxt step
def gol_step(frameNum, img, grid, N): 

	newGrid = grid.copy() 
	for i in range(N): 
		for j in range(N): 
			
			## calculates the total nuber of live neighbors for each cell
			live_neighbors = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + 
								  grid[(i-1)%N, j] + grid[(i+1)%N, j] +
								  grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
								  grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])) 

			## rule 1,2 
			if grid[i, j] == ALIVE: 
				if (live_neighbors < 2) or (live_neighbors > 3): 
					newGrid[i, j] = DEAD 
			## rule 4
			else:
				if live_neighbors == 3: 
					newGrid[i, j] = ALIVE

	 
	img.set_data(newGrid) 
	grid[:] = newGrid[:] 
	
	## checks if the board is valid after the update
	if is_valid_board(grid):
		return img

## takes the array representation of the grid and convers it into an image
def draw_gol_board(grid):
	fig, ax = plt.subplots() 
	img = ax.imshow(grid, interpolation='nearest') 
	img.set_cmap('binary')
	ani = animation.FuncAnimation(fig, gol_step, fargs=(img, grid, N),interval=50)
	plt.show()


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Conway's GOL")
	parser.add_argument('--pattern', dest='initial_pattern', required=False)
	args = parser.parse_args()
	
	N = 100
	grid = np.array([])
	
	if args.initial_pattern == 'glider':
		grid = np.zeros(N*N).reshape(N,N)
		pattern('glider', 0, 0, grid)
	else:
		grid = randomGrid(N) 

	draw_gol_board(grid)
	 


