import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def extract_visible_properties(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(4000)

        # Scroll + clique no botão "Ver mais"
        while True:
            found_button = False
            for _ in range(30):
                await page.mouse.wheel(0, 300)
                await page.wait_for_timeout(300)
                try:
                    button = await page.query_selector('#see-more')
                    if button:
                        print("🔘 Botão 'Ver mais' encontrado. Clicando para carregar mais imóveis...")
                        await button.scroll_into_view_if_needed()
                        await page.wait_for_timeout(1000)
                        await button.click()
                        await page.wait_for_timeout(3000)
                        found_button = True
                        break
                except:
                    pass
            if not found_button:
                print("✅ Nenhum botão 'Ver mais' encontrado. Continuando extração...")
                break

        # Captura os cards
        cards = await page.query_selector_all('div[data-testid="house-card-container-rent"]')
        print(f"🔎 {len(cards)} imóveis visíveis encontrados")

        imoveis = []

        for idx, card in enumerate(cards, start=1):
            try:
                href = await card.eval_on_selector("a", "el => el.href")

                try:
                    descricaoPrimaria = await card.locator("h2.CozyTypography").first.inner_text()
                except:
                    descricaoPrimaria = ""

                try:
                    valor_total = await card.locator("div.Cozy__CardTitle-Title").first.inner_text()
                    valor_total = valor_total.replace("total", "").replace("R$", "").strip()
                except:
                    valor_total = ""

                try:
                    valor_aluguel = await card.locator("div.Cozy__CardTitle-Subtitle").first.inner_text()
                    valor_aluguel = valor_aluguel.replace("aluguel", "").replace("R$", "").strip()
                except:
                    valor_aluguel = ""

                try:
                    detalhes = await card.locator("h3.CozyTypography").first.inner_text()
                except:
                    detalhes = ""

                try:
                    enderecos = await card.locator("h2.CozyTypography").all_inner_texts()
                    enderecoAproximado = enderecos[-1].strip().replace(",", " - ") if len(enderecos) > 1 else ""
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

        await browser.close()
        return pd.DataFrame(imoveis)

def main():
    url = "https://www.quintoandar.com.br/alugar/imovel/contagem-mg-brasil/de-500-a-1500-reais/1-quartos/1-2-3-vagas/aceita-pets"
    df = asyncio.run(extract_visible_properties(url))
    print("\n✅ Fim da execução.")
    print(df.head(10).to_string(index=False))
    df.to_excel("imoveis.xlsx", index=False)
    print("📁 Arquivo 'imoveis.xlsx' salvo com sucesso!")

if __name__ == "__main__":
    main()
