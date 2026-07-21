import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
from datetime import datetime

URL = "http://localhost:7089/"

# Loads the environment variables entered in the file .env
load_dotenv()

# Pulls the data securely (if none exists, sets a blank default value)
USER = os.getenv("POSTO_USER", "")
PASSWORD = os.getenv("POSTO_PASSWORD", "")

try:
    with sync_playwright() as p:
        # Chrome starts visibly to track tests
        browse = p.chromium.launch(headless=False, channel="chrome")
        context = browse.new_context()
        page = context.new_page()

        current_date = datetime.now().strftime("%d%m%Y")

        page.goto(URL)

        # Populating using protected variables and static selectors identified on the login screen
        page.get_by_placeholder("usuário").fill(USER)
        page.get_by_placeholder("senha").fill(PASSWORD)

        # Identify the login button and click on it
        page.get_by_text("Acessar").click()

        print("Successful login (protected credentials)!")

        # Stores the HTML sidebar structure of the gas station system
        side_menu = page.locator('iframe[name="name_htmlMenu_OD7"]').content_frame

        # Go through three menus before accessing the inventory report:
        # [ Relatorios -> Estoques -> Estoques por Grupo ou ]
        menu_reports = side_menu.locator("li").filter(has_text="Relatorios")
        menu_reports.click()

        menu_stocks = menu_reports.get_by_role("link", name="Estoques")
        menu_stocks.click()

        side_menu.get_by_role("link", name="Estoques por Grupo ou").click()

        # Find the date field and fill it in with the current date to receive the current stock
        date_label = page.locator("label.required", has_text="Data do Estoque")
        date_field = date_label.locator("xpath=../following-sibling::div[1]")
        date_field.locator("input").fill(current_date)

        # Select the option to show all products in stock
        page.get_by_role("group", name="Produtos com Estoque").get_by_role(
            "radio", name="Todos"
        ).click()

        # PAUSE: Open the Playwright panel for a stock screen inspection
        page.pause()

        browse.close()

except Exception as e:
    print(f"\n[ERROR] Execution failed: {e}")
    input("\nPress Enter to close the terminal...")
