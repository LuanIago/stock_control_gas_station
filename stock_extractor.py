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
        page.fill('[id="O14_id-inputEl"]', USER)
        page.fill('[id="O18_id-inputEl"]', PASSWORD)

        login_button = page.locator('[id="O2C_id"]')
        login_button.click()

        # Avoids the use of 'time.sleep' by expecting the network to be idle after login
        page.wait_for_load_state("networkidle")

        print("Login efetuado com sucesso (credenciais protegidas)!")

        # PAUSE: Open the Playwright panel for a stock screen inspection
        page.pause()

        browse.close()

except Exception as e:
    print(f"\n[ERROR] Execution failed: {e}")
    input("\nPress Enter to close the terminal...")
