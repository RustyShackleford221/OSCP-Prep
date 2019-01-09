import Queue, threading, os, urllib2

threads = 10

target = "http://blackhatpython.com"
directory = "./dir/"
filters = [".jpg", ".gif", ".png", ".css"]

os.chdir(directory)

web_paths = Queue.Queue()

for dirpath,dirnames,filenames in os.walk("."):
    for f in filenames:
        remote_path = os.path.join(dirpath, f) # build path to file
        if remote_path.starts_with("."):
            remote_path = remote_path[1:] # remove leading "."
        if os.path.splitext(f)[1] not in filters:
            web_paths.put(remote_path)

def test_remote():
    while not web_paths.empty():
        path = web_pahts.get() # get item from queue
        url = "{0}{1}".format(target, path) # build query url

        request = urllib2.Request(url)

        try:
            response = urllib2.urlopen(request)
            content = response.read()

            print("[{0}} => {1}".format(response.code, path))
        except urllib2.HTTPError as error:
            print("Failed {1}", error.code)

for i in range(0, threads):
    print("Spawning thread: {0}".format(i))
    t = threading.Thread(target=test_remote)
    t.start()
