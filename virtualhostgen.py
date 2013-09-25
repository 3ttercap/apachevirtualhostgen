#!/usr/bin/env python

from sys import argv
import os

# Initial global variables
siteroot = '/home/sites/'
errorlog = '/home/logs/errors/'
accesslog = '/home/logs/access/'
saveto = '/etc/apache2/sites-enabled/'

# Settings
documentroot  = '' # site subroot for virtualhost documentroot
settingsValue = False # indicator whether next argument for setting
settings = Indexes = FollowSymLinks = ''


def changeSettings(s, arg = ''):
	
	global settings, settingsValue, documentroot, Indexes, FollowSymLinks
	
	# check settings identifier
	if s == 'I':
		Indexes = '+Indexes'
	elif s == 'F':
		FollowSymLinks = '+FollowSymLinks'
	elif s == 'd':
		# check whether function is called with argument to change document root
		if settingsValue:
			documentroot += '/' + arg + '/'
		else:
			settingsValue = 'd'
		
		
	settings = '\n\n    Options '
	
	
def generateVirtualHost(siteurl):
	
	global settings, Indexes, FollowSymLinks, documentroot
	
	settings = settings+Indexes+' '+FollowSymLinks
	
	data = """<VirtualHost *:80>
    ServerName %s
    ServerAlias  www.%s

    DocumentRoot %s %s

    ErrorLog \"%serror_%s.log\"
    CustomLog \"%saccess_%s.log\" common
</VirtualHost>""" % (siteurl, siteurl, siteroot + siteurl + documentroot, settings, errorlog, siteurl, accesslog, siteurl)
	return data
	

def saveFile(siteurl, virtualHostFile):
	
	global saveto, siteroot, documentroot
	
	documentroot = siteurl + documentroot
	
	# Make site directory if needed
	if not os.path.isdir(siteroot+documentroot):
		os.makedirs(siteroot+documentroot)
		os.chdir(siteroot+documentroot)
		
		# create splash page
		splash = open('index.html', 'w')
		splash.truncate()
		splash.write('<h1>Your website here!</h1>')
		splash.close()
		
		print 'Directory '+siteroot+documentroot+' created'
	
	# save file in saveto variable
	os.chdir(saveto)
	# check current file doesn't exist, else prompt for overwrite
	target = siteurl + '.conf'
	target = open(target, 'w')
	target.truncate()
	target.write(virtualHostFile)
	target.close()
	
	print 'Successfully created the Virtual Host File '+siteurl+'.conf in the location '+saveto
	print 'Reloading Apache'
	os.system('sudo service apache2 reload')

# Start 
def start():
	
	# Check for arguments and change settings
	if len(argv) > 1:
		
		# foreach argument
		for i in argv[1:]:
			
			# check if setting, else site
			if i[0] == '-':
				changeSettings(i[1])
			else:
				# ensure value is not for settings
				global settingsValue, saveto
				if settingsValue == False:
					# Not settings value, so create and save virtual host file!
					virtualHost = generateVirtualHost(i)
					if os.path.isfile(saveto+i+'.conf'):
						print 'Virtual Host already exists! Overwrite?'
						while True:
							c = raw_input('> ')
							if c.lower() == 'y' or c.lower() == 'yes':
								saveFile(i, virtualHost)
								break
							elif c.lower() =='n' or c.lower() == 'no':
								break
					else:
						saveFile(i, virtualHost)
				else:
					changeSettings(settingsValue, i)
					settingsValue = False
			
	else:
		print 'No arguments fed'

start()