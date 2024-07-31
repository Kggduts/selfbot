import os

class Notification:
	def __init__(self, client):
		self.client = client
	
	async def notify(self):
		if self.client.data.config.music_notification:
			await self.play_music()

	async def play_music(self):
		try:
			os.startfile('assets/music.mp3')
		except:
			pass