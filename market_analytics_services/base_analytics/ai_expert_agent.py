import os
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from googletrans import Translator

import ai_expert_config
import config


class AIExpertAgent(webdriver.Chrome):

    def __init__(self):
        parent_path = Path(__file__).parent.parent.parent
        self.driver_path = str(parent_path) + "\\SeleniumDrivers"
        os.environ['PATH'] += self.driver_path
        super().__init__()
        self.get("https://chat.lmsys.org/")
        time.sleep(1)
        self.waiting_time = ai_expert_config.WRITING_WAIT_TIME
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.base_prompt = "You are a professional stock market analyst. You need to write middle size (350-400 words) fundamental analysis summary for gas producing company {company} with metrics:{metrics}.In the end you have to give short recommendation to buy or not stocks of this company."

    def ask_for_analysis(self, stock_symbol: str, data_string: str, language):
        msg = self.base_prompt.format(company=stock_symbol, metrics=data_string)
        attempts = 0
        success = False
        summary = ""
        while not success and attempts != ai_expert_config.MAX_ATTEMPTS:
            attempts += 1
            try:
                self.refresh()
                time.sleep(1)
                wait = WebDriverWait(self, self.waiting_time + 40)
                text_area = wait.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
                text_area.send_keys(msg)
                text_area.send_keys(Keys.RETURN)
                time.sleep(2)
                send_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Send']")))
                send_button.click()
                time.sleep(self.waiting_time)
                bot_responses = [wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='bot']")))]
                success = True if bot_responses[0].text[-1] == '.' else False
                conts = 0
                while not success and conts < 3:
                    conts += 1
                    text_area.send_keys("continue")
                    text_area.send_keys(Keys.RETURN)
                    time.sleep(2)
                    send_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Send']")))
                    send_button.click()
                    time.sleep(ai_expert_config.CONTINUE_WAIT_TIME)
                    bot_responses = wait.until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='bot']")))
                    if bot_responses[-1].text[-1] == '.':
                        success = True
                if success:
                    for bot_response in bot_responses:
                        summary += bot_response.text
            except Exception as e:
                if config.LOG:
                    print(e)
                self.waiting_time += ai_expert_config.ADDITIONAL_TIME
        if not success:
            raise ConnectionError("Could not get result from vicuna chat service")
        if language == "RUS":
            translation = self.translator.translate(summary, dest='ru')
            return translation.text
        return summary
