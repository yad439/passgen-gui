from typing import Iterable

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem

from entry import Entry


class TableAdapter:
	def __init__(self, table: QTableWidget):
		self.__table = table

	def add(self, entry: Entry) -> None:
		table = self.__table
		rows_num = table.rowCount()
		table.insertRow(rows_num)
		table.setItem(rows_num, 0, QTableWidgetItem(entry.target))
		if entry.host is not None:
			table.setItem(rows_num, 1, QTableWidgetItem(entry.host))
		if entry.destination is not None:
			table.setItem(rows_num, 2, QTableWidgetItem(entry.destination))
		if entry.number is not None:
			table.setItem(rows_num, 3, QTableWidgetItem(str(entry.number)))

	def remove(self, row: int) -> None:
		self.__table.removeRow(row)

	def remove_selected(self) -> None:
		selection = self.__table.selectedIndexes()
		rows = set(map(lambda x: x.row(), selection))
		assert len(rows) <= 1
		for row in rows:
			self.remove(row)

	def get_selected(self) -> Entry:
		selection = self.__table.selectedIndexes()
		rows = list(set(map(lambda x: x.row(), selection)))
		assert len(rows) == 1
		row = rows[0]

		return self.row_to_entry(row)

	def get_all(self) -> Iterable[Entry]:
		rows = self.__table.rowCount()
		return map(self.row_to_entry, range(rows))

	def row_to_entry(self, row):
		table = self.__table
		entry = Entry(table.item(row, 0).text())
		host = table.item(row, 1)
		destination = table.item(row, 2)
		number = table.item(row, 3)
		if host is not None:
			entry.host = host.text()
		if destination is not None:
			entry.destination = destination.text()
		if number is not None:
			entry.number = int(number.text())
		return entry
