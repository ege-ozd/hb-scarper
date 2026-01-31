import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_product_qna(driver, url):
    qna_data = []
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    try:
        # Sayfayı sekme butonlarının olduğu yere kadar kaydır
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)

        # Sekmeyi bulmak için daha esnek bir XPATH
        q_tab = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Soru Cevap')] | //div[contains(text(), 'Soru Cevap')]")))
        driver.execute_script("arguments[0].click();", q_tab)
        print("Soru-Cevap sekmesi tıklandı.")
        time.sleep(3)

        # "Daha fazla" butonuna basma döngüsü
        for _ in range(5):  # Şimdilik 5 kez basmayı dene (Sınırı artırabilirsin)
            try:
                more_btn = driver.find_elements(By.XPATH, "//button[contains(., 'Daha fazla')]")
                if more_btn and more_btn[0].is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", more_btn[0])
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", more_btn[0])
                    time.sleep(3)
                else:
                    break
            except:
                break

        soup = BeautifulSoup(driver.page_source, "html.parser")
        questions = soup.find_all("div", class_=lambda x: x and x.startswith("hermes-RowQuestion-module-"))
        answers = soup.find_all("div", class_=lambda x: x and x.startswith("hermes-RowAnswers-module-"))

        for q, a in zip(questions, answers):
            qna_data.append({
                "soru": q.get_text(strip=True),
                "cevap": a.get_text(strip=True)
            })
    except Exception as e:
        print(f"Soru-Cevap kısmında beklenmedik durum: {e}")

    return qna_data