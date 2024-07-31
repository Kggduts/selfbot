import discord
import asyncio
import json

class Commands:
	def __init__(self, client):
		self.client = client

	async def help(self):
		self.client.logger.info(f"Sent command menu via webhook")
		await self.client.webhooks.send(
			title = f"📋 COMMAND MENU 📋",
			description = "**`start`\n`pause`\n\n`help`\n`stat`\n`setting`\n\n`say` + `-text`\n`give` + `<@user_id>` + `amount`\n`do_quest` + `on/off`\n\n`huntbot_upgrade_mode` + `on/off`\n`huntbot_upgrade_type` + `type`\n\n`use_gem` + `on/off`\n`sort_gem` + `min/max`\n`star_gem` + `on/off`\n\n`animals_mode` + `on/off`\n`animals_type` + `type`\n`animals_rank` + `rank`**",
			color = discord.Colour.random()
		)

	async def start_selfbot(self):
		self.client.data.checking.pause = False
		self.client.data.available.captcha = False
		self.client.data.available.selfbot = True
		self.client.logger.info(f"Start selfbot")
		await self.client.webhooks.send(
			title = f"🌤️ START SELFBOT 🌤️",
			color = discord.Colour.random()
		)

	async def pause_selfbot(self):
		self.client.data.checking.pause = True
		self.client.data.available.selfbot = False
		self.client.logger.info(f"Pause selfbot")
		await self.client.webhooks.send(
			title = f"🌑 PAUSE SELFBOT 🌑",
			color = discord.Colour.random()
		)

	async def stat_selfbot(self):
		self.client.logger.info(f"Sent stat via webhook")
		await self.client.webhooks.send(
			title = f"📊 STAT 📊",
			description = f"**Worked <t:{int(self.client.data.selfbot.turn_on_time)}:R> with:\n{self.client.data.emoji.arrow}Sent __{self.client.data.stat.command}__ Commands\n{self.client.data.emoji.arrow}Solved __{self.client.data.stat.captcha}__ Captchas\n{self.client.data.emoji.arrow}Done __{self.client.data.stat.quest}__ Quests\n{self.client.data.emoji.arrow}Claimed Huntbot __{self.client.data.stat.huntbot}__ Times\n{self.client.data.emoji.arrow}Used Gem __{self.client.data.stat.gem}__ Times\n{self.client.data.emoji.arrow}Gambled __{self.client.data.stat.gamble}__ Cowoncy\n{self.client.data.emoji.arrow}Changed Channel __{self.client.data.stat.change_channel}__ Times\n{self.client.data.emoji.arrow}Slept __{self.client.data.stat.sleep}__ Times**",
			color = discord.Colour.random()
		)

	async def show_setting(self):
		await self.client.webhooks.send(
			title = f"🔥 CONFIRM `YES` IN 10S 🔥",
			description = "**Send setting via webhook including __token__, __TwoCaptcha API__, __webhook url__, ...**",
			color = discord.Colour.random()
		)
		try:
			await self.client.wait_for("message", check = lambda message: message.content.lower() in ['yes', 'y'] and message.author.id in self.client.data.config.command['owner_id'], timeout = 10)
		except asyncio.TimeoutError:
			pass
		else:
			self.client.logger.info(f"Sent setting via webhook")
			with open(self.client.data.config.file) as file:
				config = json.load(file)
			await self.client.webhooks.send(
				title = f"💾 SETTING 💾",
				description = config[self.client.data.config.token],
				color = discord.Colour.random()
			)

	async def say_text(self, message):
		text = message.content.split("-")[1]
		await message.channel.send(text)
		self.client.logger.info(f"Sent {text}")

	async def give_cowoncy(self, message, command):
		if self.client.conditions.message(message, False, True, [], []):
			await message.channel.send(f"{self.client.data.discord.prefix}give {command[1]} {command[2]}")
			self.client.logger.info(f"Sent {self.client.data.discord.prefix}give {command[1]} {command[2]}")
		else:
			await message.channel.send(f"owogive {command[1]} {command[2]}")
			self.client.logger.info(f"Sent owogive {command[1]} {command[2]}")
		self.client.data.stat.command += 1
		member = await self.client.get_channel(message.channel.id).guild.fetch_member(self.client.user.id)
		nickname = member.nick if member.nick else member.display_name
		try:
			give_cowoncy_message = await self.client.wait_for("message", check = lambda message: self.client.conditions.give_cowoncy(message, str(nickname)), timeout = 5)
			if self.client.conditions.message(give_cowoncy_message, True, False, [f'<@{self.client.user.id}>', '... *but... why?*'], []):
				self.client.logger.info(f"Can't give cowoncy to yourself")
			elif self.client.conditions.message(give_cowoncy_message, True, False, [str(nickname), 'you can only send'], []):
				self.client.logger.info(f"Amount of giving cowoncy for today is over")
			elif self.client.conditions.message(give_cowoncy_message, True, False, [str(nickname), 'you silly hooman'], []):
				self.client.logger.info(f"Don't have enough cowoncy to give")
			elif self.client.conditions.message(give_cowoncy_message, True, False, [], []) and give_cowoncy_message.embeds and str(nickname) in give_cowoncy_message.embeds[0].author.name and "you are about to give cowoncy" in give_cowoncy_message.embeds[0].author.name:
				button = give_cowoncy_message.components[0].children[0]
				await button.click()
				self.client.logger.info(f"Gived cowoncy successfully")
		except asyncio.TimeoutError:
			self.client.logger.error(f"Couldn't get send cowoncy message")

	async def change_do_quest_mode(self, command):
		if command[1].lower() == "on" or command[1].lower() == "off":
			setting = command[1].lower() == "on"
			self.client.data.checking.doing_quest = not setting
			self.client.data.available.quest = setting
			self.client.data.config.quest['mode'] = setting
			self.client.logger.info(f"Do quest: {command[1].lower()}")
			await self.client.webhooks.send(
				title = f"🛸 CHANGED CONFIG 🛸",
				description = f"**{self.client.data.emoji.arrow}Do quest: {command[1].lower()}**",
				color = discord.Colour.random()
			)

	async def change_huntbot_upgrade_mode(self, command):
		if command[1].lower() == "on" or command[1].lower() == "off":
			setting = command[1].lower() == "on"
			self.client.data.config.huntbot['upgrade']['mode'] = setting
			self.client.logger.info(f"Huntbot upgrade mode: {command[1].lower()}")
			await self.client.webhooks.send(
				title = f"🛸 CHANGED CONFIG 🛸",
				description = f"**{self.client.data.emoji.arrow}Huntbot upgrade mode: {command[1].lower()}**",
				color = discord.Colour.random()
			)

	async def change_huntbot_upgrade_type(self, command):
		self.client.data.config.huntbot['upgrade']['type'] = command[1].lower()
		self.client.logger.info(f"Huntbot upgrade type: {command[1].lower()}")
		await self.client.webhooks.send(
			title = f"🛸 CHANGED CONFIG 🛸",
			description = f"**{self.client.data.emoji.arrow}Huntbot upgrade type: {command[1].lower()}**",
			color = discord.Colour.random()
		)

	async def change_use_gem_mode(self, command):
		if command[1].lower() == "on" or command[1].lower() == "off":
			setting = command[1].lower() == "on"
			self.client.data.checking.no_gem = setting
			self.client.data.config.gem['mode'] = setting
			self.client.logger.info(f"Use gem: {command[1].lower()}")
			await self.client.webhooks.send(
				title = f"🛸 CHANGED CONFIG 🛸",
				description = f"**{self.client.data.emoji.arrow}Use gem: {command[1].lower()}**",
				color = discord.Colour.random()
			)

	async def change_sort_gem_mode(self, command):
		if command[1].lower() == "min" or command[1].lower() == "max":
			self.client.data.config.gem['sort'] = command[1].lower()
			self.client.logger.info(f"Sort gem: {command[1].lower()}")
			await self.client.webhooks.send(
				title = f"🛸 CHANGED CONFIG 🛸",
				description = f"**{self.client.data.emoji.arrow}Sort gem: {command[1].lower()}**",
				color = discord.Colour.random()
			)

	async def change_star_gem_mode(self, command):
		if command[1].lower() == "on" or command[1].lower() == "off":
			setting = command[1].lower() == "on"
			self.client.data.available.special_pet = setting
			self.client.data.config.gem['star'] = setting
			self.client.logger.info(f"Star gem: {command[1].lower()}")
			await self.client.webhooks.send(
				title = f"🛸 CHANGED CONFIG 🛸",
				description = f"**{self.client.data.emoji.arrow}Star gem: {command[1].lower()}**",
				color = discord.Colour.random()
			)

	async def change_animals_mode(self, command):
		if command[1].lower() == "on" or command[1].lower() == "off":
			setting = command[1].lower() == "on"
			self.client.data.config.animals['mode'] = setting
			self.client.logger.info(f"Animals mode: {command[1].lower()}")
			await self.client.webhooks.send(
				title = f"🛸 CHANGED CONFIG 🛸",
				description = f"**{self.client.data.emoji.arrow}Animals mode: {command[1].lower()}**",
				color = discord.Colour.random()
			)

	async def change_animals_type(self, command):
		self.client.data.config.animals['type'] = command[1].lower()
		self.client.logger.info(f"Animals type: {command[1].lower()}")
		await self.client.webhooks.send(
			title = f"🛸 CHANGED CONFIG 🛸",
			description = f"**{self.client.data.emoji.arrow}Animals type: {command[1].lower()}**",
			color = discord.Colour.random()
		)

	async def change_animals_rank(self, command):
		self.client.data.config.animals['rank'] = command[1].lower()
		self.client.logger.info(f"Animals rank: {command[1].lower()}")
		await self.client.webhooks.send(
			title = f"🛸 CHANGED CONFIG 🛸",
			description = f"**{self.client.data.emoji.arrow}Animals rank: {command[1].lower()}**",
			color = discord.Colour.random()
		)