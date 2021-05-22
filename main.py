import os
import sys
from pathlib import Path

import pyperclip
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog, QTableWidget

from entry import Entry
from data_io import read_file, write_file
from passgen import PassGen
from table_adapter import TableAdapter

DATA_PATH = Path(__file__).resolve().parent / 'data.tsv'


def create_window(form: str):
	loader = QUiLoader()
	path = os.fspath(Path(__file__).resolve().parent / form)
	ui_file = QFile(path)
	ui_file.open(QFile.ReadOnly)
	win = loader.load(ui_file)
	ui_file.close()
	return win


def add_entry(table: TableAdapter):
	dialog = create_window('addDialog.ui')
	dialog.exec()
	if dialog.result() == QDialog.Accepted:
		target: str = dialog.targetLineEdit.text()
		host = dialog.hostLineEdit.text()
		destination = dialog.destinationLineEdit.text()
		number = dialog.numberLineEdit.text()
		entry = Entry(target)
		if len(host) != 0:
			entry.host = host
		if len(destination) != 0:
			entry.destination = destination
		if len(number) != 0:
			entry.number = int(number)
		table.add(entry)


def main():
	app = QApplication([])

	pass_dialog = create_window('passwordDialog.ui')
	pass_dialog.exec()
	password = pass_dialog.lineEdit.text()

	pass_gen = PassGen(password)
	window = create_window('form.ui')

	table: QTableWidget = window.entryTable
	table.setHorizontalHeaderLabels(['target', 'host', 'destination', 'number'])
	adapter = TableAdapter(table)
	if DATA_PATH.exists():
		for entry in read_file(DATA_PATH):
			adapter.add(entry)

	window.addButton.clicked.connect(lambda: add_entry(adapter))

	window.removeButton.clicked.connect(lambda: adapter.remove_selected())

	window.runButton.clicked.connect(lambda: pyperclip.copy(pass_gen.get_password(adapter.get_selected())))

	window.show()
	status = app.exec_()
	write_file(DATA_PATH, adapter.get_all())
	sys.exit(status)


if __name__ == "__main__":
	main()