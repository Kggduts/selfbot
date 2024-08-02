import asyncio
import random
import discord
import time

from discord.ext import tasks

class Tasks:
	def __init__(self, client):
		self.client = client
		self.tasks = [
			self.check_owo_status,
			self.change_channel,
			self.check_twocaptcha_balance,
			self.do_quest,
			self.vote_topgg,
			self.claim_daily,
			self.sleep,
			self.grind,
			self.claim_submit_huntbot,
			self.check_glitch,
			self.sell_sac_animals,
			self.play_gamble,
			self.pray_curse,
			self.entertainment,
		]

	async def start(self, skip = None):
		self.client.data.available.selfbot = True
		for task in self.tasks:
			if skip:
				if task in skip:
					continue
			try:
				task.start()
				await asyncio.sleep(random.randint(10, 20))
			except RuntimeError:
				pass

	async def stop(self, skip = None):
		self.client.data.available.selfbot = False
		for task in self.tasks:
			if skip:
				if task in skip:
					continue
			task.cancel()

	@tasks.loop(minutes = 1)
	async def check_owo_status(self):
		if self.client.data.config.check_owo_status and self.client.data.current_task_loop.check_owo_status > 0:
			await self.client.modules.check_owo_status()
		self.client.data.current_task_loop.check_owo_status += 1

	@tasks.loop(seconds = random.randint(600, 1200))
	async def change_channel(self):
		if self.client.data.current_task_loop.change_channel > 0:
			await self.client.modules.change_channel()
		self.client.data.current_task_loop.change_channel += 1

	@tasks.loop(minutes = 1)
	async def check_twocaptcha_balance(self):
		if self.client.data.config.twocaptcha_balance['mode']:
			if self.client.data.config.image_captcha['mode']:
				await self.client.modules.check_twocaptcha_balance(self.client.data.config.image_captcha['twocaptcha'])
			if self.client.data.config.hcaptcha['mode']:
				await self.client.modules.check_twocaptcha_balance(self.client.data.config.hcaptcha['twocaptcha'])
		self.client.data.current_task_loop.check_twocaptcha_balance += 1

	@tasks.loop(minutes = 1)
	async def do_quest(self):
		if int(self.client.data.timeout.quest) - time.time() <= 0:
			self.client.data.available.quest = True
		if self.client.data.config.quest['mode'] and self.client.data.available.quest and not self.client.data.checking.doing_quest:
			await self.client.modules.do_quest()
		self.client.data.current_task_loop.do_quest += 1

	@tasks.loop(hours = 12)
	async def vote_topgg(self):
		if self.client.data.config.topgg:
			await self.client.modules.vote_topgg()
		self.client.data.current_task_loop.vote_topgg += 1

	@tasks.loop(minutes = 1)
	async def claim_daily(self):
		if self.client.data.config.daily:
			await self.client.modules.claim_daily()
		self.client.data.current_task_loop.claim_daily += 1

	@tasks.loop(minutes = 1)
	async def sleep(self):
		if self.client.data.config.sleep:
			await self.client.modules.sleep()
		self.client.data.current_task_loop.sleep += 1

	@tasks.loop(seconds = random.randint(18, 25))
	async def grind(self):
		try:
			if self.client.data.config.grind['owo'] or self.client.data.quest.owo:
				await self.client.modules.send_owo()
				await asyncio.sleep(random.randint(5, 10))
			if self.client.data.config.grind['hunt'] or self.client.data.quest.hunt:
				await self.client.modules.send_hunt()
				await asyncio.sleep(random.randint(5, 10))
			if (self.client.data.config.grind['battle'] or self.client.data.quest.battle) and not self.client.data.checking.block_battle:
				await self.client.modules.send_battle()
				await asyncio.sleep(random.randint(5, 10))
			if self.client.data.config.grind['quote']:
				await self.client.modules.send_quote()
		except Exception as e:
			self.client.logger.error(f"Grind Has The Error | {str(e)}")
			await self.client.webhooks.send(
				title = "⚙️ GRIND ⚙️",
				description = f"**{self.client.data.emoji.arrow}Error: {str(e)}**",
				color = discord.Colour.random()
			)
		self.client.data.current_task_loop.grind += 1

	@tasks.loop(minutes = 1)
	async def claim_submit_huntbot(self):
		if self.client.data.config.huntbot['claim_submit']:
			await self.client.modules.claim_submit_huntbot()
		self.client.data.current_task_loop.claim_submit_huntbot += 1

	@tasks.loop(seconds = random.randint(600, 1200))
	async def check_glitch(self):
		if self.client.data.config.glitch:
			await self.client.modules.check_glitch()
		self.client.data.current_task_loop.check_glitch += 1

	@tasks.loop(seconds = random.randint(1200, 3600))
	async def sell_sac_animals(self):
		if self.client.data.config.animals['mode']:
			await self.client.modules.sell_sac_animals()
		self.client.data.current_task_loop.sell_sac_animals += 1

	@tasks.loop(seconds = random.randint(60, 120))
	async def play_gamble(self):
		if self.client.data.config.gamble['slot']['mode'] or self.client.data.quest.gamble:
			await self.client.modules.play_slot()
			await asyncio.sleep(random.randint(5, 10))
		if self.client.data.config.gamble['coinflip']['mode'] or self.client.data.quest.gamble:
			await self.client.modules.play_coinflip()
			await asyncio.sleep(random.randint(5, 10))
		if self.client.data.config.gamble['blackjack']['mode'] or self.client.data.quest.gamble:
			await self.client.modules.play_blackjack()
		self.client.data.current_task_loop.play_gamble += 1

	@tasks.loop(seconds = random.randint(300, 600))
	async def pray_curse(self):
		if self.client.data.config.pray_curse['mode'] and (not self.client.data.quest.pray or not self.client.data.quest.curse) and not self.client.data.checking.block_pray_curse:
			if self.client.data.config.pray_curse['type'].lower() == "pray":
				await self.client.modules.pray(self.client.data.config.pray_curse['user_id'])
			else:
				await self.client.modules.curse(self.client.data.config.pray_curse['user_id'])
		self.client.data.current_task_loop.pray_curse += 1

	@tasks.loop(seconds = random.randint(60, 120))
	async def entertainment(self):
		if int(self.client.data.timeout.entertainment) - time.time() <= 0:
			self.client.data.checking.run_limit = False
			self.client.data.checking.pup_limit = False
			self.client.data.checking.piku_limit = False
		if self.client.data.config.entertainment['run'] and not self.client.data.checking.run_limit:
			await self.client.modules.send_run()
		if self.client.data.config.entertainment['pup'] and not self.client.data.checking.pup_limit:
			await self.client.modules.send_pup()
		if self.client.data.config.entertainment['piku'] and not self.client.data.checking.piku_limit:
			await self.client.modules.send_piku()
		if self.client.data.config.entertainment['common_ring']:
			await self.client.modules.buy_common_ring()
		self.client.data.current_task_loop.entertainment += 1