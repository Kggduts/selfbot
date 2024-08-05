import time
import random
import json

class Data:
	def __init__(self, token):
		self.config = Config(token)

		self.owo = OwO()
		self.cmd = CMD()
		self.stat = Stat()
		self.emoji = Emoji()
		self.quest = Quest()
		self.discord = Discord()
		self.selfbot = Selfbot()
		self.timeout = Timeout()
		self.checking = Checking()
		self.available = Available()
		self.animals_list = Animals_List()
		self.current_task_loop = Current_Task_Loop()
		self.current_gamble_bet = Current_Gamble_Bet(self)

class Config:
	def __init__(self, token):
		self.file = "configs/owo_selfbot.json"
		with open(self.file) as file:
			data = json.load(file)
			self.token = token
			self.check_owo_status = data[token]['check_owo_status']
			self.join_owo_giveaway = data[token]['join_owo_giveaway']
			self.get_owo_prefix = data[token]['get_owo_prefix']
			self.someone_mentions = data[token]['someone_mentions']
			self.someone_challenges = data[token]['someone_challenges']
			self.channel_id = data[token]['channel_id']
			self.image_captcha = data[token]['image_captcha']
			self.hcaptcha = data[token]['hcaptcha']
			self.twocaptcha_balance = data[token]['twocaptcha_balance']
			self.quest = data[token]['quest']
			self.topgg = data[token]['topgg']
			self.daily = data[token]['daily']
			self.sleep = data[token]['sleep']
			self.grind = data[token]['grind']
			self.huntbot = data[token]['huntbot']
			self.gem = data[token]['gem']
			self.glitch = data[token]['glitch']
			self.animals = data[token]['animals']
			self.caught = data[token]['caught']
			self.gamble = data[token]['gamble']
			self.pray_curse = data[token]['pray_curse']
			self.entertainment = data[token]['entertainment']
			self.command = data[token]['command']
			self.webhook = data[token]['webhook']
			self.log_file = data[token]['log_file']
			self.music_notification = data[token]['music_notification']
			self.error_retry_times = data[token]['error_retry_times']

class OwO:
	def __init__(self):
		self.id = 408785106942164992

class CMD:
	def __init__(self):
		self.owo = ['owo', 'uwu']
		self.hunt = ['h', 'hunt']
		self.battle = ['b', 'battle']
		self.action = ['cuddle', 'hug', 'kiss', 'lick', 'nom', 'pat', 'poke', 'slap', 'stare', 'highfive', 'bite', 'greet', 'punch', 'handholding', 'tickle', 'kill', 'hold', 'pats', 'wave', 'boop', 'snuggle', 'bully']

class Stat:
	def __init__(self):
		self.command = 0
		self.captcha = 0
		self.quest = 0
		self.huntbot = 0
		self.gem = 0
		self.gamble = 0
		self.change_channel = 0
		self.sleep = 0

class Emoji:
	def __init__(self):
		self.arrow = "<a:Arrow:1065047400714088479>"
		self.legendary = "<a:legendary:417955061801680909>"
		self.gem = "<a:gem:510023576489951232>"
		self.fabled = "<a:fabled:438857004493307907>"
		self. glitch = "<a:distorted:728812986147274835>"
		self.hidden = "<a:hidden:459203677438083074>"

class Quest:
	def __init__(self):
		self.owo = False
		self.hunt = False
		self.battle = False
		self.gamble = False
		self.action_someone = False
		self.battle_friend = False
		self.cookie = False
		self.pray = False
		self.curse = False
		self.action_you = False

class Discord:
	def __init__(self):
		self.prefix = "owo"
		self.channel = ""
		self.channel_id = ""
		self.mention = ""
		self.nickname = ""
		self.quest = ""
		self.inventory = "gem1 gem3 gem4 star"
		self.ga_joined = []

class Selfbot:
	def __init__(self):
		self.on_ready = True
		self.turn_on_time = time.time()
		self.work_time = random.randint(600, 1200)

class Timeout:
	def __init__(self):
		self.quest = 0
		self.daily = 0
		self.huntbot = 0
		self.glitch = 0
		self.entertainment = 0

class Checking:
	def __init__(self):
		self.pause = False
		self.no_gem = False
		self.run_limit = False
		self.pup_limit = False
		self.piku_limit = False
		self.doing_quest = False
		self.block_battle = False
		self.block_pray_curse = False
		self.captcha_attempts = 0

class Available:
	def __init__(self):
		self.selfbot = True
		self.special_pet = True
		self.quest = True
		self.captcha = False
		self.blackjack = False

class Animals_List:
	def __init__(self):
		self.legendary = ['gdeer', 'gfox', 'glion', 'gowl', 'gsquid']
		self.gem = ['gcamel', 'gfish', 'gpanda', 'gshrimp', 'gspider']
		self.bot = ['dinobot', 'giraffbot', 'hedgebot', 'lobbot', 'slothbot']
		self.glitch = ['glitchflamingo', 'glitchotter', 'glitchparrot', 'glitchraccoon', 'glitchzebra']
		self.fabled = ['dboar', 'deagle', 'dfrog', 'dgorilla', 'dwolf']
		self.hidden = ['hkoala', 'hlizard','hmonkey', 'hsnake', 'hsquid']

class Current_Task_Loop:
	def __init__(self):
		self.check_owo_status = 0
		self.change_channel = 0
		self.check_twocaptcha_balance = 0
		self.do_quest = 0
		self.vote_topgg = 0
		self.claim_daily = 0
		self.sleep = 0
		self.grind = 0
		self.claim_submit_huntbot = 0
		self.check_glitch = 0
		self.sell_sac_animals = 0
		self.play_gamble = 0
		self.pray_curse = 0
		self.entertainment = 0

class Current_Gamble_Bet:
	def __init__(self, client):
		self.client = client
		self.slot = int(self.client.config.gamble['slot']['bet'])
		self.coinflip = int(self.client.config.gamble['coinflip']['bet'])
		self.blackjack = int(self.client.config.gamble['blackjack']['bet'])