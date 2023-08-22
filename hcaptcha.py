from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import os
from twocaptcha import TwoCaptcha
from proxy_auth_data import login, password

#2CaptchaAPI
def solveHCaptcha():
    

    api_key = os.getenv('APIKEY_2CAPTCHA', '80e79102cb6c33a53a236589e2394229')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.hcaptcha(
            sitekey='a5f74b19-9e45-40e0-b45d-47ff91b7a6c2',
            url='https://accounts.hcaptcha.com/demo',
        )
    except Exception as e:
        print(e)
        return False

    else:
        return result


# Настройка опций для веб-драйвера
options = webdriver.ChromeOptions()
options.add_experimental_option('useAutomationExtension', False)
UserAgent = UserAgent()
options.add_argument(f"user-agent={UserAgent.random}")
options = {
'proxy': {'http': 'http://brd-customer-hl_ce63cbe3-zone-data_center:47go741wi9a6@brd.superproxy.io:22225',
'https': 'http://brd-customer-hl_ce63cbe3-zone-data_center:47go741wi9a6@brd.superproxy.io:22225'},
}

# Запуск веб-драйвера с настройками прокси
driver = webdriver.Chrome(seleniumwire_options=options)
# Открытие страницы
driver.get("https://lumtest.com/myip.json")
time.sleep(2)
driver.get("https://accounts.hcaptcha.com/demo")

# Кастомные селекторы
class CustomSelectors:
    @staticmethod
    def by_iframe_title(title_value):
        return By.CSS_SELECTOR, f'iframe[title="{title_value}"]'
    def by_input_aria_label(label_value):
        return By.CSS_SELECTOR, f'input[aria-label="{label_value}"]'


field = WebDriverWait(driver, 10).until(EC.presence_of_element_located(CustomSelectors.by_input_aria_label('Form Field (optional)')))
field.send_keys("Example")

time.sleep(3)

iframe = WebDriverWait(driver, 10 ).until(EC.presence_of_element_located(CustomSelectors.by_iframe_title('Widget containing checkbox for hCaptcha security challenge')))
result = solveHCaptcha()

if result:
    code = result['code']
    driver.execute_script(
        "document.querySelector("+ "'"+ '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + code + "'")
    driver.find_element(By.XPATH, "/html/body/div[5]/form/fieldset/ul/li[3]/input").click()

time.sleep(10)

# Закрытие драйвера
driver.quit()
