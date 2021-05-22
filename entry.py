from typing import Optional


class Entry:
	def __init__(self, target: str, *, host: Optional[str] = None, destination: Optional[str] = None,
	             number: Optional[int] = None):
		self.target = target
		self.host = host
		self.destination = destination
		self.number = number
