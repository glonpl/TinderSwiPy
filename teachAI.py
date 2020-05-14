from SwiperModules.tinderSeleniumSwiper import SeleniumSwiper as SS
from SwiperModules.viewerGui import Viewer as GUI

driver = SS()
driver.Facebook_login()
driver.real_user_stare()
driver.Tinder_login()
driver.Close_popup()
driver.real_user_stare()
viewer = GUI(list([]))
while True:
    viewer.setList(driver.get_her_photo())
    driver.Swipe_it(viewer.pictureBrowser())

driver.close()
