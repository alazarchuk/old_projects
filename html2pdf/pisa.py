import sx.pisa3
import urllib2
import sys
import os
import logging

logging.basicConfig(stream=sys.stdout, level=10)

def print_params(*args, **kargs):
	print "+"*60
	print args
	print kargs
	print "+"*60
	#return args[0]

src = urllib2.urlopen('http://highscalability.com/scaling-mania-mysql-conference-2008/')

if src.headers.has_key('content-type'):
    #encoding = src.headers['content-type'].split('charset=')[1]
    encoding = None
else:
    encoding = None

content = src.read()


resfile = open('mysql.pdf', "wb")
pdf = sx.pisa3.pisaDocument(content, resfile,  encoding=encoding, errout = sys.stdout, show_error_as_pdf = True, link_callback=print_params)
print "*"*20
print pdf.err
resfile.close()

os.system("evince " + resfile.name)
