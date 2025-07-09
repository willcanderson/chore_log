from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

driver = webdriver.Chrome()

class WebpageTests(StaticLiveServerTestCase):

    def test_registration_and_play_logging(self):
        # parent
        driver.get(f"{self.live_server_url}/chorelogapp/register-parent/")
        parent_username = driver.find_element(By.NAME, "username")
        email = driver.find_element(By.NAME, "email")
        parent_password = driver.find_element(By.NAME, "password")
        parent_confirmation = driver.find_element(By.NAME, "confirmation")
        parent_username.send_keys("parent_name")
        email.send_keys("parent@example.com")
        parent_password.send_keys("password12345")
        parent_confirmation.send_keys("password12345")
        parent_confirmation.send_keys(Keys.RETURN)
        self.assertTrue("Hello, parent_name" in driver.page_source)

        driver.get(f"{self.live_server_url}/chorelogapp/logout/")

        # child
        driver.get(f"{self.live_server_url}/chorelogapp/register-child/")
        parent_email = driver.find_element(By.NAME, "parent-email")
        username = driver.find_element(By.NAME, "username")
        password = driver.find_element(By.NAME, "password")
        confirmation = driver.find_element(By.NAME, "confirmation")
        parent_email.send_keys("parent@example.com")
        username.send_keys("child_name")
        password.send_keys("12345password")
        confirmation.send_keys("12345password")
        time.sleep(1) # Test usually (but not always) fails without this because of "parent not found" error. DB slow?
        confirmation.send_keys(Keys.RETURN)
        self.assertTrue("Hello, child_name" in driver.page_source)

        # log play
        log_play_button = driver.find_element(By.CLASS_NAME, "log-play-button")
        log_play_button.click()
        game = driver.find_element(By.NAME, "game")
        minutes = driver.find_element(By.NAME, "minutes_played")
        game.send_keys("Mario")
        minutes.send_keys("10")
        time.sleep(1)
        minutes.send_keys(Keys.RETURN)
        self.assertTrue('<td>Mario</td>' in driver.page_source)
