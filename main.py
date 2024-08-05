import sys
import json
import time
import datetime
import requests
import threading

from owo.client import OwOSelfbot

class KeyManager:
	def __init__(self, client):
		self.client = client
		self.payment_key = self.get_payment()
		self.trial_key = self.get_trial()

	def get_payment(self):
		github = requests.get(self.client.data['key']['payment']).text
		return list(filter(bool, github.split("\n")))

	def get_trial(self):
		github = requests.get(self.client.data['key']['trial']).text
		return list(filter(bool, github.split("\n")))

	def get_date(self):
		date = datetime.datetime.now(datetime.UTC)
		return date.year * date.month * date.day

	def expire_trial(self):
		expire = datetime.datetime.now(datetime.UTC).replace(hour = 0, minute = 0, second = 0, microsecond = 0)
		if datetime.datetime.now(datetime.UTC) < expire:
			expire = expire - datetime.timedelta(days = 1)
		expire = (expire - datetime.datetime.now(datetime.UTC)).seconds
		print(expire)
		print(f"[+] It will expire in {datetime.timedelta(seconds = expire)}")
		return(expire)

	def enter_trial(self):
		key = self.get_date()
		print(f"[+] Get trial key: {"".join(f"\n[+] {x}" for x in self.trial_key)}\n")
		answer = input("[?] Enter trial key: ")
		if answer == str(key):
			with open(self.client.file) as file:
				config = json.load(file)
			config['trial'] = answer
			with open("configs/key.json", "w") as file:
				json.dump(config, file, indent = 4)
			print(f"[+] The trial key is CORRECT ({answer})")
			return True
		else:
			print(f"[-] The trial key is INCORRECT ({answer})")

class PhandatSelfbot:
	def __init__(self):
		self.file = "configs/key.json"
		self.data = self.get_data()
		self.key_manager = KeyManager(self)

	def get_data(self):
		return requests.get("https://raw.githubusercontent.com/realphandat/realphandat/main/phandat-selfbot/data.json").json()

	def owo_selfbot(self):
		threads = []
		OwOClients = []
		with open("configs/owo_selfbot.json") as file:
			owo_config = json.load(file)
		for token in owo_config:
			OwOClient = OwOSelfbot(OwOClients, token)
			OwOClients.append(OwOClient)
			thread = threading.Thread(target = OwOClient.run, daemon = True, args = (token,))
			threads.append(thread)
			thread.start()
		return threads

	def start(self, expire):
		threads = []
		with open("configs/mode.json") as file:
			mode = json.load(file)
		if mode['owo_selfbot']:
			threads.extend(self.owo_selfbot())

		if expire:
			time.sleep(expire)
			sys.exit("[-] The trial key expired")
		else:
			for thread in threads:
				thread.join()

	def check_key(self):
		print(requests.get(self.data['intro']).text)

		expire = 0
		with open("configs/key.json") as file:
			key = json.load(file)
		if key['payment'] in self.key_manager.payment_key:
			print(f"[+] The payment key is CORRECT ({key['payment']})")
		else:
			print(f"[-] The payment key is INCORRECT ({key['payment']})")
			if key['trial'] == str(self.key_manager.get_date()):
				print(f"[+] The trial key is CORRECT ({key['trial']})")
			else:
				if not self.key_manager.enter_trial():
					return
			expire = self.key_manager.expire_trial()
		self.start(expire)


if __name__ == "__main__":
	phandat_selfbot = PhandatSelfbot()
	phandat_selfbot.check_key()