import logging

from bs4 import BeautifulSoup
from loterias_config import Config
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from requests import get

    
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Link doc lib 
# https://docs.python-telegram-bot.org/en/stable/

TOKEN = Config.TOKEN_TG

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    print(user)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def get_lotofacil(update: Update, context: ContextTypes.DEFAULT_TYPE, concurson: None) -> None:
    """Send a message when the resultado da lotofacil."""
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
    
    await update.message.reply_text(texto)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


def user_author():
	"""
	- Buscar usuarios autorizados a interragir com o bot
	"""
	return [1370856180,352435550]
    

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    #application.add_handler(CommandHandler("start", start, filters.Chat(352435550)))
    application.add_handler(CommandHandler("help", help_command))
    #application.add_handler(CommandHandler("help", help_command, filters.Chat(352435550)))
    
    application.add_handler(CommandHandler("Lotofácil", get_lotofacil))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling()
    

if __name__ == "__main__":
    main() 