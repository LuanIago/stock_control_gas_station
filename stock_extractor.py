import os
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

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

        page.goto("http://localhost:7089/")

        # Populating using protected variables and static selectors identified on the login screen
        page.get_by_placeholder("usuário").fill(USER)
        page.get_by_placeholder("senha").fill(PASSWORD)

        login_button = page.get_by_text("Acessar")
        login_button.click()

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

        # PAUSE: Open the Playwright panel for a stock screen inspection
        page.pause()

        browse.close()

except Exception as e:
    print(f"\n[ERROR] Execution failed: {e}")
    input("\nPress Enter to close the terminal...")
