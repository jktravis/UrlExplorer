#!/usr/local/bin/env python
#**************************************************************************
# Program.........: UrlExplorer 
# Copyright.......: Copyright (c) 2012 Joshua Travis
# Initial Author..: Joshua Travis (joshua.travis@gmail.com); @jktravis
# Date Written....: 2012-11-08
# Date Modified...: 2013-03-02
# Description.....: Script to convert a URL into a file path. There is also a
#                   mechanism to migrate files from dev to staging. Currently,
#                   the drives have to be manually configured.
# Called By.......: Command line or double-click
# Options.........: -m <file> 
#                   Iterates over the file and Migrates/Moves the respective files
#**************************************************************
import os, re, sys, getopt, shutil, json

#try:
#  input_json = json.load(open(os.path.abspath(self.settings_file)))
#
#  for majorkey, subdict in input_json.iteritems():
#     if majorkey == 'drives':
#        for subkey, value in subdict.iteritems():
#           self.drives[subkey] = value
#
#     if majorkey == 'archive_dir':
#        self.archive_dir = subdict
#
#  if len(self.args) == 0 and len(self.options) == 0:
#     urlexpl = UrlExplorer()
#     urlexpl.ShowInput("\nPlease Enter URL to open: ")
#
#  elif len(self.options) > 0 and len(self.args) == 0:
#     print 'Usage: ' + sys.argv[0] + ' -m <file>'
#     sys.exit(2)
#
#  elif len(self.options) == 0 and len(self.args) > 0:
#     print 'Usage: ' + sys.argv[0] + ' -m <file>'
#     sys.exit(2)
#
#  else:
#Process and execute the options
#This only runs if one option AND one argument is provided
#Additionally, this is specific to the migration portion
      #urlexpl = UrlExplorer()
      #for option, arg in self.options:
         #if option == '-m':
            #TODO: Call Object Method
            #urlexpl.Migrate()

         #if option == '-a':
         #   urlexpl.Migrate()
   
#TODO: Move this to Method
      #if self.migrate:
      #   lines = self.GetFileLines(self.args[0])

#         for line in lines:
#            self.Migrate(os.path.abspath(self.ProcessUrl(line)))
#      
#      if self.archive_dir:
#         self.Archive(self.args[0])
#
#      print "\nMigration completed with (" + str(self.error_count) + ") errors."
#      if self.error_count != 0:
#         sys.exit(2)
#
#except IOError as e:
#  print 'No configuration found. Be sure the file exists and is properly populated.'
#  sys.exit(2)
#
#except getopt.GetoptError:
#  print 'Usage: ' + sys.argv[0] + ' -m <file>'
#  sys.exit(2)
#
#except KeyboardInterrupt:
#  sys.exit(2)
#
#except InvalidDomainError:
#  print '\nPlease provide a valid domain and path. Domains recognized are: \n'
#  for key, val in self.domains.iteritems():
#     print val
#
#  raw_input("\n<Press ENTER to exit>\n")
#  sys.exit(2)
#
#except InvalidCopyError as e:
#  print "\n" + 'Unable to open path' + "\n\n" + e.filename + "\n\nPlease confirm your drive mapping settings."
#  raw_input("<Press ENTER to exit>\n")
#
#except NoDriveFoundError:
#  print "No stage drive found. Please confirm your configuration."
#  sys.exit(2)


#TODO: Move all settings to th json file

#**************************************************************
#Begin User Configurable Properties
#**************************************************************

# Sample regex. Matches: 
#   http://dev.example.com
#   https://stage.example.com
#   http://www.example.com
#   https://www.example.com
#**************************************************************
#End User Configurable Properties
#**************************************************************
class UrlExplorer:

# expects the arguments to be of type string, string, dict, string, dict, respectively
   def __init__(self, drives, domains, settings_file='settings.json', domain_regex='http:\/\/(dev|stage|www).example.com\/', archive_dir=''):
      self.settings_file = settings_file
      self.domain_regex = re.compile(domain_regex)
      self.drives = drives
      self.archive_dir = archive_dir
      self.domains = domains #INCLUDE the trailing backslash
      self.error_count = 0 #used to track the numbers of errors when copying files

   #prompt for the URL
   def ShowInput(self, prompt):
      path = raw_input(prompt)
      return path

#Convert the URL into a filepath.
   def ConvertUrl(self, url):
      path = self.domain_regex.sub('', url)

      try:
         npath = self.GetDrive(url) + path

      except TypeError:
         raise InvalidDomainError

      return npath


#Archive file
   def Archive(self, f):
      try:
         shutil.move(os.path.abspath(f), os.path.abspath(self.archive_dir))
         return True
      except:
         return False

#returns the lines from the given file
   def GetFileLines(self, in_file):
      return open(in_file).read().splitlines()

#Opens the path in default file browser. Explorer.exe for example
#Not tested on other systems, though it might work
   def OpenPath(self, foldername):
      try:
         systems = {
               'nt': os.startfile,
               'posix': lambda foldername: os.system('open "%s"' % foldername)
               }
         systems.get(os.name, os.startfile)(foldername)

      except (AttributeError):
         raise InvalidCopyError(foldername)

#Get stage drive
   def GetStage(self, path):
      drive = re.match('^.{3}', path).group(0)
      if drive == self.drives['dev_drive']:
         return self.drives['stage_drive'][0:2] # strip the backslash so the re module will play nice

      else:
         raise NoDriveFoundError
      
#Migrate the files in the file
   def Migrate(self, dev):
      stage = re.sub('^.{2}', self.GetStage(dev), dev)
      try:
         print 'Copying file:', dev, " => ", stage
      
         directory = os.path.split(stage)[0]

         if not os.path.exists(directory):
             os.makedirs(directory)
         
         shutil.copyfile(dev, stage)
         print 'Success!', '\n'

# Catch exception here so loop will continue
      except IOError as e:
         msg = 'Failed:'
         print msg, e, '\n', dev, stage, '\n'
         self.error_count += 1

# GetDrive()
# return appropriate drive letter "
# To add more, just update your drives and domains
# and add more conditionals
   def GetDrive(self, url):
      try:
         domain = self.domain_regex.search(url).group(0)
      except AttributeError:
         raise InvalidDomainError

# In my environment, we don't have direct access to production.
# So all prod links open dev links.
      if domain == self.domains['prod']:
         return self.drives['dev_drive']

      elif domain == self.domains['dev']:
         return self.drives['dev_drive']

      elif domain == self.domains['stage']:
         return self.drives['stage_drive']

#**************************************************************************
#Exception classes
#**************************************************************************
class InvalidDomainError(Exception):
   pass

class InvalidCopyError(Exception):
   def __init__(self, filename):
      self.filename = filename

   def __str__(self):
      return repr(self.filename)

class NoDriveFoundError(Exception):
   pass
