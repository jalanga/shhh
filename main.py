# !/usr/bin/env python3
import os
import random
import threading
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class Views:

    def __init__(self):
        self.views = 0
        self.votes = 0
        self.proxy_ct = 0
        self.proxies = []
        self.time_sleep = int(os.getenv('TIME_SLEEP', 10))
        self.coin_link = os.getenv("COIN_LINK", "https://coinmarketcap.com/currencies/pornrocket/")
        self.workers = int(os.getenv("WORKERS", 3))
        self.get_proxies()
        self.do()

    def get_proxies(self):

        with open('proxies.txt') as f:
            lines = f.readlines()
            for line in lines:
                self.proxies.append(line.strip())

    def get_proxy(self):
        if self.proxies:
            if self.proxy_ct >= len(self.proxies):
                self.proxy_ct = 0
            proxy_ip = self.proxies[self.proxy_ct]
            self.proxy_ct += 1
            return proxy_ip

    def do(self):
        while True:
            for i in range(self.workers):
                threading.Thread(target=self.spawn).start()
                time.sleep(5)
            time.sleep(self.time_sleep + 4)

    @staticmethod
    def get_random_ua():
        agents = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36'
        ]

        return random.choice(agents)

    def spawn(self):
        try:
            proxy_ip = self.get_proxy()

            profile = webdriver.FirefoxProfile()

            proxy = None
            if proxy_ip:
                proxy = Proxy(
                    {
                        'proxyType': ProxyType.MANUAL,
                        'httpProxy': proxy_ip,
                        'ftpProxy': proxy_ip,
                        'sslProxy': proxy_ip,
                    }
                )

                profile.set_preference("network.proxy.type", 1)
                profile.set_preference("network.proxy.https", proxy_ip.split(':')[0])
                profile.set_preference("network.proxy.https_port", proxy_ip.split(':')[1])

            profile.set_preference("general.useragent.override", self.get_random_ua())
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
            profile.set_preference("media.peerconnection.enabled", False)

            # save to FF profile
            profile.update_preferences()

            browser = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                browser_profile=profile,
                proxy=proxy
            )
            browser.delete_all_cookies()

            browser.get(self.coin_link)

            try:
                WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'cmc-logo')))
                print("Page is ready!")
                self.views += 1
                browser.execute_script("window.scroll({top: 2000});")

                time.sleep(3)
                buttons = browser.find_elements_by_class_name('cmc-button')
                if buttons:
                    buttons[0].click()
                    print("Voted")
                    self.votes += 1
            except TimeoutException:
                print("Loading took too much time!")

            time.sleep(self.time_sleep)
            browser.quit()
            print('-------------------')
            print("Views: %d" % self.views)
            print("Votes: %d" % self.votes)
            print('-------------------')
        except Exception:
            pass

Views()
