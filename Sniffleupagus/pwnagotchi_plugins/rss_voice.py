import os
import re
import sys
import time
import logging
import random, re
import subprocess

import pwnagotchi.plugins as plugins
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts

import html

try:
    import feedparser
except Exception as e:
    logging.error("%s. Installing feedparser..." % repr(e))
    subprocess.check_call([sys.executable, "-m", "pip", "install", "feedparser"])
    logging.info("Trying to import 'feedparser' again")
    import feedparser

class RSS_Voice(plugins.Plugin):
    __author__ = 'Sniffleupagus'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Use RSS Feeds to replace canned voice messages on various events'

#     main.plugins.rss_voice.enabled = true
#     main.plugins.rss_voice.feed.wait.url = "https://www.reddit.com/r/worldnews.rss"
#     main.plugins.rss_voice.feed.bored.url = "https://www.reddit.com/r/showerthoughts.rss"
#     main.plugins.rss_voice.feed.sad.url = "https://www.reddit.com/r/pwnagotchi.rss"

    
    def __init__(self):
        self.last_checks = {"-internet-": 0, "wait" : 0}
        logging.debug("RSS_Voice plugin started")
        self.voice = ""
        self.last_voice = "wasssup!!!!"
        self.feedcache = {}

    def _wget(self, url, rssfile, verbose = False):
        logging.debug("RSS_Voice _wget %s: %s" % (rssfile, url))
        process = subprocess.run(["/usr/bin/curl", "-s", "-A", "linux:pwnagotchi_rss:v1.2.34 by %s" % self.options['reddit'], "-o", rssfile, url])
        if rssfile in self.feedcache:
            del self.feedcache[rssfile]
        logging.debug("RSS_Voice: %s", repr(process))

    def _fetch_rss_message(self, key):
        rssfile = "%s/%s.rss" % (self.options["path"], key)
        if self.voice != "":
            return self.voice

        if rssfile in self.last_checks and time.time() < (self.last_checks[rssfile] + 20):
            return self.last_checks['-MSG_%s' % rssfile]

        if os.path.isfile(rssfile):
            logging.info("RSS_Voice pulling from %s" % (rssfile))
            try:
                if rssfile in self.feedcache:
                    feed = self.feedcache[rssfile]
                else:
                    feed = feedparser.parse(rssfile)
                    self.feedcache[rssfile] = feed

                article = random.choice(feed.entries)

                def sub_element(match_obj):
                    ele = match_obj.group(1)
                    if ele in article: return article[ele]
                    else:
                        try:
                            return html.unescape(re.sub('<[^>]+>', '', eval("article[%s]" % ele)))

                        except Exception as e:
                            logging.warn(repr(e))
                            return repr(e)

                if "format" in self.options["feed"][key]:
                    headline = re.sub(r"%([^%]+)%", sub_element, self.options["feed"][key]["format"])
                    headline = html.unescape(re.sub('<[^>]+>', '', headline))
                else:
                    headline = "%s: %s" % (article.author[3:], html.unescape(re.sub('<[^>]+>', '', article.summary)))

            except Exception as e:
                headline = repr(e)

            logging.info("RSS_Voice %s: %s" % (key, headline))

            self.last_checks['-MSG_%s' % rssfile] = headline
            self.last_checks[rssfile] = time.time()

            return headline
        else:
            return ""
        
    # called when http://<host>:<port>/plugins/<plugin>/ is called
    # must return a html page
    # IMPORTANT: If you use "POST"s, add a csrf-token (via csrf_token() and render_template_string)
    def on_webhook(self, path, request):
        # do something to edit RSS urls
        pass

    # called when the plugin is loaded
    def on_loaded(self):
        logging.debug("RSS_Voice options = %s" % self.options)
        if "path" not in self.options:
            self.options['path'] = "/root/voice_rss"

        if "reddit" not in self.options:
            # add main.plugins.rss_voice.reddit = "/u/YOUR_REDDIT_NAME"
            # to config.toml.  Don't really edit it here
            self.options['reddit'] = "/u/CHANGEME-TO-GET-RSS_WORKING"

        rssdir = self.options['path']
        if not os.path.isdir(rssdir):
            logging.info("Creating directory for rss feeds: %s" % (rssdir))
            try:
                os.mkdir(rssdir)
            except Exception as e:
                logging.error("mkdir %s: %s" % (rssdir, repr(e)))

    # called before the plugin is unloaded
    def on_unload(self, ui):
        pass

    # called hen there's internet connectivity
    def on_internet_available(self, agent):
        # check rss feeds, unless too recent
        logging.info("RSS_Voice internet available")
        now = time.time()
        if now < (self.last_checks['-internet-'] + 300):
            time.sleep(5)
            return
        self.last_checks['-internet-'] = now

        if "feed" in self.options:
            feeds = self.options["feed"]
            logging.info("RSS_Voice processing feeds: %s" % feeds)
            for k,v in feeds.items():   # a feed value can be a dictionary
                logging.debug("RSS_Voice feed: %s = %s" % (repr(k), repr(v)))
                timeout = 3600 if "timeout" not in v else v["timeout"]
                logging.debug("RSS_Voice %s timeout = %s" % (repr(k), timeout))
                try:
                    if not k in self.last_checks or now > (self.last_checks[k] + timeout):
                        # update feed if past timeout since last check
                        rss_file = "%s/%s.rss" % (self.options['path'], k)
                        if os.path.isfile(rss_file) and now < os.path.getmtime(rss_file) + timeout:
                            logging.debug("too soon by file age!")
                        else:    
                            if "url" in v:
                                self._wget(v["url"], rss_file)
                                self.last_checks[k] = time.time()
                            else:
                                logging.warn("No url in  %s" % repr(v))
                    else:
                        logging.debug("too soon!")
                except Exception as e:
                    logging.error("RSS_Voice: %s" % repr(e))
        logging.info("internet_av done")


    # called when the ui is updated
    def on_ui_update(self, ui):
        # update those elements
        st = ui.get('status')
        if self.voice != "":
            logging.debug("RSS: Status to %s" % self.voice)
            ui.set('status', self.voice)
            self.last_voice = self.voice
            self.voice = ""
        elif st == "...":
            logging.debug("RSS: Status to %s" % self.voice)
            ui.set('status', self.voice)
            self.voice = self.last_voice

    # called when everything is ready and the main loop is about to start
    def on_ready(self, agent):
        self.on_internet_available(agent)
        # you can run custom bettercap commands if you want
        #   agent.run('ble.recon on')
        # or set a custom state
        #   agent.set_bored()

    # set up RSS feed per emotion
    
    # called when the status is set to bored
    def on_bored(self, agent):
        self.voice = self._fetch_rss_message("bored")

    # called when the status is set to sad
    def on_sad(self, agent):
        self.voice = self._fetch_rss_message("sad")

    # called when the agent is waiting for t seconds
    def on_wait(self, agent, t):
        self.voice = "(%ss) %s" % (int(t), self._fetch_rss_message("wait"))
        logging.debug("RSS_Voice on_wait: %s" % self.voice)


    # called when the agent is sleeping for t seconds
    def on_sleep(self, agent, t):
        self.voice = "(%ss zzz) %s" % (int(t), self._fetch_rss_message("sleep"))

