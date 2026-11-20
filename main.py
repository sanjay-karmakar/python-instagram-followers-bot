from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


SIMILAR_ACCOUNT = ""
USERNAME = ""
PASSWORD = ""


class InstaFollower:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.maximize_window()
        self.driver.get("https://instagram.com")


    def login(self):
        username = self.driver.find_element(By.NAME, value="email")
        password = self.driver.find_element(By.NAME, value="pass")

        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)

        login_button = self.driver.find_element(By.XPATH, value='//*[@id="login_form"]/div/div[1]/div/div[3]/div/div/div/div[1]')
        login_button.click()

        time.sleep(5)
        not_now =self.driver.find_element(By.XPATH, value='/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div[2]')
        not_now.click()

        time.sleep(5)
        not_now2 = self.driver.find_element(By.XPATH, value='/html/body/div[2]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')
        not_now2.click()


    def find_followers(self):
        time.sleep(3)
        self.driver.get(f"https://www.instagram.com/{SIMILAR_ACCOUNT}/")
        time.sleep(5)

        # FIXED: Matches <a>, <button>, or <span> containing "followers"
        followers_btn = self.driver.find_element(
            By.XPATH,
            value="//a[contains(@href, 'followers')] | //button[contains(., 'followers')] | //span[contains(text(), 'followers')]",
        )
        followers_btn.click()
        time.sleep(4)

        dialog = self.driver.find_element(By.CSS_SELECTOR, value="div[role='dialog']")
        scrollable_div = self.driver.execute_script(
            """
            const dialog = arguments[0];
            for (const el of dialog.querySelectorAll('div')) {
                if (el.scrollHeight > el.clientHeight && el.clientHeight > 100) {
                    return el;
                }
            }
            return dialog;
            """,
            dialog,
        )

        for _ in range(5):
            self.driver.execute_script(
                "arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div
            )
            time.sleep(2)


    def follow(self):
        all_buttons = self.driver.find_elements(
            By.XPATH, value="//div[@role='dialog']//button[.//div[text()='Follow']]"
        )

        for button in all_buttons:
            try:
                button.click()
                time.sleep(1.5)
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(
                    By.XPATH, value="//button[contains(text(), 'Cancel')]"
                )
                cancel_button.click()



bot = InstaFollower()
bot.login()
bot.find_followers()
bot.follow()