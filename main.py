import hashlib
import os
import sys
from pathlib import Path

import pyperclip
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog, QLabel, QTableWidget

from data_io import read_file, write_file
from entry import Entry
from passgen import PassGen
from table_adapter import TableAdapter

SALT = b'\x89\x1c\x9eD\xe2\xfa\xd0!\x9d\xab\xb7\xfch\x0e\xd6\x1b\x96tg\xbe\x00\xa22J\xb2j\xcb\xe5JX_!'

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


def generate_check(password: str, output: QLabel):
	output.setText(hashlib.pbkdf2_hmac('sha3-224', password.encode('utf-8'), SALT, 16384, 2).hex())


def main():
	app = QApplication([])

	pass_dialog = create_window('passwordDialog.ui')
	pass_dialog.lineEdit.textEdited.connect(lambda pas: generate_check(pas, pass_dialog.checkLabel))
	pass_dialog.exec()
	if pass_dialog.result() != QDialog.Accepted:
		return
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
