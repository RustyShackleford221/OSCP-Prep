import threading
import urllib
import urllib.request
from queue import Queue

threads = 50
target_url = "http://testphp.vulnweb.com"
wordlist_file = "all.txt" # from SVNDigger
resume = None # used in case of network connectivity failures
user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36"

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

def dir_bruter(word_queue, extensions=None):
    while not word_queue.empty():
        attempt = word_queue.get()
        attempt_list = []
        
        # check if there's a file extension, if there is not, it's a 
        # directory we're bruting
        if "." not in attempt:
            attempt_list.append("/{0}/".format(attempt))
        else:
            attempt_list.append("/{0}".format(attempt))
        # check if we want to bruteforce extensions
        if extensions is not None:
            for extension in extensions:
                attempt_list.append("/{0}{1}".format(attempt, extension))
        # iterate over our list of attempts
        for brute in attempt_list:
            url = "{0}{1}".format(target_url, urllib.request.quote(brute))
            try:
                headers = {"User-Agent":user_agent}
                r = urllib.request.Request(url, headers=headers)
                response = urllib.request.urlopen(r)
                if len(response.read()):
                    print("[{0}] =>  {1}".format(response.code, url))
            except urllib.error.URLError as e:
                if hasattr(e, "code") and e.code != 404:
                    print("!!! {0} => {1}".format(e.code, url))
                pass
            
word_queue = build_wordlist(wordlist_file)
extensions = [".php", ".bak", ".orig", ".inc"]
for i in range(0, threads):
    t = threading.Thread(target=dir_bruter, args=(word_queue, extensions,))
    t.start()