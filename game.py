"""
Test simulator for Hunger Games brilliant.org competition

https://brilliant.org/competitions/hunger-games/
	
"""

import random
from random import randint
from players import players as players_AI
	
class Player:
	def __init__(self, food, AI):
		self.food = food
		self.AI = AI

		self.hunts = 0
		self.slacks = 0
		self.reputation = 0.0
		self.hunt_decisions = None
		self.exit_round = 0
	
	def __unicode__(self):
		return self.AI.__class__.__name__

	def __str__(self):
		return self.AI.__class__.__name__

class Debugger:
	def __init__(self, enabled=True, round_interval=100, decisions=False, player_out=True):
		self.enabled = enabled
		self.round_interval = round_interval
		self.decisions = decisions
		self.player_out = player_out
	
	def print_start_game(self, num_players, start_food):
		if self.enabled:
			print 'Num players', len(players_AI)
			print 'Start food', start_food
	
	def print_start_round(self, game_round):
		if self.enabled and game_round % self.round_interval == 0:
			print 'Round', game_round

	def print_decisions(self, decisions):
		if self.enabled and self.decisions:
			for d in decisions:
				print d

	def print_player(self, player, game_round):
		if self.enabled and game_round % self.round_interval == 0:
			print '{0} hunts = {1} slacks = {2} rep = {3} food = {4}'.format(
				player, player.hunts, player.slacks, player.reputation, 
				player.food)

	def print_player_out(self, player, game_round):
		if self.enabled and self.player_out:
			print 'Out!', player, 'round', game_round

def get_hunt_decisions(players, extra_food_threshold, game_round):
	# Format: hunt_decisions[player][opponent]
	# Player used as placeholder in decision matrix for player == opponent
	hunt_decisions = []
	for player in players:
		# Build list of other players's reputations
		player_reputations = []
		index = 0
		current_index = None
		for opponent in players:
			if opponent != player:
				player_reputations.append(opponent.reputation)
			else:
				current_index = index
			index += 1
		
		current_decisions = player.AI.hunt_choices(
			game_round, 
			player.food, 
			player.reputation, 
			extra_food_threshold, 
			player_reputations
		)
		current_decisions.insert(current_index, player.AI.__class__.__name__)
		hunt_decisions.append(current_decisions)
	return hunt_decisions

def get_hunt_food(p_decision, opp_decision):
	food = None
	if p_decision == 'h' and opp_decision == 'h':
		food = (6 + 6) / 2 - 6 # 0
	elif p_decision == 'h' and opp_decision == 's':
		food = (6 + 0) / 2 - 6 # -3
	elif p_decision == 's' and opp_decision == 'h':
		food = (0 + 6) / 2 - 2 # 1
	elif p_decision == 's' and opp_decision == 's':
		food = (0 + 0) / 2 - 2 # -2
	else:
		# Invalid decisions are technically 's', but this is for testing purposes
		print 'ERROR: unknown decisions', p_decision, opp_decision
	return food

def players_round_end(players, extra_food_threshold, total_hunters):
	extra_food = 0
	if total_hunters >= extra_food_threshold:
		extra_food = 2 * (len(players) - 1)
	
	for player in players:
		player.food += extra_food
		player.AI.round_end(extra_food, extra_food_threshold, total_hunters)

def remove_hungry_players(players, game_round):
	removed = []
	for player in players:
		if player.food <= 0:
			removed.append(player)
	for player in removed:
		players.remove(player)
		player.exit_round = game_round
		debugger.print_player_out(player, game_round)
	return removed

def run_game():
	start_num_players = len(players_AI)
	start_food = 300 * (start_num_players - 1)
	debugger.print_start_game(start_num_players, start_food)
	
	players = [Player(start_food, AI) for AI in players_AI]
	
	losers = []
	for game_round in range(1, max_game_rounds):
		debugger.print_start_round(game_round)

		num_players = len(players)
		extra_food_threshold = randint(0, num_players * (num_players - 1))
		random.shuffle(players)
	
		hunt_decisions = get_hunt_decisions(
			players, 
			extra_food_threshold,
			game_round
		)	
		debugger.print_decisions(hunt_decisions)

		# Process hunting decisions
		total_hunters = 0
		for p_index in range(num_players):
			player = players[p_index]
			hunts = 0
			slacks = 0
			food_earnings = []
			for opp_index in range(num_players):
				if p_index != opp_index:
					decision = hunt_decisions[p_index][opp_index]
					food = get_hunt_food(decision, hunt_decisions[opp_index][p_index])
					food_earnings.append(food)
					if decision == 'h':
						total_hunters += 1
						hunts += 1
					elif decision == 's':
						slacks += 1
			player.food += sum(food_earnings)
			player.hunts += hunts
			player.slacks += slacks
			player.reputation = player.hunts / float(player.hunts + player.slacks)
			debugger.print_player(player, game_round)

			player.AI.hunt_outcomes(food_earnings)

		players_round_end(players, extra_food_threshold, total_hunters)
		losers.extend(remove_hungry_players(players, game_round))

		if len(players) < 2:
			break
	
	# TODO: Determine winner if remaining players go out in last round
	# NOTE: If the last N players all die in the same round or 
	# N players have the same food at the end of the game, then 
	# reputation will be used as the tiebreaker, with the highest 
	# reputation winning.
	
	if players:
		print '\nWinners'
		for player in sorted(players, key=lambda player: player.food, reverse=True):
			print '{0} hunts = {1} slacks = {2} rep = {3} food = {4}'.format(
				player, player.hunts, player.slacks, player.reputation, 
				player.food)
	print '\nLosers'
	for i in range(len(losers)):
		player = losers[len(losers) - i - 1]
		print '{0} hunts = {1} slacks = {2} rep = {3} exit = {4}'.format(
			player, player.hunts, player.slacks, player.reputation, 
			player.exit_round)

max_game_rounds = 10000
debugger = Debugger(
	enabled=True,
	round_interval=100,
	decisions=False,
	player_out=True
)
run_game()