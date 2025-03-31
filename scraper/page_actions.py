from .config import SCROLL_RETRIES, WAIT_SCROLL, WAIT_AFTER_CLICK, WAIT_BEFORE_START

async def expand_all_cards(page):
    await page.wait_for_timeout(WAIT_BEFORE_START)

    while True:
        found_button = False

        for _ in range(SCROLL_RETRIES):
            await page.mouse.wheel(0, 300)
            await page.wait_for_timeout(WAIT_SCROLL)

            try:
                button = await page.query_selector('#see-more')
                if button:
                    await button.scroll_into_view_if_needed()
                    await page.wait_for_timeout(1000)
                    await button.click()
                    await page.wait_for_timeout(WAIT_AFTER_CLICK)
                    found_button = True
                    break
            except:
                pass

        if not found_button:
            break