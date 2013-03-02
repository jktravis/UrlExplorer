# Purpose
This program has two primary purposes. The first being to provide a method to easily open
the corresponding directory within Windows Explorer based on the URL. The second 
is to more easily copy development web pages and assets to their appropriate staging 
location from a Windows workstation with drives mapped to the root directories of 
the respective web sites. 

# Requirements
This script has been only been tested on [Python 2.7 (64 bit)](http://www.python.org/getit/) running on Windows 7. 
Other versions of Python may work, as well as other operating systems, with a little tweaking. 

# Configuration
## Python
1. Once Python has been installed, be sure that you add the Python27 directory to your system path. This can be done by clicking the Start menu and searching for:
    system path
2. The first option for "Edit the systems environment variables" is what you need.
3. Open that panel and select "Environment Variables" at the bottom.
4. In the "User Variables" section at the top, either edit or add "PATH" and add
    "C:\Python27"
to the end. Be sure to preface the path with the semi-colon (;) if there was already a PATH variable to edit.

## Script
To configure the program, you will need to set the settings_file path at the
top of the UrlExplorer.py file. By default, it is set to the accompanying file
name and in the same directory as the main program. Once that is set, you will 
need to add the appropriate drives in the settings.json file. 

Other settings need to be set in the script directly. I am slowly working
towards moving these settings out to the settings file, but in the meantime,
they will need to be configured directly. 

__domain_regex__: Set this to the regular expression that will match your domain
name. A sample regex has been included that will match production, staging, and
development URLs. 

__domains__: Set the respective domains that will represent the various
environments for each system. "Prod" being the public URL, "stage" being the
place where the files are placed when moving to production, and "dev" being the
place where you make edits or QA before moving to production. 

## Settings.json
The section for the drives need to be headed with lowercase "drives". For example:

    "stage_drive" : "Z:\\"

There is also an auto archive feature for the file in question. Simply add the path to the "archive_dir" option in the settings file to enable it. 

Other sections are to come...someday.

## Multiple systems
You can have more than one system setup as well. Be sure to do the following
and you should be all set:

1. Update the regex to include all domains to capture.
2. Update the settings file to include all the respective mapped drives.
3. Update the domains dictionary to include the respective URLs
4. Include the check for the additional domains in the GetDrive() function and
	return the respective drive.
5. Include a check in the GetStage function to return the appropriate stage
	drive

# Usage
The script can be executed from Windows Explorer by double-clicking. This will
activate the default mode of opening a directory path based on the domain of
the URL given to the prompt. The same behavior is true for simple command-line
execution:

```Shell
    python UrlExplorer.py
```

## Migration
To migrate files, a separate text file will need to be populated with the
development or production URLs for the files that will need to be moved with one link per line. The script will then need to be run from the command-line and given the
-m flag and the file with the links as an argument. Example:

```Shell
    python UrlExplorer.py -m file_of_links
```

The script will iterate over the lines of the file, converting the URLs to file
paths, and copying the respective files to the staging server. For all intents
and purposes, "staging" here is synonymous with production. __Testing has not be
performed for environments that contain only two systems (production and development); thus, caution is stressed when using this tool in such
environments.__ The process will create new directories and files, and will overwrite without question. It will not, however, delete files. 

# License
This is being distributed under the MIT license.
