import os
def validateDirectory(path):
	if os.path.isdir(path) == False:
		print path + ' is not found or wrong. abort.'
		quit()
	return

def validateLanguage(lang):
	languages = ['en', 'fr', 'es', 'de', 'pt']
	if not lang in languages:
		print 'this language is not valid'
		quit()

	return True
