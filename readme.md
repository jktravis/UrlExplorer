# Purpose
The purpose of this program is to more easily copy development web pages and
assets to their appropriate staging location from a Windows workstation with
drives mapped to the document roots of the respective web sites. 

# Requirements
This script has been only been tested on [Python 2.7 (64 bit)](http://www.python.org/getit/) running on Windows 7. 
Other versions of Python may work, as well as other operating systems, with a 
little tweaking. 

# Configuration
## Python
1. Once Python has been installed, be sure that you add the Python27 directory to your system path. This can be done by clicking the Start menu and searching for:
    system path
2. The first option for "Edit the systems environment variables" is what you need.
3. Open that panel and select "Environment Variables" at the bottom.
4. In the "User Variables" section at the top, either edit or add "PATH" and add
    "C:\Python27"
to the end. Be sure the preface the path with the semi-colon (;) if there was already a PATH variable to edit.

## Script
To configure the program, you will need to set the settings_file path at the
top of the UrlExplorer.py file. By default, it is set to the accompanying file
name and in the same directory as the main program. Once that is set, you will 
need to add the appropriate drives in the settings.json file. The section for
the drives need to be headed with lowercase "drives". For example:

    "stage_drive" : "Z:\\"

There is also an auto archive feature for the file in question. Simply add the path to the "archive_dir" option in the settings file to enable it. 

# Usage
The script can be executed from the Explorer by double-clicking. This will
activate the default mode of opening a directory path based on the domain of
the URL given to the prompt. The same behavior is true for simple command-line
execution:

    python UrlExplorer.py

## Migration
To migrate files, a separate text file will need to be populated with the
development URLs for the files that will need to be moved with one link per
line. The script will then need to be run from the command-line and given the
-m flag and the file with the links as an argument. Example:

    python UrlExplorer.py -m file_of_links

The script will iterate over the lines of the file, converting the URLs to file
paths, and copying the respective files to the staging server. For all intents
and purposes, "staging" here is synonymous with production. The process will
create new directories and files, and will overwrite without question. It will
not, however, delete files. 

# License
This is being distributed under the MIT license.
