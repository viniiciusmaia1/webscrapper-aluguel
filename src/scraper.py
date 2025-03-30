from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def init_driver(headless=False):
    options = webdriver.ChromeOptions()

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extract_visible_properties(driver, url):
    driver.get(url)
    time.sleep(4)

    cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="house-card-container-rent"]')
    print(f"🔎 {len(cards)} imóveis visíveis encontrados")

    imoveis = []

    for idx, card in enumerate(cards, start=1):
        try:
            parent_link = card.find_element(By.XPATH, ".//a")
            href = parent_link.get_attribute("href")

            # Descrição
            try:
                descricaoPrimaria = card.find_element(By.CSS_SELECTOR, "h2.CozyTypography.UQvm9e").text.strip()
            except:
                descricaoPrimaria = ""

            # Valor total
            try:
                valor_total = card.find_element(By.CSS_SELECTOR, "div.Cozy__CardTitle-Title").text.replace("total", "").replace("R$", "").strip()
            except:
                valor_total = ""

            # Valor aluguel
            try:
                valor_aluguel = card.find_element(By.CSS_SELECTOR, "div.Cozy__CardTitle-Subtitle").text.replace("aluguel", "").replace("R$", "").strip()
            except:
                valor_aluguel = ""

            # Detalhes
            try:
                detalhes = card.find_element(By.CSS_SELECTOR, "h3.CozyTypography").text.strip()
            except:
                detalhes = ""

            # Endereço
            try:
                enderecoAproximado = card.find_elements(By.CSS_SELECTOR, "h2.CozyTypography")[-1].text.strip()
                enderecoAproximado = enderecoAproximado.replace(",", " - ")
            except:
                enderecoAproximado = ""

            imoveis.append({
                "url": href,
                "descricao Primaria": descricaoPrimaria,
                "valor_total": valor_total,
                "valor_aluguel": valor_aluguel,
                "enderecoAproximado": enderecoAproximado,
                "detalhes": detalhes
            })

        except Exception as e:
            print(f"❌ Erro ao processar imóvel #{idx}: {e}")
            continue

    df = pd.DataFrame(imoveis)
    return df
