async def extract_card_data(card):
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
    endereco_aproximado = enderecos[-1].strip().replace(",", " - ") if len(enderecos) > 1 else ""

    return {
        "url": href,
        "descricao": descricao,
        "valor_total": valor_total,
        "valor_aluguel": valor_aluguel,
        "area": area,
        "quartos": quartos,
        "vagas": vagas,
        "endereco": endereco_aproximado
    }