import sys
import discord

from owo.data import Data
from public.log import Log
from owo.quest import Quest
from owo.tasks import Tasks
from owo.modules import Modules
from owo.commands import Commands
from owo.webhooks import Webhooks
from owo.conditions import Conditions
from owo.notification import Notification

class OwOSelfbot(discord.Client):
	def __init__(self, OwOClients, token, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.OwOClients = OwOClients
		self.data = Data(token)
		self.log = Log(self)
		self.quest = Quest(self)
		self.tasks = Tasks(self)
		self.modules = Modules(self)
		self.commands = Commands(self)
		self.webhooks = Webhooks(self)
		self.conditions = Conditions(self)
		self.notification = Notification(self)
	
	async def on_ready(self):
		if self.data.selfbot.on_ready:
			self.data.selfbot.on_ready = False
			self.data.owo = self.get_user(self.data.owo.id)
			self.logger = await self.log.create("owo")
			await self.modules.startup()
			await self.modules.intro()
			await self.tasks.start()

	async def on_message(self, message):
		if self.data.selfbot.expire:
			sys.exit()
		await self.modules.detect_image_captcha(message)
		await self.modules.detect_hcaptcha(message)
		await self.modules.detect_unknown_captcha(message)
		await self.modules.detect_problems(message)
		if self.data.config.someone_mentions:
			await self.modules.someone_mentions(message)
		if self.data.config.someone_challenges or self.data.quest.battle_friend:
			await self.modules.someone_challenges(message)
		if self.data.config.quest['mode']:
			await self.modules.quest_progress(message)
		if (self.data.config.gem['mode'] or self.conditions.glitch_available()) and not self.data.checking.no_gem:
			empty_gem = await self.modules.check_empty_gem(message)
			if empty_gem:
				await self.modules.use_gem(empty_gem)
		if self.data.config.caught:
			await self.modules.check_caught_animals(message)
		if self.data.config.command['mode']:
			await self.modules.command(message)

	async def on_message_edit(self, before, after):
		if self.data.config.gamble['slot']['mode']:
			await self.modules.check_slot(after)
		if self.data.config.gamble['coinflip']['mode']:
			await self.modules.check_coinflip(after)
		if self.data.config.join_owo_giveaway:
			await self.modules.join_owo_giveaway(after)