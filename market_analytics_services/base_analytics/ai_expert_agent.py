import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from googletrans import Translator
from  pathlib import Path

import time


class AIExpertAgent(webdriver.Chrome):

    def __init__(self):
        #driver_path: str = r"D:\SeleniumDrivers"
        parent_path = Path(__file__).parent.parent.parent
        self.driver_path = str(parent_path) + "\\SeleniumDrivers"
        os.environ['PATH'] += self.driver_path
        super().__init__()
        self.get("https://chat.lmsys.org/")
        time.sleep(2)
        self.waiting_time = 60
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.base_prompt = "You are a professional stock market analyst. You need to write middle size (350-400 words) fundamental analysis summary for company gas producing company {company} with metrics:{metrics}.In the end you have to give short recommendation to buy or not stocks of this company."

    def ask_for_analysis(self, stock_symbol: str, data_string: str, language):
        msg = self.base_prompt.format(company=stock_symbol, metrics=data_string)
        error_counter = 0
        while True:
            try:
                self.refresh()
                time.sleep(2)
                wait = WebDriverWait(self, self.waiting_time + 40)
                text_area = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
                text_area.send_keys(msg)
                text_area.send_keys(Keys.RETURN)
                time.sleep(4)
                send_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Send']")))
                send_button.click()
                time.sleep(self.waiting_time)
                bot_response = wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='bot']")))
                summary = bot_response.text
                conts = 0
                success = True if summary[-1] == '.' else False
                while not success and conts < 3:
                    conts += 1
                    summary = ""
                    text_area.send_keys("continue")
                    text_area.send_keys(Keys.RETURN)
                    time.sleep(4)
                    send_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Send']")))
                    send_button.click()
                    time.sleep(self.waiting_time/2)
                    bot_responses = wait.until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='bot']")))
                    for bot_response in bot_responses:
                        summary += bot_response.text
                if success:
                    summary = str(summary)
                    if language == "RUS":
                        translation = self.translator.translate(summary, dest='ru')
                        return translation.text
                    return summary
                else:
                    raise SyntaxError()
            except Exception as e:
                if error_counter > 4:
                    raise e
                else:
                    error_counter += 1
                    self.waiting_time += 20