import time
from selenium import webdriver
from selenium.common import MoveTargetOutOfBoundsException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


nome_grupo = input(f'Digite o nome do grupo\n')

# Crie uma instância de Options
opcoes = Options()

# Adicione o argumento "--headless"
opcoes.add_argument("--headless")

# Inicialize o driver do navegador (por exemplo, Chrome)
driver = webdriver.Chrome(options=opcoes)

# Maximiza a janela do navegador
driver.maximize_window()

# Acesse o site
driver.get("url da intranet")

# Encontre o campo de e-mail e insira o e-mail
email_field = driver.find_element(By.ID, "email")
email_field.send_keys("meu_email")

# Encontre o campo de senha e insira a senha
password_field = driver.find_element(By.ID, "password")
password_field.send_keys("minha_senha")

# Submeta o formulário pressionando Enter
password_field.submit()

# Redirecione para a nova URL
driver.get("http://10.94.2.74/bconnect/setup-groups")

# Encontre o link e clique nele
link = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-success")
link.click()

email_field = driver.find_element(By.ID, "name")
email_field.send_keys(nome_grupo)

with open("file.txt", "r") as file:
    lojas = [line.strip().lower() for line in file]  # Normalize os nomes das lojas

# Encontre todas as divs com a classe "col-md-4"
divs = driver.find_elements(By.CSS_SELECTOR, "div.col-md-4")

# Crie uma cópia da lista de lojas
lojas_nao_encontradas = lojas.copy()

# Para cada div
for div in divs:
    # Encontre a label e o input dentro da div
    label = div.find_element(By.CSS_SELECTOR, "label.form-check-label")
    checkbox = div.find_element(By.CSS_SELECTOR, "input.form-check-input")

    # Se o texto da label estiver na lista de lojas
    if label.text.strip().lower() in lojas:

        try:
            # Clique no checkbox
            checkbox.click()
            time.sleep(0.8)

            # Remova a loja da lista de lojas não encontradas
            lojas_nao_encontradas.remove(label.text.strip().lower())

        except MoveTargetOutOfBoundsException as erro:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)

        except ElementClickInterceptedException:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)

# Se ainda há lojas não encontradas após a primeira varredura
if lojas_nao_encontradas:
    # Faça uma segunda varredura de baixo para cima
    count = 0
    for div in reversed(divs):
        # Encontre a label e o input dentro da div
        label = div.find_element(By.CSS_SELECTOR, "label.form-check-label")
        checkbox = div.find_element(By.CSS_SELECTOR, "input.form-check-input")
        count += 1

        if 60 <= count <= 110:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)
            time.sleep(0.5)
            count += 1

        if 160 <= count <= 197:
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)
            time.sleep(0.5)
            count += 1

        # Se o texto da label estiver na lista de lojas
        if label.text.strip().lower() in lojas_nao_encontradas:

            try:
                # Clique no checkbox
                checkbox.click()
                time.sleep(1.5)

                # Remova a loja da lista de lojas não encontradas
                lojas_nao_encontradas.remove(label.text.strip().lower())

            except MoveTargetOutOfBoundsException as erro:
                #driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)
                pass

            except ElementClickInterceptedException:
                #driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.UP)
                pass


# Imprima as lojas que não foram encontradas
print("Lojas não encontradas:")
for loja in lojas_nao_encontradas:
   print(loja)


# Se todas as lojas foram encontradas
if len (lojas_nao_encontradas) <= 3:
    # Rolar para o final da página novamente
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)
    # Encontre o botão e clique nele
    salvar_button = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    time.sleep(2)
    salvar_button.click()