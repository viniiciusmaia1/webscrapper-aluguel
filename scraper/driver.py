from playwright.async_api import async_playwright
from .config import VIEWPORT

class PlaywrightDriver:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context(viewport=VIEWPORT)

    async def new_page(self, url: str):
        self.page = await self.context.new_page()
        await self.page.goto(url)
        return self.page

    async def stop(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
