import telebot, csv
from decouple import config #pip install python-decouple
from telebot.types import LabeledPrice


token = config('TOKEN_BOT')
bot = telebot.TeleBot(token)
token_provider = config('TOKEN_PROVIDER')

respostas = {'Ola' : 'Oi, em que posso ajudar ?' , 'Bom dia' : 'tudo bem? em que posso ajudar ?'}

precos = [
    LabeledPrice(label='Meu livro Leandro', amount=401),
    LabeledPrice('Um brinde', 401)
]


def id_user(id_telegram):
    with open('ids_telegram_csv', 'a') as ids:
        e = csv.writer(ids)
        e.writerow([id_telegram])


@bot.message_handler(commands=['start', 'inicio']) # recebe a lita de comandos
def start(message):
    id_user(message.from_user.id)
    #recebe dois parametros id do usuário
    bot.send_message(message.chat.id, "Olá, tudo bem?\nDeseja comprar meu livro em pdf?\nClick /comprar para realizar a compra do livro.")

@bot.message_handler(commands=['comprar'])
def comprar(message):
    bot.send_invoice(
        message.from_user.id,
        title='Robo Leandro Vendas',
        description='Ajude com os meus objetivos, compre meu livro ^^',
        provider_token=token_provider,
        currency='BRL',
        photo_url=config('IMG_PRODUTO'),
        photo_height=512,
        photo_size=512,
        photo_width=512,
        is_flexible=False,
        prices=precos,
        invoice_payload='PAYLOAD'
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkount_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message="Erro ao finalizar sua compra, tente novamente mais tarde!"
    )


@bot.message_handler(content_types=['sucessful_payment'])
def pagou(message):
    doc_testepdf = open('teste.pdf', 'rb')
    bot.send_document(message.chat.id, doc_testepdf)
    bot.send_message(message.from_user.id, 'Agradecemos a sua compra!\nLink do livro foi liberado com sucesso!')


@bot.message_handler(commands=['download'])
def download(message):
    doc_testepdf = open('teste.pdf', 'rb')
    bot.send_document(message.chat.id, doc_testepdf)

@bot.message_handler(func=lambda m: True)
def message_user(message):
    print("Mensagem: ", message.text)
    resp = respostas.get(str(message.text).lower(), 'Não entendi o que você quis dizer, tente novamente!\nVocê pode utilizar a função /help ou /start para iniciar.')
    bot.send_message(message.from_user.id, resp)


bot.skip_pending = True
bot.polling(non_stop=True, interval=0)
