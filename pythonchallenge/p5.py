# Answer: channel (needed hit)
import urllib2, pickle
banner_data = urllib2.urlopen("http://www.pythonchallenge.com/pc/def/banner.p").read()
banner_obj = pickle.loads(banner_data)
banner = ""
for line in banner_obj:
   for item in line:
      banner += item[0]*item[1]
   banner += "\n"
print banner
