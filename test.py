from UrlExplorer2 import UrlExplorer

domains = {'prod':'http://www.example.com/',
           'dev' : 'http://dev.example.com/',
           'stage' : 'http://stage.example.com/'}

drives = {'stage_drive': 'Z:/', 'dev_drive':'X:/'}

myexp = UrlExplorer(drives, domains)
foo = myexp.ConvertUrl('http://stage.example.com/foo/bar/index.html')
print foo
