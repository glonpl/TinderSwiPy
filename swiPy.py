from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait as w8
from selenium.webdriver.common.by import By
from selenium.common import exceptions as NoEl
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Function to simulate user staring
def real_user_stare(x=1):
    import random
    from time import sleep
    sleep(random.uniform(1.5 * x, 4 * x))

# obvious. requires encrypted mail and password with key (run PasswordEncrypt if throws errors)
def Facebook_login():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=options)
    driver.get("https://facebook.com")
    real_user_stare()
    key, mail, passwd = read_from_files()
    from cryptography.fernet import Fernet
    f = Fernet(key)
    driver.find_element_by_id("email").send_keys(f.decrypt(mail).decode())
    driver.find_element_by_id("pass").send_keys(f.decrypt(passwd).decode())
    driver.find_element_by_id("pass").submit()
    return driver

# requres to be logged in on facebook
def Tinder_login(driver):
    driver.get("https://tinder.com")
    more_options_button = w8(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div/div[3]/span/button')))
    real_user_stare()
    try:
        btn = driver.find_element_by_xpath("//button[@aria-label='Log in with Facebook']").click()
    except NoEl.NoSuchElementException:

        driver.find_element_by_css_selector(".Fw\(\$medium\)").click()
        try:
            btn = driver.find_element_by_xpath("//button[@aria-label='Log in with Facebook']").click()
        except NoEl:
            driver.refresh()
            real_user_stare()
            Tinder_login(driver)

# helper function to het variables from encrypted files, used while logging in to facebook
def read_from_files():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    file = open('passwd.key', 'rb')
    passwd = file.read()
    file.close()
    file = open('mail.key', 'rb')
    mail = file.read()
    file.close()
    return key, mail, passwd

# closes popups after loging on tinder
def Close_popup(driver):
    i = 1
    while i != 0:
        real_user_stare(2)  # doesn't work as expected
        try:
            popup1 = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]').click()
        except NoEl.NoSuchElementException:
            i = 0

# swiper function
def Swipe_it(driver):
    i = 1
    while i != 0:
        if driver.find_element_by_xpath('//*[contains(text(), "You\'re Out of Likes!")]').is_displayed():
            i = 0
            print("Tinder doesn\'t want me to date :<")
            break
        try:
            btn_noThanks = driver.find_element_by_xpath("//*[contains(text(), 'No Thanks')]").click()
        except NoEl.ElementNotInteractableException:
            try:
                if judge_her(driver)>5:
                    like_button = w8(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Like']"))).click()
                else:
                    dislike_button = w8(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, "//button[@aria-label='Nope']"))).click()
            except NoEl.ElementClickInterceptedException:
                try:
                    match_button = driver.find_element_by_xpath("//*[contains(text(), 'Keep Swiping')]").click()
                except NoEl.ElementNotInteractableException:
                    try:
                        not_interessted_button = driver.find_element_by_xpath(
                            "//*[contains(text(), 'Not interested')]").click()
                    except NoEl.ElementClickInterceptedException:
                        real_user_stare(4)
        except NoEl.ElementClickInterceptedException:
            try:
                btn_iRefuse = driver.find_element_by_xpath("//*[contains(text(), 'I Accept')]").click()
            except NoEl:
                real_user_stare()
        # throws timeout exception(unhandled yet), but only if u interrupt
        real_user_stare()




def scrap_url_list(list_of_url):
    for i in range(len(list_of_url)):
        temp=list_of_url[i].replace('background-image: url("', '')
        list_of_url[i]= temp[0:temp.find('");')]
    return list_of_url


def get_her_photo(driver):
    topone= driver.find_element_by_css_selector("div[class='recCard Ov(h) Cur(p) W(100%) Bgc($c-placeholder) StretchedBox Bdrs(8px) CenterAlign--ml Toa(n) active Prs(1000px) Bfv(h)']")
    girls_name = str(
        topone.find_element_by_css_selector("#content > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.recsCardboard.W\(100\%\).Mt\(a\).H\(100\%\)--s.Px\(10px\)--s.Pos\(r\) > div > div.recsCardboard__cards.Expand.Animdur\(\$fast\).Animtf\(eio\).Pos\(r\).CenterAlign.Z\(1\) > div.recCard.Ov\(h\).Cur\(p\).W\(100\%\).Bgc\(\$c-placeholder\).StretchedBox.Bdrs\(8px\).CenterAlign--ml.Toa\(n\).active.Prs\(1000px\).Bfv\(h\) > div.Pos\(a\).D\(f\).Jc\(sb\).C\(\#fff\).Ta\(start\).B\(0\).W\(100\%\).Wc\(\$transform\).P\(16px\).P\(20px\)--l > div > div.Pos\(a\).Fz\(\$l\).B\(0\).Trsdu\(\$fast\).NetWidth\(100\%\,50px\).D\(f\).Ai\(c\) > div > div > span").get_attribute("innerHTML"))
        #
        # topone.find_element_by_xpath(
        # '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div/div/span').get_attribute(
        # "innerHTML")) #sems to be locking once for a time especiallywhen she got 2 pics & mostly on last one in queue
    # edit: proably it's about last person in queue. xpath selector seems to be stuck on last swiped prsn.  
    print(girls_name)
    raw_list_url = list([])
    body = driver.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main')
    body.click()
    tries = 3
    i=0
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
        actions = ActionChains(driver)
        actions.move_to_element(body).send_keys(Keys.SPACE).perform()
    return scrap_url_list(raw_list_url)

# prototype function, user input will be replaced by AI
def judge_her(driver):
    photos=get_her_photo(driver)
    print(photos)
    print(len(photos))
    if (len(photos)==1)&(photos[0].find("unknown.jpg")!=-1): #wyrzyca ludzi bez mordy
        return 1
    result=int(input('do you like her? 1-10'))
    # result=6
    return result
# jak 2 takie same imiona pod rząd, pobiera zdjecia 2os

driver = Facebook_login()
real_user_stare()
Tinder_login(driver)
Close_popup(driver)
real_user_stare()
Swipe_it(driver)
driver.close()


