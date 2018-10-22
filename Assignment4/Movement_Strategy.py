import abc

import math


display_width = 800
display_height = 800

class Movement():
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def move(self):
        """Required Method"""

class MoveDown(Movement):
    def move(self, ghost, wrap=False):
    	
    	angle = 90

    	if (wrap == False) and ((ghost.x > display_width - 20) or (ghost.y >display_height -40)):
    		ghost.vel = 0

    	ghost.x += ghost.vel * math.cos(math.radians(angle))
    	ghost.y += ghost.vel * math.sin(math.radians(angle))

    	if wrap == True:
    		ghost.x %= display_width
    		ghost.y %= display_height


class MoveRight(Movement):
    def move(self, ghost, wrap=False):
    	
    	angle = 0

    	if (wrap == False) and ((ghost.x > display_width - 20) or (ghost.y >display_height -40)):
    		ghost.vel = 0

    	ghost.x += ghost.vel * math.cos(math.radians(angle))
    	ghost.y += ghost.vel * math.sin(math.radians(angle))

    	if wrap == True:
    		ghost.x %= display_width
    		ghost.y %= display_height
        