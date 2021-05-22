import subprocess

from entry import Entry


class PassGen:
	def __init__(self, secret: str, exe: str = "passGen"):
		self.__secret = secret
		self.exe = exe

	def get_password(self, entry: Entry) -> str:
		command = [self.exe, '-i']

		phrase = entry.target
		if entry.host is not None:
			phrase += '/' + entry.host
		if entry.destination is not None:
			phrase += ':' + entry.destination
		if entry.number is not None:
			phrase += '%' + str(entry.number)
		phrase += '~' + self.__secret

		result = subprocess.run(command, input=phrase, capture_output=True, text=True, check=True)
		return result.stdout.strip()

	def check_secret(self):
		return subprocess.run([self.exe, '-i', '-c'], input=f'#{self.__secret}#', capture_output=True, text=True,
		                      check=True).stdout.strip()
