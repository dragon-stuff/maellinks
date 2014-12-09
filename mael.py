import requests
import lxml.html
import requests_cache
import re
from collections import Counter
requests_cache.install_cache()

regexes = [r"v[=/](.{11})[&#;?%].*",
           r"v[=/](.{11})$",
           r"embed.(.{11})$",
           r"embed.(.{11})[&#;?%].*",
           r"watch.(.{11})$",
           r"vid=(.{11})[&#;?%].*",
           r"vid=(.{11})$",
           r"user/.*/(.{11})$"]

def get_youtube_id(url):
    for regex in regexes:
        m = re.search(regex, url.strip())
        if m:
            for match_text in m.groups():
                return match_text

def scrape(c):
    r = requests.get(c)
    root = lxml.html.fromstring(r.content)
    candidates = root.xpath("//a[contains(@href, 'youtube.com/')]/@href")
    for c in candidates:
        cc = get_youtube_id(c)
        if cc:
            yield cc




url = "http://www.maelfroth.org/links.php"
r = requests.get(url)
root = lxml.html.fromstring(r.content)
root.make_links_absolute(url)

candidates = root.xpath("//a[contains(@href, url)]/@href".format(url))

bag=Counter()
for c in candidates:
    if '%23maelfroth' not in c:
        # print "ignoring", c  # TODO: not filtering maelfroth at mo!
        continue
    for youtube_id in scrape(c):
        #bag.add(youtube_id)
        bag[youtube_id] += 1

print bag.most_common(20)


