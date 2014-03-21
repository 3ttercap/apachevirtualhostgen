Virtual Host Generator
==================================================


This script allows you to create apache2 virtual host files through the simple invoking of the script.

The script can be fed multiple arguments that determine the virtual host file options, creating and then prompting you to reload the apache configuration files to take effect.

## Getting Started

Simply copy the script into your operating system, and edit a few details in the script to tailor it for your environment.

These variables are located at the top of the script

1. The `saveto` variable contains the file root of where to save virtualhost files
2. The `logs` variable contains the root for all access/error logs

## Usage

The script must be invoked with the last argument being a servername, such as with `virtualhostgen examplesite.com`. Flags must be before the servername, and change information contained in the virtual host file, for example `virtualhostgen -i -d laravel/public example.org`.

Current support flags are:

- `-u` this flag is required, and must proceed a default user to own
- `-d` Appends the default value of document root (/home/%user%/appended/root)
- `-D` Overides the default of document root (/overwrited/root/)
- `-f` turns off FollowSymLinks, and `+f` turns them on
- `-i` turns off Indexes, and `+i` turns them on

Example base usage:
`virtualhostgen.py -u 'joshwalwyn' example.com`
`virtualhostgen.py -u 'joshwalwyn' +i -f -D /var/www/mainsite example.com`