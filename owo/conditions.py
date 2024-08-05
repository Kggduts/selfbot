import re
import time
import datetime

class Conditions:
	def __init__(self, client):
		self.client = client

	def reset_time(self):
		reset_time = datetime.datetime.now(datetime.UTC).replace(hour = 7, minute = 0, second = 0, microsecond = 0)
		if datetime.datetime.now(datetime.UTC) < reset_time:
			reset_time = reset_time - datetime.timedelta(days = 1)
		reset_time = (reset_time - datetime.datetime.now(datetime.UTC)).seconds
		return(reset_time + 30)

	def message(self, message, is_owo, in_channel, all_content, any_content):
		if not is_owo or message.author.id == self.client.data.owo.id:
			if not in_channel or message.channel.id == self.client.data.discord.channel_id:
				if not all_content or all(text in message.content for text in all_content):
					if not any_content or any(text in message.content for text in any_content):
						return True
	
	def single_quest(self, quest):
		if re.findall(r"Say 'owo' [0-9]+ times!", quest):
			return True
		if re.findall(r"[0-9]+ from hunting and battling!", quest):
			return True
		if re.findall(r"Manually hunt [0-9]+ times!", quest):
			return True
		if re.findall(r"Hunt [0-9]+ animals that are (.*?) rank!", quest):
			return True
		if re.findall(r"Battle [0-9]+ times!", quest):
			return True
		if re.findall(r"Gamble [0-9]+ times!", quest):
			return True
		if re.findall(r"Use an action command on someone [0-9]+ times!", quest):
			return True

	def glitch_available(self):
		return self.client.data.config.glitch and not (self.client.data.timeout.glitch - time.time() <= 0) and self.client.data.current_task_loop.check_glitch > 0

	def give_cowoncy(self, message, nickname):
		if self.message(message, True, False, [f'<@{self.client.user.id}>', '... *but... why?*'], []):
			return True
		if self.message(message, True, False, [nickname, 'you can only send'], []):
			return True
		if self.message(message, True, False, [nickname, 'you silly hooman'], []):
			return True
		if self.message(message, True, False, [], []) and message.embeds and nickname in message.embeds[0].author.name and "you are about to give cowoncy" in message.embeds[0].author.name:
			return True