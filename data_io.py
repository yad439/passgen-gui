import csv
from pathlib import Path
from typing import Iterable

from entry import Entry


def write_file(file_path: Path, data: Iterable[Entry]) -> None:
	data_str = map(lambda e: [e.target, e.host, e.destination, str(e.number) if e.number is not None else None], data)
	with open(file_path, 'w',newline='') as file:
		writer = csv.writer(file, delimiter='\t')
		writer.writerows(data_str)


def read_file(file_path: Path) -> Iterable[Entry]:
	with open(file_path) as file:
		reader = csv.reader(file, delimiter='\t')
		return list(map(lambda r: Entry(r[0], host=r[1] if len(r[1]) != 0 else None,
		                                destination=r[2] if len(r[2]) != 0 else None,
		                                number=int(r[3]) if len(r[3]) != 0 else None), reader))
