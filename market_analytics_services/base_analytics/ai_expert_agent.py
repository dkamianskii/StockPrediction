import os
from pathlib import Path
import time
from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from googletrans import Translator

from market_analytics_services.base_analytics import ai_expert_config
import config


class AIExpertAgent(webdriver.Chrome):
    driver_path = str(Path(__file__).parent.parent.parent) + "\\SeleniumDrivers"
    os.environ['PATH'] += driver_path

    def __init__(self):
        super().__init__()
        self.waiting_time = ai_expert_config.WRITING_WAIT_TIME
        self.waiter = WebDriverWait(self, self.waiting_time + 40)
        self.translator = Translator(service_urls=['translate.googleapis.com'])
        self.bot_responses = []
        self.base_prompt = "You are a professional stock market analyst. You need to write middle size (350-400 words) fundamental analysis summary for gas producing company {company} with metrics:{metrics}.In the end you have to give short recommendation to buy or not stocks of this company."

    def _get_full_response(self, text_area, task: str) -> bool:
        text_area.send_keys(task)
        text_area.send_keys(Keys.RETURN)
        time.sleep(self.waiting_time)
        self.bot_responses = [self.waiter.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid='bot']")))]
        conts = 0
        e = self.bot_responses[-1].text[-1]
        while self.bot_responses[-1].text[-1] != '.':
            if conts == ai_expert_config.MAX_CONTINUES:
                return False
            conts += 1
            text_area.send_keys("continue")
            text_area.send_keys(Keys.RETURN)
            time.sleep(ai_expert_config.CONTINUE_WAIT_TIME)
            self.bot_responses = self.waiter.until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[data-testid='bot']")))
        return True

    def _dialog(self, start_prompt: str) -> Optional[str]:
        self.refresh()
        time.sleep(2)
        text_area = self.waiter.until(EC.visibility_of_element_located((By.TAG_NAME, "textarea")))
        if self._get_full_response(text_area, start_prompt):
            analysis: str = self.bot_responses[0].text
            for response in [r.text for r in self.bot_responses[1:]]:
                repeat_place = -1
                for i in range(1, min(len(analysis), len(response), 100)):
                    if analysis[-i:] == response[:i]:
                        repeat_place = i
                    elif repeat_place != -1:
                        break
                if repeat_place != -1:
                    response = response[repeat_place:]
                if analysis[-1] != " " and response[0] != 0:
                    analysis += " "
                analysis += response
            return analysis
        else:
            return None

    def ask_for_analysis(self, stock_symbol: str, data_string: str, language):
        self.get("https://chat.lmsys.org/")
        time.sleep(1)
        start_prompt = self.base_prompt.format(company=stock_symbol, metrics=data_string)
        attempts = 0
        summary = None
        while summary is None and attempts != ai_expert_config.MAX_ATTEMPTS:
            attempts += 1
            try:
                summary = self._dialog(start_prompt)
            except Exception as e:
                if config.LOG:
                    print(e)
                self.waiting_time += ai_expert_config.ADDITIONAL_TIME
        self.close()
        if summary is None:
            raise ConnectionError("Could not get result from vicuna chat service")
        if language == "RUS":
            translation = self.translator.translate(summary, dest='ru')
            return translation.text
        return summary
