import asyncio
from playwright.async_api import async_playwright

async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        context = await browser.new_context()

        page = await context.new_page()

        await page.goto(
            "https://www.trustpilot.com/review/www.amazon.com"
        )

        print(
            "\nIf Trustpilot asks you to log in,"
            "\nlog in manually."
            "\nThen press ENTER here."
        )

        input()

        await context.storage_state(
            path="trustpilot_session.json"
        )

        print("Session saved successfully.")

        await browser.close()

asyncio.run(main())