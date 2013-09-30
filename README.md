Virtual Host Generator
==================================================


This script allows you to create apache2 virtual host files through the simple invoking of the script.

The script can be fed multiple arguments that determine the virtual host file options, creating and then prompting you to reload the apache configuration files to take effect.

## Getting Started

Simply copy the script into your operating system, and edit a few details in the script to tailor it for your environment.

These variables are located at the top of the script

1. The `siteroot` variable contains the root of for your website files
2. The `errorlog` variable contains the root for error logs
3. The `accesslog` variable contains the root for access logs
4. The `saveto` variable contains to the root for virtualhost files to go

## Usage

The script must be invoked with the last argument being a servername, such as with `virtualhostgen examplesite.com`. Flags must be before the servername, and change information contained in the virtual host file, for example `virtualhostgen -i -d laravel/public example.org`.

Current support flags are:

- `-d` is followed by another argument (such as `laravel/public`) and adds to the document route
- `-D` is similar to -d, but instead of adding to the document route, it overides the default value
- `-F` turns the FollowSymLinks option on
- `-I` turns the Index option on

The flags are limited to suit my current set up. This will be updated to include options to turn off certain options that may have different defaults on different systems.