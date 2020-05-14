from selenium import webdriver
from selenium.common import exceptions as exception
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait as w8

import SwiperModules.loginDataEncrypter as loginData


class SeleniumSwiper:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument('start-maximized')
        self.driver = webdriver.Chrome(options=options)

    # Function to simulate user staring
    def real_user_stare(self, x=1):
        import random
        from time import sleep
        sleep(random.uniform(1.5 * x, 4 * x))

    # obvious. requires encrypted mail and password with key (run PasswordEncrypt if throws errors)
    def Facebook_login(self):
        self.driver.get("https://facebook.com")
        self.real_user_stare()
        key, mail, passwd = self.read_from_files()
        from cryptography.fernet import Fernet
        f = Fernet(key)
        self.driver.find_element_by_id("email").send_keys(f.decrypt(mail).decode())
        self.driver.find_element_by_id("pass").send_keys(f.decrypt(passwd).decode())
        self.driver.find_element_by_id("pass").submit()
        # return self.driver

    # requres to be logged in on facebook
    def Tinder_login(self):
        self.driver.get("https://tinder.com")
        more_options_button = w8(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[3]/span/button')))
        self.real_user_stare()
        try:
            btn = self.driver.find_element_by_xpath("//button[@aria-label='Log in with Facebook']").click()
        except exception.NoSuchElementException:

            self.driver.find_element_by_css_selector(".Fw\(\$medium\)").click()
            try:
                btn = self.driver.find_element_by_xpath("//button[@aria-label='Log in with Facebook']").click()
            except exception:
                self.driver.refresh()
                self.real_user_stare()
                self.Tinder_login()

    # helper function to het variables from encrypted files, used while logging in to facebook
    def read_from_files(self):
        while True:
            try:
                file = open('./key.key', 'rb')
                key = file.read()
                file.close()
                file = open('./passwd.key', 'rb')
                passwd = file.read()
                file.close()
                file = open('./mail.key', 'rb')
                mail = file.read()
                file.close()
            except FileNotFoundError:
                loginData.encrypt()
                continue
            break
        return key, mail, passwd

    # closes popups after loging on tinder
    def Close_popup(self):
        i = 1
        while i != 0:
            self.real_user_stare(2)  # doesn't work as expected
            try:
                popup1 = self.driver.find_element_by_xpath(
                    '//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
            except exception.NoSuchElementException:
                i = 0

    # swiper function

    def Swipe_it(self, result):
        if self.driver.find_element_by_xpath('//*[contains(text(), "You\'re Out of Likes!")]').is_displayed():
            i = 0
            print("Tinder doesn\'t want me to date :<")
            return False
        try:
            btn_noThanks = self.driver.find_element_by_xpath("//*[contains(text(), 'No Thanks')]").click()
        except exception.ElementNotInteractableException:
            try:
                if (result > 0.5):
                    like_button = w8(self.driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Like']"))).click()
                else:
                    dislike_button = w8(self.driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Nope']"))).click()
            except exception.ElementClickInterceptedException:
                try:
                    match_button = self.driver.find_element_by_xpath("//*[contains(text(), 'Keep Swiping')]").click()
                except exception.ElementNotInteractableException:
                    try:
                        not_interessted_button = self.driver.find_element_by_xpath(
                            "//*[contains(text(), 'Not interested')]").click()
                    except exception.ElementClickInterceptedException:
                        self.real_user_stare(4)
        except exception.ElementClickInterceptedException:
            try:
                btn_iRefuse = self.driver.find_element_by_xpath("//*[contains(text(), 'I Accept')]").click()
            except exception:
                self.real_user_stare()
        # throws timeout exception(unhandled yet), but only if u interrupt
        self.real_user_stare()
        return True

    def scrap_url_list(self, list_of_url):
        for i in range(len(list_of_url)):
            temp = list_of_url[i].replace('background-image: url("', '')
            list_of_url[i] = temp[0:temp.find('");')]
            print(list_of_url)
        return list_of_url

    def handle_exceptions(self):
        while True:
            if self.driver.find_element_by_xpath('//*[contains(text(), "You\'re Out of Likes!")]').is_displayed():
                i = 0
                print("Tinder doesn\'t want me to date :<")
                return False
            try:
                btn_noThanks = self.driver.find_element_by_xpath("//*[contains(text(), 'No Thanks')]").click()
            except (exception.ElementNotInteractableException, exception.NoSuchElementException,
                    exception.ElementClickInterceptedException) as e:
                try:
                    match_button = self.driver.find_element_by_xpath("//*[contains(text(), 'Keep Swiping')]").click()
                except (exception.ElementNotInteractableException, exception.NoSuchElementException,
                        exception.ElementClickInterceptedException) as e:
                    try:
                        not_interessted_button = self.driver.find_element_by_xpath(
                            "//*[contains(text(), 'Not interested')]").click()
                    except (exception.ElementNotInteractableException, exception.NoSuchElementException,
                            exception.ElementClickInterceptedException) as e:
                        try:
                            btn_iRefuse = self.driver.find_element_by_xpath("//*[contains(text(), 'I Accept')]").click()
                        except (exception.ElementNotInteractableException, exception.NoSuchElementException,
                                exception.ElementClickInterceptedException) as e:
                            return False

    def get_her_photo(self):
        topone = self.driver.find_element_by_css_selector(
            "div[class='recCard Ov(h) Cur(p) W(100%) Bgc($c-placeholder) StretchedBox Bdrs(8px) CenterAlign--ml Toa(n) active Prs(1000px) Bfv(h)']")
        girls_name = str(
            topone.find_element_by_css_selector(
                "#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.recsCardboard.W\(100\%\).Mt\(a\).H\(100\%\)--s.Px\(10px\)--s.Pos\(r\) > div > div.recsCardboard__cards.Expand.Animdur\(\$fast\).Animtf\(eio\).Pos\(r\).CenterAlign.Z\(1\) > div.recCard.Ov\(h\).Cur\(p\).W\(100\%\).Bgc\(\$c-placeholder\).StretchedBox.Bdrs\(8px\).CenterAlign--ml.Toa\(n\).active.Prs\(1000px\).Bfv\(h\) > div.Pos\(a\).D\(f\).Jc\(sb\).C\(\#fff\).Ta\(start\).B\(0\).W\(100\%\).Wc\(\$transform\).P\(16px\).P\(20px\)--l > div > div.Pos\(a\).Fz\(\$l\).B\(0\).Trsdu\(\$fast\).NetWidth\(100\%\,50px\).D\(f\).Ai\(c\) > div > div > span").get_attribute(
                "innerHTML"))
        print(girls_name)
        raw_list_url = list([])
        if self.handle_exceptions():
            return False  # out of likes
        body = self.driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main')
        body.click()
        tries = 3
        i = 0
        while tries > 0:
            girls = topone.find_elements_by_xpath('.//*[@aria-label="' + girls_name + '"]')
            for i in girls:
                if i.get_attribute("style") in raw_list_url:
                    print("jj")
                    tries -= 1
                else:
                    print("adding: " + i.get_attribute("style"))
                    raw_list_url.append(i.get_attribute("style"))
                    tries = 3
            actions = ActionChains(self.driver)
            actions.move_to_element(body).send_keys(Keys.SPACE).perform()
        return self.scrap_url_list(raw_list_url)

    # prototype function, user input will be replaced by AI
    def judge_her(self, photos):
        # photos=self.get_her_photo()
        print(photos)
        print(len(photos))
        if (len(photos) == 1) & (photos[0].find("unknown.jpg") != -1):
            return 1
        result = int(input('do you like her? 1-10'))
        # result=6

        return True if result > 0.5 else False
