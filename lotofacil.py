from bs4 import BeautifulSoup
from loterias_config import Config
from telebot import TeleBot
from requests import get

def env_sms(texto, BOT_TOKEN=Config.TOKEN, DESTINATION=Config.DESTINATION):
    """
    """
    tb = TeleBot(BOT_TOKEN)
    tb.send_message(DESTINATION,texto)

#
URL = Config.URL_LOTO
resultado = list()
resultado_str = ""

#
page = get(URL)

#
page.status_code

#
soup = BeautifulSoup(page.content, 'html.parser')

#
texto = soup.find("h1").text

concurso = texto.split()[-3]
data = texto.split()[-1]

texto = "Concurso {} {}".format(concurso, data)

# TAG: "span" CLASS: "circle"
dezenas = soup.find_all("span", class_="circle")

for tag in range(len(dezenas[:15])):
    resultado.append(dezenas[tag].text)

for i, v in enumerate(resultado):
    if int(i) % 5 == 0:
        resultado_str = resultado_str + "\n" + v
    else:
        resultado_str = resultado_str + " - " + v

texto = texto + "\n" + resultado_str

env_sms(texto)
