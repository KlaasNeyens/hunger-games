from random import randint

class Player:
    def __init__(self):
        self.food = 0
        self.reputation = 0

    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
		# The main routine that plays each individual round.

		# You must create an array of variables 'hunt_decisions' and assign an 'h' for hunt or
		# an 's' for slack (i.e., not hunt) to each member of the array; the order of the hunt
		# decisions in hunt_decisions should correspond to the order of opponents'
		# reputations in player_reputations.

		# Blank variables or errors will be assigned 's'.

		# The variables passed in to hunt_choices for your use are:
		#     round_number: integer, the number round you are in.
		#     current_food: integer, the amount of food you have.
		#     current_reputation: float (python's representation of real numbers), your current reputation.
		#     m: integer, the threshold cooperation/hunting value for this round.
		#     player_reputations: list of floats, the reputations of all the remaining players in the game.
		#                         The ordinal positions of players in this list will be randomized each round.		
		
		hunt_decisions = []
		for p in player_reputations:
			if randint(0, 1) == 1:
				hunt_decisions.append('h')
			else:
				hunt_decisions.append('s')
		return hunt_decisions

    def hunt_outcomes(self, food_earnings):
		# hunt_outcomes is called after all hunts for the round are complete.

		# The variable passed in to hunt_outcomes for your use is:
		#     food_earnings: list of integers, the amount of food earned from the last round's hunts.
		#                    The entries can be negative as it is possible to lose food from a hunt.
		#                    The amount of food you have for the next round will be current_food
		#                    + sum of all entries of food_earnings + award from round_end.
		#                    The list will be in the same order as the decisions you made in that round.
		pass

    def round_end(self, award, m, number_hunters):
		# round_end is called after all hunts for the round are complete.

		# award - the total amount of food you received due to cooperation in the round.
		# Can be zero if the threshold m was not reached.

		# The variables passed in to round_end for your use are:
		#     award: integer, total food bonus (can be zero) you received due to players cooperating
		#            during the last round. The amount of food you have for the next round will be
		#            current_food (including food_earnings from hunt_outcomes this round) + award.
		#     number_hunters: integer, number of times players chose to hunt in the last round.
		pass

class Hunter(Player):
    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
        hunt_decisions = ['h' for x in player_reputations]
        return hunt_decisions

class Slacker(Player):
    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
        hunt_decisions = ['s' for x in player_reputations]
        return hunt_decisions

class Hermit(Player):
	# Likes to be with to be in the smallest group
	def __init__(self):
		self.num_players = 0
		self.num_hunted = 1
		self.last_hunts = 0

	def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
		if self.num_players * self.num_players / 2 >= (self.num_hunted - self.last_hunts):
			hunt_decisions = ['h' for x in player_reputations]
			self.last_hunts = len(hunt_decisions)
		else:
			hunt_decisions = ['s' for x in player_reputations]
			self.last_hunts = 0
			
		self.num_players = len(player_reputations)
		return hunt_decisions

	def round_end(self, award, m, number_hunters):
		self.num_hunted = number_hunters

class Socialite(Player):
	# Likes to be with to be in the largest group
	def __init__(self):
		self.num_players = 0
		self.num_hunted = 1
		self.last_hunts = 0

	def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
		if self.num_players * self.num_players / 2 < (self.num_hunted - self.last_hunts):
			hunt_decisions = ['h' for x in player_reputations]
			self.last_hunts = len(hunt_decisions)
		else:
			hunt_decisions = ['s' for x in player_reputations]
			self.last_hunts = 0
			
		self.num_players = len(player_reputations)
		return hunt_decisions

	def round_end(self, award, m, number_hunters):
		self.num_hunted = number_hunters
		
class MostlySlacker(Player):
    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
		hunt_decisions = []
		for p in player_reputations:
			if randint(0, 2) == 1:
				hunt_decisions.append('h')
			else:
				hunt_decisions.append('s')
		return hunt_decisions

class MostlyHunter(Player):
    def hunt_choices(self, round_number, current_food, current_reputation, m, player_reputations):
		hunt_decisions = []
		for p in player_reputations:
			if randint(0, 2) != 1:
				hunt_decisions.append('h')
			else:
				hunt_decisions.append('s')
		return hunt_decisions


# players used as list of contestants by test simulator to run game
players = [
	Player(), 
	Hunter(), 
	Slacker(),
	Hermit(),
	Socialite(),
	MostlySlacker(),
	MostlyHunter()
]