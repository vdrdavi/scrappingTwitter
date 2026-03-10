import locale

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import csv

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)
driver.get("https://x.com/Nike")

wait = WebDriverWait(driver, 20)

try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[@data-testid='tweet']")))
    
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(3)
    
    tweets = driver.find_elements(By.XPATH, "//*[@data-testid='tweet']")
    
    dados = [["Name", "Username", "Data", "Tweet", "Replies", "Retweets", "Likes", "Views", "Url_tweet", "Url_imagem"]]
    
    for tweet in tweets:
        try:
            info = tweet.find_element(By.XPATH, ".//*[@data-testid='User-Name']")
            info_list = info.text.splitlines()
            username = info.text.splitlines()[1]
            name = info.text.splitlines()[0]
            posting_date_list = info_list[-1].split(" ")
            
            print(f"Username: {username}")
            print(f"Name: {name}")
            mes = f"{datetime.strptime(posting_date_list[2], '%b').month:02d}"
            data = posting_date_list[0]+"/"+mes
            print(f"Data: {data}")
            
            tweet_content = tweet.find_element(By.XPATH, ".//*[@data-testid='tweetText']")
            print(f"Tweet: {tweet_content.text.replace('\n', ' ')}")
            
            containers = tweet.find_elements(By.XPATH, ".//*[@data-testid='app-text-transition-container']")

            valores_extraidos = []

            for container in containers:
                try:
                    span_interno = container.find_element(By.XPATH, "./span/span")
                    valores_extraidos.append(span_interno.text)
                except:
                    valores_extraidos.append("0")

            for i in range(len(valores_extraidos)):
                valores_extraidos[i] = valores_extraidos[i].replace("mil", "000").replace("mi", "000000").replace(" ", "")
                
            print(valores_extraidos)
            
            try:
                link_elemento = tweet.find_element(By.XPATH, ".//time/..")
                link_tweet = link_elemento.get_attribute("href")
            except:
                link_tweet = "Sem link"

            try:
                imagem_elemento = tweet.find_element(By.XPATH, ".//*[@data-testid='tweetPhoto']//img")
                link_imagem = imagem_elemento.get_attribute("src")
            except:
                link_imagem = "Sem imagem"

            print(f"Link do Tweet: {link_tweet}")
            print(f"Link da Imagem: {link_imagem}")
            

            dados.append([name, username, data, tweet_content.text.replace('\n', ' '), valores_extraidos[0], valores_extraidos[1], valores_extraidos[2], valores_extraidos[3], link_tweet, link_imagem])
        except:
            continue
            
except Exception as e:
    print(f"Erro: {e}")

driver.quit()

with open('dados.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(dados)