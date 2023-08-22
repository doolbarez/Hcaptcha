from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
import time
import os
from twocaptcha import TwoCaptcha

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
#options.add_argument("--proxy-server=34.101.245.121:80")

# Запуск веб-драйвера с настройками прокси
driver = webdriver.Chrome(options=options)
# Открытие страницы
driver.get("https://accounts.hcaptcha.com/demo")

field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/fieldset/ul/li[1]/input")))
field.send_keys("Example")

time.sleep(3)
iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[5]/form/fieldset/ul/li[2]/div/div/iframe")))
result = solveHCaptcha()

if result:
    code = result['code']
    driver.execute_script(
        "document.querySelector("+ "'"+ '[name="h-captcha-response"]' + "'" + ").innerHTML = " + "'" + code + "'")
    driver.find_element(By.XPATH, "/html/body/div[5]/form/fieldset/ul/li[3]/input").click()

time.sleep(10)

# Закрытие драйвера
driver.quit()