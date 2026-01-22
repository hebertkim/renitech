# app/services/notifications/whatsapp_web_service.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

class WhatsAppWebService:
    """
    Envia mensagens via WhatsApp Web automaticamente usando Selenium.
    """

    @staticmethod
    def send_message(phone: str, message: str):
        """
        phone: número completo com código do país, ex: +5541996454466
        message: mensagem de texto
        """
        chrome_options = Options()
        chrome_options.add_argument("--user-data-dir=./selenium_data")  # mantém sessão logada
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_argument("--headless")  # opcional
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )

        try:
            encoded_msg = message.replace(" ", "%20")
            url = f"https://web.whatsapp.com/send?phone={phone.replace('+','')}&text={encoded_msg}"
            driver.get(url)
            time.sleep(10)  # espera carregar WhatsApp Web

            send_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            send_box.send_keys(Keys.ENTER)
            time.sleep(3)

            print(f"📲 WhatsApp enviado para {phone}")

        except Exception as e:
            print(f"❌ Erro ao enviar WhatsApp para {phone}: {e}")
        finally:
            driver.quit()
