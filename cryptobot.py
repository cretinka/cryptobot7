import telebot
import requests

TOKEN = "6433098966:AAFaMkonP6tbKjld6h9gu00HLxX_d7Iqgf0"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который покажет цену валюты. Просто введите команду в формате:\n/currency base quote количество\nНапример: /currency usd eur 10")

@bot.message_handler(commands=['currency'])
def get_currency_price(message):
    try:
        command, base_currency, quote_currency, amount = message.text.split()

        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": f"{base_currency}",
            "vs_currencies": "usd,eur,rub",
        }
        response = requests.get(url, params=params)
        data = response.json()

        base_to_usd_rate = data.get(base_currency, {}).get("usd", 0)
        if base_to_usd_rate == 0:
            bot.send_message(message.chat.id, "Не удалось получить курс валюты. Пожалуйста, убедитесь, что вы используете корректный код валюты.")
            return

        if base_currency == quote_currency:
            bot.send_message(message.chat.id, "Нельзя конвертировать валюту в саму себя.")
            return

        price = (1 / base_to_usd_rate) * float(amount)
        bot.send_message(message.chat.id, f"Цена {amount} {base_currency.upper()} в {quote_currency.upper()}: {price:.2f} {quote_currency.upper()}")

    except (ValueError, IndexError):
        bot.send_message(message.chat.id, "Пожалуйста, введите команду в формате /currency base quote количество\nНапример: /currency usd eur 10")

bot.polling(none_stop=True)