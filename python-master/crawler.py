#!/usr/bin/env python
#     __                                           _             __   _    
#    / /_  __  __   ______________ _____  __  __  (_)_  ______  / /__(_)__ 
#   / __ \/ / / /  / ___/ ___/ __ `/_  / / / / / / / / / / __ \/ //_/ / _ \
#  / /_/ / /_/ /  / /__/ /  / /_/ / / /_/ /_/ / / / /_/ / / / / ,< / /  __/
# /_.___/\__, /   \___/_/   \__,_/ /___/\__, /_/ /\__,_/_/ /_/_/|_/_/\___/ 
#       /____/                         /____/___/                          
#
###############################################################################
# Download huge collections of wordlist:#
#http://ul.to/folder/j7gmyz#
##########################################################################
#
####################################################################
# Need daylie updated proxies?#
#http://j.mp/Y7ZZq9#
################################################################
#
######################################################
#### Crawler by crazyjunkie ######
###################################################
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# Author:
# ..:: crazyjunkie ::..
#
# Changelog
# - Implemented a depth limit in crawling logic.
# - Added summary at the end of crawling with statistical data about the crawling results
# - Incresed crawl speed. 
# - Implemented HEAD method for analysing file types before crawling. 
# - Almost all from the last published version! 
#
# ToDo
# - [!] Exception inside crawl() function. While statement rise the exception.
#   <class 'httplib.IncompleteRead'>
#   ...
#   IncompleteRead(2020 bytes read, 4429 more expected)


# standar imports
import sys
import re
import getopt
import urllib2
import urlparse
import httplib
import copy
import os
import time
import socket
import datetime

import getpass

####################
# Global Variables
debug=False
vernum='1.0.1'
verbose=False
log=False
auth=False

time_responses = []

# This is for identify links in a HTTP answer
#linkregex = re.compile('[^>](?:href=|src=|content=\"http)[\'*|\"*](.*?)[\'|\"]',re.IGNORECASE)
linkregex = re.compile('[^>](?:href\=|src\=|content\=\"http)[\'*|\"*](.*?)[\'|\"].*?>',re.IGNORECASE)
linkredirect = re.compile('(?:open\\(\"|url=|URL=|location=\'|src=\"|href=\")(.*?)[\'|\"]')
linksrobots = re.compile('(?:Allow\:|Disallow\:|sitemap\:).*',re.IGNORECASE)
information_disclosure = re.compile('(?:<address>)(.*)[<]',re.IGNORECASE)


# HTTP Response Codes
# -------------------
error_codes={}
error_codes['0']='Keyboard Interrupt exception'
error_codes['1']='Skypping url'
error_codes['-2']='Name or service not known'
error_codes['22']='22 Unknown error'
error_codes['104']='104 Connection reset by peer'
error_codes['110']='110 Connection timed out'
error_codes['111']='111 Connection refused'
error_codes['200']='200 OK'
error_codes['300']='300 Multiple Choices'
error_codes['301']='301 Moved Permanently'
error_codes['302']='Moved'
error_codes['305']='305 Use Proxy'
error_codes['307']='307 Temporary Redirect'
error_codes['400']='400 Bad Request'
error_codes['401']='401 Unauthorized'
error_codes['403']='403 Forbidden'
error_codes['404']='404 Not Found'
error_codes['405']='405 Method Not Allowed'
error_codes['407']='407 Proxy Authentication Required'
error_codes['408']='408 Request Timeout'
error_codes['500']='500 Internal Server Error'
error_codes['503']='503 Service Unavailable'
error_codes['504']='504 Gateway Timeout'
error_codes['505']='505 HTTP Version Not Supported'
error_codes['9999']='Server responds with a HTTP status code that we do not understand'


# End of global variables
###########################


# Print version information and exit
def version():
	"""
	This function prints the version of this program. It doesn't allow any argument.
	"""
	print "+----------------------------------------------------------------------+"
    	print "| "+ sys.argv[0] + " Version "+ vernum +"                              |"
	print "| This program is free software; you can redistribute it and/or modify |"
	print "| it under the terms of the GNU General Public License as published by |"
	print "| the Free Software Foundation; either version 2 of the License, or    |"
	print "| (at your option) any later version.                                  |"
	print "|                                                                      |"
	print "| Author: ..:: crazyjunkie ::..                                        |"
	print "+----------------------------------------------------------------------+"
	print

# Print help information and exit:
def usage():
	"""
	This function prints the posible options of this program.

	No parameters are needed.
	"""
	print "+----------------------------------------------------------------------+"
	print "| "+ sys.argv[0] + " Version "+ vernum +"                              |"
	print "| This program is free software; you can redistribute it and/or modify |"
	print "| it under the terms of the GNU General Public License as published by |"
	print "| the Free Software Foundation; either version 2 of the License, or    |"
	print "| (at your option) any later version.                                  |"
	print "|                                                                      |"
	print "| Author: ..:: crazyjunkie ::..                                        |"
	print "+----------------------------------------------------------------------+"
	print 
	print "\nUsage: %s <options>" % sys.argv[0]
	print "Options:"
    	print "  -h, --help                           Show this help message and exit"
      	print "  -V, --version                        Output version information and exit"
	print "  -v, --verbose                        Be verbose"
        print "  -D, --debug                          Debug"
	print "  -u, --url                            URL to start crawling"
        print "  -w, --write                          Save crawl output to a local file"
        print "  -L, --common-log-format              Generate log of the requests in CLF"
        print "  -e, --export-file-list               Creates a file with all the URLs to found files during crawling. You can use wget to download the entire list"
        print "  -l, --crawl-limit                    Maximum links to crawl"
	print "  -C, --crawl-depth                    Limit the crawling depth according to the value specified. Ex.: -C 2. "
	print "  -d, --download-file                  Specify the file type of the files to download: png,pdf,jpeg,gif,css,x-javascript,x-shockwave-flash"
        print "  -i, --interactive-download           Before downloading files allow user to specify manually the type of files to download"
        print "  -U, --usuario                        User name for authentication"
        print "  -P, --password                       Request password for authentication"
	print
	print "Example: python crawler.py -u http://www.example.com -w -C 10 -i "
	print
	sys.exit(1)

def printout(input_text,output_file):

	"""
	To main functionalities are covered in this function:
	1. Prints a text in the stdout
	2. Write a text in the given file. 

	Not return any value.
	"""

	global debug
	global verbose

	try:
		print input_text 
		if output_file:
			try:
				output_file.write(input_text+'\n')
			except:
				print '[!] Not saving data in output' 

        except Exception as inst:
		print '[!] Exception in printout() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1

def check_url(url):

	"""
	This function verifies that the given 'url' is well formatted, this means that it has defined a protocol and a domain. 
	The urlparse.urlparse() function is used. 

	The return values can be 'True'/'False'.
	"""

	global debug
	global verbose

	try:
		url_parsed = urlparse.urlparse(url)
		if url_parsed.scheme and url_parsed.netloc:
			return True
		else:
			return False

        except Exception as inst:
		print '[!] Exception in check_url() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1

def encode_url(url):

	"""
	This function encode the URL according to Percentage or URL encoding.  
	Actually only replaces a 'space' to '%20'.

	Returns an URL.
	"""

	global debug
	global verbose

	url_encoded = ""
	try:	
		url_encoded = url.replace(" ","%20")
		#url_encoded = url_encoded.replace("&amp;","&")
		
		return url_encoded

        except Exception as inst:
		print '[!] Exception in encode_url() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1

def log_line(request, response_code, response_size,log_file):

	"""
	This function generates an output line of a given HTTP request in CLF (Common Log Format)

	Not return any value.
	"""

	global debug
	global verbose

	try:
		try:
			if response_size == -1:
				content_size = '-'
			else:
				content_size = str(response_size)
			local_hostname = socket.gethostname()
			local_user = os.getenv('USER')
			timestamp = time.strftime('%e/%b/%Y:%X %z').strip()
			method = request.get_method()
			protocol = 'HTTP/1.1'	# This is the version of the protocol that urllib2 uses
			user_agent = request.get_header('User-agent')
			url = request.get_full_url()
			
			# COMMON LOG FORMAT
			log_file.write(local_hostname+' '+'-'+' '+local_user+' '+'['+timestamp+']'+' '+'"'+method+' '+url+' '+protocol+'"'+' '+str(response_code)+' '+content_size+' "-" "'+user_agent+'"\n')

			# URLSNARF FORMAT
			#log_file.write(local_hostname+' '+'- - '+'['+timestamp+']'+' '+'"'+method+' '+url+' '+protocol+'"'+' - - "-" "'+user_agent+'"\n')
		except:
			print 'Not logging the following request: {0}'.format(request.get_full_url())

	except Exception as inst:
		print '[!] Exception in log_line() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y

def get_url(url, host, username, password, download_files_flag):

	"""
	This function does a HTTP request of the given URL using the urllib2 python library. 

	Returns two values: [request,response]
	"""

	global debug
	global verbose
	global auth

	#Vector to save time responses of each request. For now it is a global variable.
	global time_responses


	starttime=0
	endtime=0
	handler=""

	try:
		try:
			starttime= time.time()

			url = encode_url(url)
			if debug:
				print 'Encoded URL: '+url
			request = urllib2.Request(url)
			request.add_header('User-Agent','Mozilla/4.0 (compatible;MSIE 5.5; Windows NT 5.0)')
			
			if auth:
				password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
				password_manager.add_password(None, host, username, password)

				handler = urllib2.HTTPBasicAuthHandler(password_manager)

			if not download_files_flag:
				#First we do a head request to see the type of url we are going to crawl
				request.get_method = lambda : 'HEAD'

				if handler:
					opener_web = urllib2.build_opener(handler)
				else: 
					opener_web = urllib2.build_opener()

				response = opener_web.open(request)

				# If it is a file, we don get the content
				if 'text/html' not in response.headers.typeheader:
					opener_web.close()
					
					endtime= time.time()
					time_responses.append(endtime-starttime)

					return [request,response]
			
			request.get_method = lambda : 'GET'
			if handler:
				opener_web = urllib2.build_opener(handler)
			else: 
				opener_web = urllib2.build_opener()

			response = opener_web.open(request)

			opener_web.close()

			endtime= time.time()
			time_responses.append(endtime-starttime)

			return [request,response]


                except urllib2.HTTPError,error_code:
			return [request,error_code.getcode()]
		except urllib2.URLError,error_code:
			error = error_code.args[0]
			return [request,error[0]]
		except socket.error,error_code:
			error = error_code.args[0]
			try:
				error = error[0]
			except:
				pass
			return [request,error]
			
	except KeyboardInterrupt:
		try:
			print '\t[!] Press a key to continue' 
			raw_input()
			return ["",1]
		except KeyboardInterrupt:
			return ["",0]
        except Exception as inst:
		print '[!] Exception in get_url() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1	

def get_links(link_host, link_path, content):

	"""
	This function uses a regular expresion to find links in a HTML source page. 
	The regular expresion used is defined in the 'linkregex' variable.

	Returns a vector of extracted links
	"""

	global debug
	global verbose
	global linkregex

	try:
		# We obtain the links in the given response
		links = linkregex.findall(content)

		# We analyze each link 
		for link in links:
			try:
				link_clean = link.strip(' ')
			except:
				print 'error'
			parsed_link = urlparse.urlparse(link_clean)
			if not parsed_link.scheme and not parsed_link.netloc:
				if link_clean.startswith('/'):
					if link_host.endswith('/'):
						links[links.index(link)] = link_host.rstrip('/')+link_clean
					else:
						links[links.index(link)] = link_host+link_clean
				elif link_clean.startswith('./'):
						links[links.index(link)] = link_host+link_clean
				else:
					links[links.index(link)] = link_path+link_clean
			else:
				links[links.index(link)] = link_clean

		for link in links:
			links[links.index(link)] = link.split('#')[0]

		return links

        except Exception as inst:
		print '[!] Exception in get_links() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1

def crawl(url,usuario,password,output_filename,crawl_limit=0,log=False,log_filename='none',crawl_depth=0):
	
	"""
	Crawl a given url using a breadth first exploration. 

	The function returns the following values: [links_crawled, urls_not_crawled, links_to_files]
	"""

	global debug
	global verbose
	global error_codes
	
	# Vector that stores the remaining URLs to crawl
	urls_to_crawl = []
	urls_not_crawled = []
	links_crawled = []
	links_extracted = []
	files=[]
	crawl_limit_flag=False

	urls_to_crawl.append(url)

	if (crawl_limit>0):
		crawl_limit_flag=True
	if crawl_depth > 0:
		crawl_depth = crawl_depth + 3
	try:
		printout('[+] Site to crawl: '+url,output_filename)
		printout('[+] Start time: '+str(datetime.datetime.today()),output_filename)
		if output_filename:
			printout('[+] Output file: '+output_filename.name,output_filename)
		if log:
			printout('[+] Common log format output: '+log_filename.name,output_filename)

		printout('',output_filename)
		printout('[+] Crawling',output_filename)

		while urls_to_crawl:
			if crawl_limit_flag:
				if (len(links_crawled) >= crawl_limit):
					break
			try:
				# We extract the next url to crawl
				url = urls_to_crawl[0]
				urls_to_crawl.remove(url)

				# Here we limit the crawl depth
				if crawl_depth > 0:
					if url.endswith('/'):
						if url.rpartition('/')[0].count('/') >= crawl_depth:
							continue
					elif url.count('/') >= crawl_depth:
							continue

				# We add the url to the links crawled
				links_crawled.append(url)

				# We print the URL that is being crawled
				printout('   [-] '+str(url),output_filename)

				# We extract the host of the crawled URL	
				parsed_url = urlparse.urlparse(url)
				host = parsed_url.scheme + '://' + parsed_url.netloc

				if parsed_url.path.endswith('/'):
					link_path = host + parsed_url.path
				else:
					link_path = host + parsed_url.path.rpartition('/')[0] + '/'

				# We obtain the response of the URL
				[request,response] = get_url(url,host,usuario, password,False)

				# If there is a response
				if response:
					#If the server didn't return an HTTP Error
					if not isinstance(response, int):
						content = response.read()

						if log:
							log_line(request,response.getcode(),len(content),log_filename)

						# We print the file type of the crawled page
						if response.headers.typeheader:
							# If it isn't an HTML file
							if 'text/html' not in response.headers.typeheader:
								if url not in files:
									files.append([url,str(response.headers.typeheader.split('/')[1].split(';')[0])])
								if verbose:
									printout('\t[-] ('+str(response.getcode())+') '+str(response.headers.typeheader),output_filename)
							else:
								#if verbose:
								#	printout('\t[-] ('+str(response.getcode())+') '+str(response.headers.typeheader),output_filename)

								links_extracted = get_links(host, link_path, content)
								links_extracted.sort()

								# We add new links to the list of urls to crawl
								for link in links_extracted:
									if debug:
										print '\t   [i] {0}'.format(link)
									parsed_link= urlparse.urlparse(link)
									link_host = parsed_link.scheme + '://' + parsed_link.netloc

									# We just crawl URLs of the same host
									if link_host == host:
										if link not in links_crawled and link not in urls_to_crawl:
											urls_to_crawl.append(link)
									elif link not in urls_not_crawled:
										urls_not_crawled.append(link)
					else:
						# We print the error code if neccesary
						printout('\t[i] '+error_codes[str(response)],output_filename)
						if log:
							log_line(request,response,-1,log_filename)
				else:
					if response==1:
						continue
					if response==0:
						print '[!] Skypping the rest of the urls'
						break

			except KeyboardInterrupt:
				try:
					print '[!] Press a key to continue' 
					raw_input()
					continue
				except KeyboardInterrupt:
					print '[!] Exiting'
					break	

			except Exception as inst:
				print '[!] Exception inside crawl() function. While statement rise the exception.'
				print type(inst)     # the exception instance
				print inst.args      # arguments stored in .args
				print inst           # __str__ allows args to printed directly
				x, y = inst          # __getitem__ allows args to be unpacked directly
				print 'x =', x
				print 'y =', y
				print 'Response: {0}'.format(response)
				break
		
		printout('[+] Total urls crawled: '+str(len(links_crawled)),output_filename)
		printout('',output_filename)

		return [links_crawled,urls_not_crawled,files]

	except KeyboardInterrupt:
		try:
			print '[!] Press a key to continue' 
			raw_input()
			return 1
		except KeyboardInterrupt:
			print '[!] Keyboard interruption. Exiting'
			return 1
       
	except Exception as inst:
		print '[!] Exception in crawl() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1

def external_links(root_url,external_vector,output_filename):
	
	"""
	This function detects external links from a lists of given URLs. The links not maching the root URL are considered as external.

	Not return any values. 
	"""

	global debug
	global verbose

	external_websites = []

	try:
		parsed_url = urlparse.urlparse(root_url)
		link_host = parsed_url.scheme + '://' + parsed_url.netloc
		domain = parsed_url.netloc.split('www.')[-1]

		printout('',output_filename)
		printout('[+] Related subdomains found: ',output_filename)
		tmp=[]
		for link in external_vector:
			parsed = urlparse.urlparse(link)
			if domain in parsed.netloc:
				subdomain = parsed.scheme+'://'+parsed.netloc
				if subdomain not in tmp:
					tmp.append(subdomain)
					printout('   [-] '+subdomain,output_filename)
		printout('[+] Total:  '+str(len(tmp)),output_filename)
       
		printout('',output_filename)
		printout('[+] Email addresses found: ',output_filename)
		for link in external_vector:
			if 'mailto' in urlparse.urlparse(link).scheme:
				printout('   [-] '+link.split(':')[1].split('?')[0],output_filename)
        
		printout('',output_filename)
		printout('[+] This website have references to the following websites: ',output_filename)
		for link in external_vector:
			parsed = urlparse.urlparse(link)
			if parsed.netloc:
				if domain not in parsed.netloc:
					external_domain = parsed.scheme+'://'+parsed.netloc 
					if external_domain not in external_websites:
						external_websites.append(external_domain)
		external_websites.sort()
		for link in external_websites:
			printout('   [-] '+link,output_filename)
		printout('[+] Total:  '+str(len(external_websites)),output_filename)
      
	except Exception as inst:
		print '[!] Exception in external_links() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1


def indexing_search(usuario, password,links_vector,output_filename):

	"""
	This function identifies directories and search for indexing in them from a given list of URLs.

	This function returns the following values: [directories found, directories_with_indexing]
	"""
	
	global debug
	global verbose
	global error_codes

	directories=[]
	indexing=[]
	request=""
	response=""

	title_start_position = -1
	title_end_position = -1
	title=""

	try:

		# Identifying directories
		for i in links_vector:
			while ( len(i.split('/')) > 4 ):
				i=i.rpartition('/')[0]
				if ( ( i+'/' )  not in directories ):
					directories.append(i+'/')

		# We sort the directories vector for proper visualization of the data
		directories.sort()
		
		printout('[+] Directories found:',output_filename)
		for directory in directories:
			printout('   [-] '+directory,output_filename)
		printout('[+] Total directories: '+str(len(directories)),output_filename)
		printout('',output_filename)

		printout('[+] Directory with indexing',output_filename)
		dots='.'
		for directory in directories:
			sys.stdout.flush()
			sys.stdout.write('\r\x1b'+dots)
			if len(dots)>30:
				dots='.'
			dots=dots+'.'
			try:
				# We extract the host of the crawled URL	
				parsed_url = urlparse.urlparse(directory)
				host = parsed_url.scheme + '://' + parsed_url.netloc
				
				# We obtain the response of the URL
				[request,response] = get_url(directory, host, usuario, password,False)		

				# If there is a response                                			
				if response:
					#If the server didn't return an HTTP Error      		
					if not isinstance(response, int):
						content = response.read()

						title_start_position = content.find('<title>')
						if title_start_position != -1:
							title_end_position = content.find('</title>', title_start_position+7)
						if title_end_position != -1:
							title = content[title_start_position+7:title_end_position]

						if title:
							if title.find('Index of') != -1:
								printout('\n   [!] '+directory,output_filename)
								indexing.append(directory)
							elif verbose:
								printout('   [-] '+directory,output_filename)

					else:
						if debug:
							# We print the error code if neccesary
							printout('   [-] '+directory+' ('+error_codes[str(response)]+')',output_filename)
				else:
					if response==1:
						continue
					if response==0:
						print '[!] Skypping the rest of the directories'
						break

			except KeyboardInterrupt:
				try:
					print '[!] Press a key to continue' 
					raw_input()
					pass
				except KeyboardInterrupt:
					print '[!] Exiting'
					break	

		printout('\n[+] Total directories with indexing: '+str(len(indexing)),output_filename)
		printout('',output_filename)

		return [directories,indexing]

	except Exception as inst:
		print '[!] Exception in indexing_search() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return 1

def report_files(export_file_list,files_vector,output_filename):
	
	"""
	This function export in a output file a list of the URLs of the found files during crawling.
	"""

	global debug
	global verbose

	try:
		if len(files_vector)>0:
			printout('[+] Files found:',output_filename)
			if export_file_list:
				try:
					local_file = open(output_name.rpartition('.')[0]+'.files','w')
					printout('[+] Exporting list of files found to: '+output_name.rpartition('.')[0]+'.files',output_filename)
				except OSError,error:
					if 'File exists' in error:
							printout('[+] Exporting list of files found to: '+output_name.rpartition('.')[0]+'.files',output_filename)
							pass
					else:
						print '[+] Error creating output file to export list of files.'
						export_file_list=False
			
			# We print the files found during the crawling
			for [i,j] in files_vector:
				printout('   [-] '+str(i)+'  ('+str(j)+')',output_filename)
				if export_file_list:
					local_file.write(i+'\n')
			printout('[+] Total files: '+str(len(files_vector)),output_filename)

		if export_file_list:
			local_file.close()

	except Exception as inst:
		print '[!] Exception in report_files() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return 1

def download_files(extensions_to_download,files_vector,usuario,password,interactive_flag,output_filename):

	"""
	This function downloads a set of files which extensions match with the given in extensions_to_download.
	If the interactive_flag is set on True, then the user can select manually the files to download choosing from the files 
	extensions found during crawling.

	This function returns a list of extensions in the found files during crawling.
	"""

	global debug
	global verbose

	list_of_files_to_download=[]
	extensions_found=[]

	try:
		if len(files_vector)>0:
			# Looking for the types of files found during crawling	
			for [i,j] in files_vector:
				if j not in extensions_found:
					extensions_found.append( j )

			#If the interactive mode is enabled, we ask user which files to downlaod
			if interactive_flag:
			 	print	
				print '[+] Starting to download files'
				print '[+] The following files were found during crawling:'
				print '   ',
				print extensions_found
				print '    Select next wich type of files you want to download. Ex.: png,pdf,css.'
				extensions_to_download= raw_input('    ')

			# Looking for files matching the download criteria	
			for [i,j] in files_vector:
				if (j in extensions_to_download):
					list_of_files_to_download.append(i)	

			#  If there is at least one file matching the download criteria, we create a output directory and download them
			if ( len(list_of_files_to_download) > 0 ):
				# Fetching found files
				printout('',output_filename)
				printout('[+] Downloading specified files: '+extensions_to_download,output_filename)
				printout('[+] Total files to download: '+str(len(list_of_files_to_download)),output_filename)

				# Creating output directory download files
				try:
					output_directory = output_name.rpartition('.')[0]+'_files'
					os.mkdir(output_directory)
					printout('[+] Output directory: '+output_directory,output_filename)
				except OSError, error:
					if 'File exists' in error:
						print '\n[!] Directory already exists. Press a key to ovewrite or CTRL+C cancel download'
						try:
							raw_input()
							printout('[+] Output directory: '+output_directory,output_filename)
						except KeyboardInterrupt:
							printout('\n[+] Download files aborted',output_filename)
							return 1 
					else:
						printout('\n[!] Download files aborted. Error while creating output directory.',output_filename)


				#Downloading files
				for i in list_of_files_to_download:
					printout('   [-] '+i,output_filename)

					# We extract the host of the crawled URL	
					parsed_url = urlparse.urlparse(i)
					host = parsed_url.scheme + '://' + parsed_url.netloc

					[request,response] = get_url(i.replace(' ','%20'), host, usuario, password, True)		


					if response:
						if not isinstance(response, int):
							response = response.read()
							try:
								local_file=open(output_directory+'/'+i.rpartition('/')[2],'w')
							except OSError, error:
								if 'File exists' in error:
									pass
								else:
									printout('   [-] Impossible to create output file for: '+output_directory+'/'+i.rpartition('/')[2],output_filename)

							if local_file:
								local_file.write(response)
								local_file.close()

			printout('[+] Download complete',output_filename)
			printout('',output_filename)

			return extensions_found
					
	except Exception as inst:
		print '[!] Exception in download_files() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1

####################	
#STATISTICS FUNCTION
####################
def statistics(global_time, directories, indexing, links_crawled, files, extensions_found, output_filename):
	global debug
	global verbose
	global time_responses
	
	queries_time = 0 
	avg_time_per_query = 0
	amt_files_per_extension = {}

	try:
		print

		if len(links_crawled) > 1:
			# Calculating avg time per query
			for i in time_responses:
				queries_time = queries_time + i
			try:
				avg_time_per_query = (queries_time / len(time_responses))
			except:
				avg_time_per_query = 0

			# Calculating incidence of files
			for [link,extension] in files:
				amt_files_per_extension[extension] = 0
			for [link,extension] in files:
				amt_files_per_extension[extension] += 1

			print '___________'
			print
			print 'Summary'
			print '___________'
			print
			if output_filename:
				print '[+] Output file stored at: {0}'.format(os.path.realpath(output_name))
				print
			print '[+] Total elapsed time: {0} seconds ({1} min)'.format(round(global_time,2),round((global_time/60),2))
			print '[+] AVG time per query: {0} seconds'.format(round(avg_time_per_query,2))
			print
			print '[+] Total links crawled\t{0}'.format(str(len(links_crawled)-len(files)))
			print '[+] Total directories\t{0}'.format(str(len(directories)))
			print '   [-] Indexing\t{0}'.format(str(len(indexing)))
			print '[+] Total found files\t{0}'.format(str(len(files)))
			for key in amt_files_per_extension.keys():
				print '       | '+key+'\t'+str(amt_files_per_extension[key])


	except Exception as inst:
		print '[!] Exception in statistics() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		return -1


##########
# MAIN
##########
def main():

	global debug
	global verbose
	global log
	global auth
	global output
	global output_name

	url_to_crawl = ""
	usuario = "crawler123"
	password = "crawler123"
	crawl_limit = 0
	extensions_to_download = "" 
	download_files_flag=False
	export_file_list = False
	interactive_flag=False

	starttime=0
	endtime=0

	#Data lists
	directories = []
	indexing = []
	links_crawled = []
	externals_url_vector = []
	files_vector = []
	extensions_found = []
	crawl_depth = 0
	save_output=False
	output_name = ""
	output_file = ""
	log_name = ""
	log_file = ""

	try:

		# By default we crawl a max of 5000 distinct URLs
		opts, args = getopt.getopt(sys.argv[1:], "hVDwu:vLU:Pl:[d:]eiC:", ["help","version","debug","write","url=","verbose","common-log-format","usuario=","password","crawl-limit=","[download-file=]","export-file-list","interactive-download","crawl-depth="])


	except getopt.GetoptError: usage()	

	for opt, arg in opts:
		if opt in ("-h", "--help"): usage()
		if opt in ("-V", "--version"): version();exit(1)
		if opt in ("-D", "--debug"): debug=True
		if opt in ("-w", "--write"): save_output=True
		if opt in ("-u", "--url"): url_to_crawl = arg
		if opt in ("-v", "--verbose"): verbose = True
		if opt in ("-L", "--common-log-format"): log = True
		if opt in ("-U", "--usuario"): usuario = arg
		if opt in ("-P", "--password"): password = getpass.getpass() ; auth = True
		if opt in ("-l", "--crawl-limit"): crawl_limit = int(arg) 
		if opt in ("-d", "--download-file"): extensions_to_download = arg ; download_files_flag=True
		if opt in ("-i", "--interactive-download"): interactive_flag=True
		if opt in ("-e", "--export-file-list"): export_file_list = True
		if opt in ("-C", "--crawl-depth"): crawl_depth = arg
	try:

		if debug:
			print '[+] Debugging mode enabled'

		if check_url(url_to_crawl):

			date = str(datetime.datetime.today()).rpartition('.')[0].replace('-','').replace(' ','_').replace(':','')
			if save_output:
				output_name = urlparse.urlparse(url_to_crawl).netloc+'.crawler'
				try:
					output_file = open(output_name,'w')
				except OSError, error:
					if 'File exists' in error:
						pass
					else:
						output_name = ""
			else:
				output_name = ""
			
			if log:
				log_name = date +'_'+ urlparse.urlparse(url_to_crawl).netloc + '.log'
				try:
					log_file = open(log_name,'w')
				except OSError, error:
					if 'File exists' in error:
						pass
					else:
						log=False

			starttime=time.time()

			# Crawl function
			[links_crawled,externals_url_vector, files_vector] = crawl(url_to_crawl, usuario, password, output_file, crawl_limit, log,log_file,int(crawl_depth))
			
			# Indexing search
			[directories, indexing] = indexing_search(usuario, password,links_crawled,output_file)
			
			# Printing found files and exporting files to an output file
			report_files(export_file_list,files_vector,output_file)

			# Searching for external links
			external_links(url_to_crawl,externals_url_vector,output_file)
			
			# Download files
			if download_files_flag or interactive_flag:
				extensions_found = download_files(extensions_to_download,files_vector,usuario,password,interactive_flag,output_file)
			
			printout('',output_file)
			printout('[+] End time: '+str(datetime.datetime.today()),output_file)

			endtime=time.time()
			# Printing statistics
			statistics(endtime-starttime,directories,indexing,links_crawled,files_vector,extensions_found,output_name)

			try:
				output_file.close()
			except:
				pass
			try:
				log_file.close()
			except:
				pass

		else:
			print
			print '[!] Check the URL provided, it should be like: http://www.example.com or http://asdf.com'
			print
			usage()

	except KeyboardInterrupt:
		# CTRL-C pretty handling
		print 'Keyboard Interruption!. Exiting.'
		sys.exit(1)
	except Exception as inst:
		print '[!] Exception in main() function'
		print type(inst)     # the exception instance
		print inst.args      # arguments stored in .args
		print inst           # __str__ allows args to printed directly
		x, y = inst          # __getitem__ allows args to be unpacked directly
		print 'x =', x
		print 'y =', y
		sys.exit(1)


if __name__ == '__main__':
	main()
