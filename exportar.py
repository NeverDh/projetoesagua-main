from importacoes import *

class exportar:
    def exportacao_contatos(self):
        ##CONFIGURANDO JANELA##
        servico = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument("--window-size=1920,1080")
        janela = webdriver.Chrome(service=servico, options=chrome_options)

        link = 'https://canalpro.grupozap.com/ZAP_OLX/0/leads/messages'
        username = 'itaimoveis7@gmail.com'
        password = 'rj103fab'

        ##APAGANDO TODOS OS EMAILS
        IMAP_SERVER = 'imap.gmail.com'
        USERNAME = 'itaimoveis7@gmail.com'
        PASSWORD = 'pjmupogavhxlwmyk'
        # Conectar ao servidor IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USERNAME, PASSWORD)
        mail.select('inbox')
        status, email_ids = mail.search(None, '1')
        result, data = mail.uid('search', None, 'ALL')
        if result == 'OK':
            email_ids = data[0].split()
            for email_id in email_ids:
                # Marcar cada email para exclusão
                mail.uid('store', email_id, '+FLAGS', '(\Deleted)')

            # Excluir os emails marcados para exclusão
            mail.expunge()
            print("Todos os emails foram excluídos com sucesso.")
    


        ##LOGANDO NO SITE E EXPORTANDO DADOS
        janela.get(link)

        while True:
            try:
                logar_usuario = janela.find_element('xpath', '//*[@id="app"]/div[2]/div/div/div/div/section[1]/div/section/form/div[1]/div/div[2]/div/div/input')
                logar_usuario.send_keys(username)
                break
            except NoSuchElementException:
                None
                
        while True:
            try:
                logar_senha = janela.find_element('xpath', '//*[@id="app"]/div[2]/div/div/div/div/section[1]/div/section/form/div[2]/div/div[2]/div/div/input')
                logar_senha.send_keys(password)
                break
            except NoSuchElementException:
                None   

        botao_logar = janela.find_element('xpath', '//*[@id="app"]/div[2]/div/div/div/div/section[1]/div/section/form/button').click()

        while True:
            try:
                janela.execute_script("document.getElementById('privacy-term-alert').style.display='none'")
                break
            except Exception as e:
                None   

        while True:
            try:
                botao_exportar = janela.find_element('xpath', '//*[@id="top-page"]/div/div[1]/div/div[3]/button').click()
                break
            except Exception as e:
                None   

        while True:
            try: 
                botao_exportar2 = janela.find_element('xpath', '//*[@id="top-page"]/div/div[1]/div/div/div[3]/button[2]').click()
                break
            except Exception as e:
                None  

    