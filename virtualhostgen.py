#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
m sys import argv
import os

# Default Variables
saveto = '/etc/apache2/sites-enabled/'
logs = '/var/www/vhosts/'

# Used to identify if next argument corresponds to a setting
settingsValue = False;
settings = []

# virtualhost document variables
document = docAppend = docRoot = ''


# Start function to create Virtual Host File
def start():

    for i in argv[1:]:
        # Check if Setting
        if i[0] == '-' or i[0] == '+' or settingsValue:
            changeSettings(i)
        else:
            createVirtualHost(i)


# Change Settings
def changeSettings(setting):

    global settings, settingsValue

    if setting in ['-u', '-d', '-D', '-f', '+f', '-i', '+i']:

        settings.append(setting)

        if setting in ['-u', '-d', '-D']:
            settingsValue = setting

    elif settingsValue:
        # save value to global var
        if settingsValue == '-u':
            global user
            user = setting
        elif settingsValue == '-d':
            global docAppend
            docAppend = setting
        elif settingsValue == '-D':
            global docRoot
            docRoot = setting
        # refresh settingsvalue indicator
        settingsValue = False


# Create the VirtualHost Data
def createVirtualHost(website):
    
    global settings, user, logs, document, docAppend, docRoot
    options = ''

    # create document and log root variables
    if docRoot != '':
        document = docRoot
    elif docAppend != '':
        document = '/home/%s/websites/%s/%s/' % (user, website, docAppend)
    else:
        document = '/home/%s/websites/%s/public' % (user, website)


    # check if any options exist and add for host file
    if(any((True for x in settings if x in ['-i', '+i', '-f', '+f']))):
        options = '\n    Options '

        # Indexes
        if '+i' in settings:
            options += '+Indexes '
        elif '-i' in settings:
            options += '-Indexes '

        # Follow SymLinks
        if '+f' in settings:
            options += '+FollowSymLinks '
        elif '-f' in settings:
            options += '-FollowSymLinks '

        options += '\n'

    vhost = """<VirtualHost *:80>
    ServerName %s
    ServerAlias www.%s

    DocumentRoot %s
    %s
    ErrorLog \"%s/error.log\"
    CustomLog \"%s/access.log\" common
</VirtualHost>""" % (website, website, document, options, logs+website, logs+website)

    saveFile(vhost, website)


# Write the file, and ensure directories exist
def saveFile(vhost, website):

    global saveto, user, document, logs

    # Make document and log directories
    if not os.path.isdir(document):
        os.makedirs(document)
        print '%s/ document directory created' % (document)
        # set user as owner
        own = 'sudo chown -R %s:%s %s' % (user, user, document)
        os.system(own) 

    if not os.path.isdir(logs+website):
        os.makedirs(logs+website)
        print '%s/ log directory created' % (logs+website)

    # save virtualhost file
    os.chdir(saveto)
    target = website + '.conf'
    target = open(target, 'w')
    target.truncate()
    target.write(vhost)
    target.close()
    print 'Successfully created the Virtual Host File '+website+'.conf in the location '+saveto

    #reload apache
    print 'Reloading Apache'
    os.system('sudo service apache2 reload')

if __name__ == '__main__':
    # Ensure at least three arguments have been set
    if len(argv) > 3:
        start()
    else:
        print 'Missing Argument: Username and Website (-u username website.com)'

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
	elif s == 'D':
		#change document root
		if settingsValue:
			documentroot = '/' + arg + '/'
		else:
			settingsValue = 'D'		
		
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

if __name__ == '__main__':
	start()
