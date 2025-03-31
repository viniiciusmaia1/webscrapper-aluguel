import pandas as pd
from .driver import PlaywrightDriver
from .page_actions import expand_all_cards
from .extractors import extract_card_data

class Scraper:
    def __init__(self, url: str):
        self.url = url
        self.imoveis = []

    async def run(self):
        driver = PlaywrightDriver()
        await driver.start()
        page = await driver.new_page(self.url)

        await expand_all_cards(page)
        cards = await page.query_selector_all('div[data-testid="house-card-container-rent"]')

        for idx, card in enumerate(cards, start=1):
            try:
                data = await extract_card_data(card)
                self.imoveis.append(data)
            except Exception as e:
                print(f"❌ Erro ao processar imóvel #{idx}: {e}")
                continue

        await driver.stop()
        return pd.DataFrame(self.imoveis)