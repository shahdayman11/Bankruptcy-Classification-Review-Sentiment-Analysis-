import asyncio
import random
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://www.trustpilot.com/review/www.amazon.com"

TARGET_REVIEWS = 6000
MAX_PAGES = 500

all_reviews = []


async def handle_route(route):
    if route.request.resource_type in ["image", "font", "media"]:
        await route.abort()
    else:
        await route.continue_()


async def scrape():
    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(
            storage_state="trustpilot_cookies.json",
            viewport={"width": 1920, "height": 1080}
        )

        page = await context.new_page()
        await page.route("**/*", handle_route)

        print("\nSTARTING SCRAPER...\n")

        for current_page in range(1, MAX_PAGES + 1):

            if len(all_reviews) >= TARGET_REVIEWS:
                print("TARGET REACHED (6000 reviews)")
                break

            url = f"{BASE_URL}?page={current_page}"
            print(f"Page {current_page}: {url}")

            try:
                await page.goto(url, timeout=60000)
                await asyncio.sleep(random.uniform(3, 5))

                # block detection
                if any(x in page.url.lower() for x in ["login", "captcha", "verify"]):
                    print("BLOCKED OR SESSION EXPIRED")
                    break

                await page.wait_for_selector(
                    '[data-service-review-card-paper="true"]',
                    timeout=30000
                )

                cards = page.locator('[data-service-review-card-paper="true"]')
                count = await cards.count()

                print(f"Found {count} reviews")

                if count == 0:
                    print("NO MORE REVIEWS")
                    break

                for i in range(count):

                    if len(all_reviews) >= TARGET_REVIEWS:
                        break

                    card = cards.nth(i)
                    html = await card.inner_html()
                    soup = BeautifulSoup(html, "html.parser")

                    def text(sel):
                        el = soup.select_one(sel)
                        return el.get_text(strip=True) if el else ""

                    def attr(sel, a):
                        el = soup.select_one(sel)
                        return el[a] if el and el.has_attr(a) else ""

                    review = {
                        "review_title": text("h2"),
                        "review_text": text('[data-service-review-text-typography="true"]'),
                        "stars": attr('[data-service-review-rating]', "data-service-review-rating"),
                        "review_date": attr("time", "datetime"),
                        "reviewer_name": text('span[data-consumer-name-typography="true"]'),
                        "reviewer_location": text('[data-consumer-country-typography="true"]')
                    }

                    all_reviews.append(review)

                print(f"TOTAL COLLECTED: {len(all_reviews)}")

                # auto backup
                if len(all_reviews) % 300 == 0:
                    pd.DataFrame(all_reviews).to_csv(
                        "backup_reviews.csv",
                        index=False,
                        encoding="utf-8-sig"
                    )
                    print("Backup saved")

                await asyncio.sleep(random.uniform(2, 5))

            except Exception as e:
                print(f"ERROR: {e}")
                break

        await browser.close()

    # final save
    df = pd.DataFrame(all_reviews)
    df.to_csv("trustpilot_6000_reviews.csv", index=False, encoding="utf-8-sig")

    print("\nDONE")
    print(f"TOTAL REVIEWS: {len(df)}")


asyncio.run(scrape())