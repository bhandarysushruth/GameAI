from random import randint
from time import clock

#creating a base class 
State = type("State",(object,),{})

class LightOn(State):
	def Execute(self):
		print("Lights On")
## ==================================================================

class LightOff(State):
	def Execute(self):
		print("Lights off")

## ==================================================================

class Transition(object):
	def __init__(self, toState):
		self.toState = toState


	def Execute(self):
		print("Transitioning....")

## ==================================================================

class SimpleFSM(object):
	def __init__(self, char):
		self.char = char
		self.states = {}
		self.transitions = {}
		self.curState = None
		self.trans = None

	def SetState(self, stateName):
		self.curState = self.states[stateName]

	def Transition(self, transName):
		self.trans = self.transitions[transName]

	def Execute(self):
		if(self.trans):
			self.trans.Execute()
			self.SetState(self.trans.toState)
			self.trans = None

		self.curState.Execute()

## ==================================================================

class Char(object):
	def __init__(self):
		self.FSM = SimpleFSM(self)
		self.LightOn = True

## ==================================================================

if __name__ == "__main__":

	light = Char()

	light.FSM.states["On"] = LightOn()
	light.FSM.states["Off"] = LightOff()
	light.FSM.transitions["toOn"] = Transition("On")
	light.FSM.transitions["toOff"] = Transition("Off")

	light.FSM.SetState("On")

	for i in range(20):
		startTime = clock()
		timeInterval = 1

		while (startTime + timeInterval> clock()):
			pass

		if (randint(0,2)):
			if(light.LightOn):
				light.FSM.Transition("toOff")
				light.LightOn = False
			else:
				light.FSM.Transition("toOn")
				light.LightOn = True

		light.FSM.Execute()












