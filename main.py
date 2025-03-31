import asyncio
from scraper.scraper import Scraper

async def main():
    url = "https://www.quintoandar.com.br/alugar/imovel/contagem-mg-brasil/de-500-a-1500-reais/1-quartos/1-2-3-vagas/aceita-pets"
    scraper = Scraper(url)
    df = await scraper.run()
    df.to_excel("imoveis.xlsx", index=False)
    print("📁 Arquivo 'imoveis.xlsx' salvo com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
