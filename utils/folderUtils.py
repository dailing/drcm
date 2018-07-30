import os


def ensurePath(folders = ['log', 'state']):
	for folder in folders:
		if not os.path.exists(folder):
			os.mkdir(folder)