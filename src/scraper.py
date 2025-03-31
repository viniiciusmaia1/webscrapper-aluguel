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

        while True:
            found_button = False
            for _ in range(30):
                await page.mouse.wheel(0, 300)
                await page.wait_for_timeout(300)
                try:
                    button = await page.query_selector('#see-more')
                    if button:
                        await button.scroll_into_view_if_needed()
                        await page.wait_for_timeout(1000)
                        await button.click()
                        await page.wait_for_timeout(3000)
                        found_button = True
                        break
                except:
                    pass
            if not found_button:
                break

        cards = await page.query_selector_all('div[data-testid="house-card-container-rent"]')

        imoveis = []

        for idx, card in enumerate(cards, start=1):
            try:
                href = await card.eval_on_selector("a", "el => el.href")

                descricao_el = await card.query_selector("h2.CozyTypography._72Hu5c")
                descricao = await descricao_el.inner_text() if descricao_el else ""

                valor_total_el = await card.query_selector("div.Cozy__CardTitle-Title")
                valor_total = await valor_total_el.inner_text() if valor_total_el else ""
                valor_total = valor_total.replace("total", "").replace("R$", "").strip()

                valor_aluguel_el = await card.query_selector("div.Cozy__CardTitle-Subtitle")
                valor_aluguel = await valor_aluguel_el.inner_text() if valor_aluguel_el else ""
                valor_aluguel = valor_aluguel.replace("aluguel", "").replace("R$", "").strip()

                detalhes_el = await card.query_selector("h3.CozyTypography")
                detalhes = await detalhes_el.inner_text() if detalhes_el else ""
                area, quartos, vagas = "", "", ""
                try:
                    partes = [p.strip() for p in detalhes.split("·")]
                    area = partes[0] if len(partes) > 0 else ""
                    quartos = partes[1] if len(partes) > 1 else ""
                    vagas = partes[2] if len(partes) > 2 else ""
                except:
                    pass

                enderecos_el = await card.query_selector_all("h2.CozyTypography")
                enderecos = [await el.inner_text() for el in enderecos_el]
                enderecoAproximado = enderecos[-1].strip().replace(",", " - ") if len(enderecos) > 1 else ""

                imoveis.append({
                    "url": href,
                    "descricao": descricao,
                    "valor_total": valor_total,
                    "valor_aluguel": valor_aluguel,
                    "area": area,
                    "quartos": quartos,
                    "vagas": vagas,
                    "endereco": enderecoAproximado
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
    df.to_excel("imoveis.xlsx", index=False)
    print("📁 Arquivo 'imoveis.xlsx' salvo com sucesso!")
