import pygame

#---------- GLOBAL VARIABLES
STEP_SIZE = 50
WINDOW_WIDTH = 1110
WINDOW_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WINDOW_SIZE = [WINDOW_WIDTH, WINDOW_HEIGHT]
POTS_WALL = "potswall.png"
POTS_EXTENSION = "potsextension.png"
KNIFE_WALL = "knifewall.png"
EXTINGUISHER_WALL = "extinguisherwall.png"
INGREDIENTS_WALL = "ingredientswall.png"
PLATES_WALL = "plateswall.png"

#---------- PYGAME INITIALIZATION
pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
background = pygame.image.load("kitchen.png")
pygame.display.set_caption("Homework 6-3")
done = False
clock = pygame.time.Clock()

#---------- DELCARING GAME OBJECT CLASSES

class Player(pygame.sprite.Sprite):
    """ This class represents the main character of the game """

    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()

        # Set height, width, and image
        self.image = pygame.Surface([STEP_SIZE, STEP_SIZE])
        self.image.fill(WHITE)
        self.image = pygame.image.load("unicorn.png")
        self.image = pygame.transform.scale(self.image, (STEP_SIZE, STEP_SIZE))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None

    def draw(self, surface, image):
        """Function draws the player"""
        surface.blit(image, (self.rect.x, self.rect.y))

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            # else:
                # Otherwise if we are moving left, do the opposite.
                # self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            # else:
            #     self.rect.top = block.rect.bottom

    def seek(self, dx, dy):
        """ Continually update the players position to get closer to target. """

        if dx > self.rect.x:    # If the player is to the right of the target, increase x
            self.change_x = 1

        if dx < self.rect.x:    # If the player is to the left of the target, decrease x
            self.change_x = -1

        if dy < self.rect.y:    # If the player is under the target, decrease y
            self.change_y = -1

        if dy > self.rect.y:    # If the player is above the target, increase x
            self.change_y = 1

        # If we're close enough to our target, set our coordinates to the exact ones targeted
        if dx - 10 <= self.rect.x <= dx + 10 and dy - 10 <= self.rect.y <= dy + 10:
            self.rect.x = dx
            self.rect.y = dy


class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """

    def __init__(self, x, y, width, height, image):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()

        # Make a wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load(image)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


#---------- GOAP FUNCTIONS
def satisfies_goal(goal, state):
    """
    Checks if the given goal is satisfied by the given world state.
    """
    for key, value in goal.items():
        try:
            if state[key] != value:
                return False
        except KeyError:
            return False

    return True


def update_state(state, effect):
    """
    Returns the given state updated by the desired effect.
    """
    state = dict(state)
    state.update(effect)
    return state


def plan(goal, state, actions, max_plan_length=10):
    """
    Returns the sequence of lowest cost actions that need to be taken to satisfy the given goal.
    """
    # Avoid infinite recursion
    if max_plan_length <= 0:
        return

    current_cost = float('inf')
    current_plan = None

    # If the state already satisfies the goal, then no action is required
    if satisfies_goal(goal, state):
        return [], 0.

    # Do a DFS search of the planning tree
    for a in actions:
        # If we do not have the prerequisites for this action, continue
        if not satisfies_goal(a.preRequisite, state):
            continue

        # Computes the new path recursively
        new_plan = plan(goal,
                        update_state(state, a.effect), actions,
                        max_plan_length - 1)

        # If we found a plan and it is cheaper than the current cost, then pick it
        if new_plan is not None:
            new_plan, new_cost = new_plan
            if a.cost + new_cost < current_cost:
                current_plan = [a] + new_plan
                current_cost = a.cost + new_cost

    return current_plan, current_cost


#---------- CREATE GAME LEVEL
all_sprite_list = pygame.sprite.Group()

# Make the walls. (x_pos, y_pos, width, height, image)
wall_list = pygame.sprite.Group()

wall = Wall(89, 231, 331, 46, POTS_WALL)   # Wall with pots
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(8, 500, 403, 69, KNIFE_WALL)    # Wall with knives
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(593, 233, 278, 57, EXTINGUISHER_WALL)  # Wall with fire extinguisher
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(605, 500, 425, 65, INGREDIENTS_WALL)  # Wall with ingredients
wall_list.add(wall)
all_sprite_list.add(wall)

player = Player(470, 180)
player.walls = wall_list

all_sprite_list.add(player)

ticktock = 0

#---------- GAME MAIN
if __name__ == '__main__':
    class GetTomato:
        x = 680
        y = 455
        image = pygame.image.load("unicorntomato.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Get Tomato"

        preRequisite = {}
        effect = {'hasTomato': True}
        cost = 1.

    class GetOnion:
        x = 815
        y = 455
        image = pygame.image.load("unicornonion.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Get Onion"

        preRequisite = {}
        effect = {'hasOnion': True}
        cost = 1.

    class GetKnife:
        x = 290
        y = 450
        image = pygame.image.load("unicornknife.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Get Knife"

        preRequisite = {}
        effect = {'hasKnife': True}
        cost = 1.

    class CutTomato:
        x = 290
        y = 450
        image = pygame.image.load("unicornchoppedtomato.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Cut Tomato"

        preRequisite = {'hasKnife': True, 'hasTomato': True}
        effect = {'choppedTomato': True}
        cost = 2.

    class CutOnion:
        x = 290
        y = 450
        image = pygame.image.load("unicornchoppedonion.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Cut Onion"

        preRequisite = {'hasKnife': True, 'hasOnion': True}
        effect = {'choppedOnion': True}
        cost = 4.

    class SearchPantry:
        x = 825
        y = 300
        image = pygame.image.load("unicornchoppedonion.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Search Pantry"

        preRequisite = {}
        effect = {'choppedOnion': True}
        cost = 2.

    class MakeTomatoSoup:
        x = 200
        y = 300
        image = pygame.image.load("unicorntomatosoup.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Make Tomato Soup"

        preRequisite = {'choppedTomato': True}
        effect = {'madeTomatoSoup': True}
        cost = 3.

    class MakeOnionSoup:
        x = 200
        y = 300
        image = pygame.image.load("unicornonionsoup.png")
        image = pygame.transform.scale(image, (STEP_SIZE, STEP_SIZE))
        name = "Make Onion Soup"

        preRequisite = {'choppedOnion': True}
        effect = {'madeOnionSoup': True}
        cost = 3.

    # TOMATO SOUP
    goal = {'madeTomatoSoup': True}
    state = {'hasKnife': False, 'hasTomato': False, 'choppedTomato': False, 'madeTomatoSoup': False}
    possible_actions = [GetTomato, GetKnife, CutTomato, MakeTomatoSoup]

    tomatoPlan, tomatoCost = plan(goal, state, possible_actions)

    # Carry out plan sequence according to GOAP algorithm
    for action in tomatoPlan:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(BLACK)
            screen.blit(background, (0, 0))
            all_sprite_list.draw(screen)

            displaytext = "GOAL: Make tomato soup; ACTION: " + action.name
            myfont = pygame.font.SysFont('arial', 20)
            textsurface = myfont.render(displaytext, False, WHITE)
            screen.blit(textsurface, (0, 0))

            # To demonstrate seek behaviour
            player.seek(action.x, action.y)
            # If we have reached the action point, break
            if player.rect.x == action.x and player.rect.y == action.y:
                # Set the sprite to have the updated image of the action completed
                player.image = action.image
                break
            player.update()

            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

    # Reset states
    goal.clear()
    state.clear()
    del possible_actions[:]
    player.image = pygame.image.load("unicorn.png")
    player.image = pygame.transform.scale(player.image, (STEP_SIZE, STEP_SIZE))

    # ONION SOUP
    goal = {'madeOnionSoup': True}
    state = {'hasKnife': False, 'hasOnion': False, 'choppedOnion': False, 'madeOnionSoup': False}
    possible_actions = [GetOnion, GetKnife, CutOnion, SearchPantry, MakeOnionSoup]

    onionPlan, onionCost = plan(goal, state, possible_actions)

    # Carry out plan sequence according to GOAP algorithm
    for action in onionPlan:
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill(BLACK)
            screen.blit(background, (0, 0))
            all_sprite_list.draw(screen)
            displaytext = "GOAL: Make onion soup; ACTION: " + action.name
            myfont = pygame.font.SysFont('arial', 20)
            textsurface = myfont.render(displaytext, False, WHITE)
            screen.blit(textsurface, (0, 0))

            # To demonstrate seek behaviour
            player.seek(action.x, action.y)
            # If we have reached the action point, break
            if player.rect.x == action.x and player.rect.y == action.y:
                # Set the sprite to have the updated image of the action completed
                player.image = action.image
                break
            player.update()

            clock.tick(60)

            # Go ahead and update the screen with what we've drawn.
            pygame.display.flip()