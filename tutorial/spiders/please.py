import Queue
import os
import threading
import urllib
import uuid

from selenium import webdriver

from tutorial.spiders import testtimecrawl

# username of person who's photos you want to scrape
username = "homme__cho"

# your own credentials
myusername = "eundong933"
mypassword = "8629083e"

# path to chrome seleneium webdriver
chrome_webdriver_path = "https://www.instagram.com/homme__cho/"


def main():
    downloader = instaDownload(username, myusername, mypassword, chrome_webdriver_path)
    images = downloader.getLinks()
    downloader.tDownload(images)


class instaDownload:
    def __init__(self, username, myusername, mypassword, chrome_webdriver_path):
        self.username = username
        self.myusername = myusername
        self.mypassword = mypassword
        self.chrome_webdriver_path = chrome_webdriver_path

    def worker(self):
        while not self.q.empty():
            item = self.q.get()
            try:

                uid = uuid.uuid4()
                uid = uid.hex

                if not os.path.exists(username):
                    os.makedirs(username)

                print item
                urllib.urlretrieve(item, self.username + "/" + uid + ".jpg")
            except IOError, e:
                print("Something went wrong ", e)
            self.q.task_done()

    def tDownload(self, links):
        self.q = Queue.Queue()

        for item in links:
            self.q.put(item)

        for i in range(8):
            t = threading.Thread(target=self.worker)
            t.daemon = False
            t.start()

        self.q.join()

    def getLinks(self):
        driver = webdriver.Chrome(executable_path=self.chrome_webdriver_path)

        driver.implicitly_wait(2)

        driver.get("https://instagram.com/" + self.username + "/")

        driver.implicitly_wait(2)

        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/nav/div/div[1]/a[2]").click()

        driver.implicitly_wait(2)

        driver.find_element_by_xpath("//*[@id=\"lfFieldInputUsername\"]").send_keys(self.myusername)

        driver.find_element_by_xpath("//*[@id=\"lfFieldInputPassword\"]").send_keys(self.mypassword)

        driver.find_element_by_xpath("//*[@id=\"react-root\"]/div/div/div[2]/div/form/p[3]/input").click()

        testtimecrawl.sleep(2)

        driver.get("https://instagram.com/" + self.username + "/")

        driver.implicitly_wait(2)

        driver.find_element_by_xpath("//*[@id=\"react-root\"]/section/main/article/div/div[3]/a").click()  # meer laden

        # scrollen
        for i in range(1, 200):
            driver.execute_script("window.scrollBy(0,500)", "")
            testtimecrawl.sleep(0.15)

        images = driver.find_elements_by_css_selector("div.-cx-PRIVATE-Photo__root")

        links = []
        for image in images:
            links.append(image.get_attribute("src"))

        return links


if __name__ == "__main__":
    main()