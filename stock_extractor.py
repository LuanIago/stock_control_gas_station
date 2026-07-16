from playwright.sync_api import sync_playwright

USUARIO = None
SENHA = None

try:
    with sync_playwright() as p:
        # O Chrome é iniciado de forma visível para acompanhar os testes
        browse = p.chromium.launch(headless=False, channel="chrome")
        context = browse.new_context()
        page = context.new_page()

        page.goto("http://localhost:7089/")

        # Preenchimento usando variáveis protegidas e seletores estáticos identificados na tela de login
        page.fill('[id="O14_id-inputEl"]', USUARIO)
        page.fill('[id="O18_id-inputEl"]', SENHA)

        login_button = page.locator('[id="O2C_id"]')
        login_button.click()

        # Evita o uso de 'time.sleep' esperando a rede ficar ociosa pós-login
        page.wait_for_load_state("networkidle")

        print("Login efetuado com sucesso (credenciais protegidas)!")

        # PAUSA: Abre o painel do Playwright para a inspeção da tela de estoque
        page.pause()

        browse.close()

except Exception as e:
    print(f"\n[ERRO] Ocorreu uma falha na execução: {e}")
    input("\nPressione Enter para fechar o terminal...")
