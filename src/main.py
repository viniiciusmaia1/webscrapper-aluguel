from scraper import init_driver, extract_visible_properties
import pandas as pd

def main():
    url = "https://www.quintoandar.com.br/alugar/imovel/contagem-mg-brasil/de-500-a-1500-reais/1-quartos/1-2-3-vagas/aceita-pets"

    driver = init_driver(headless=False)
    df = extract_visible_properties(driver, url)
    driver.quit()

    print("\n✅ Fim da execução.")
    print(df.head(10).to_string(index=False))

    df.to_excel("imoveis.xlsx", index=False)
    print("📁 Arquivo 'imoveis.xlsx' salvo com sucesso!")

if __name__ == "__main__":
    main()
