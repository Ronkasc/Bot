import telebot
import requests

class WeatherBot:
    def __init__(self, token, owm_api_key, owm_api_url):
        self.token = token
        self.owm_api_key = owm_api_key
        self.owm_api_url = owm_api_url
        self.bot = telebot.TeleBot(self.token)

    def run(self):
        @self.bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            self.bot.reply_to(message, 'Я бот, который показывает текущую погоду. Просто напиши мне название города.')

        @self.bot.message_handler(commands=['dev'])
        def send_welcome(message):
            self.bot.reply_to(message, 'Разработчик - Титов Илья Андреевич\n Студент группы Пкс-1-21')

        @self.bot.message_handler(func=lambda message: True)
        def get_weather(message):
            try:
                city = message.text
                params = {'q': city, 'appid': self.owm_api_key, 'units': 'metric'}
                response = requests.get(self.owm_api_url, params=params)
                data = response.json()

                if data['cod'] == '404':
                    self.bot.reply_to(message, 'Город не найден. Попробуйте еще раз.')
                else:
                    weather_info = f"Погода в городе {city}:\nТемпература: {data['main']['temp']}°C\nВлажность: {data['main']['humidity']}%\n"
                    self.bot.reply_to(message, weather_info)
            except Exception as e:
                self.bot.reply_to(message, f'Произошла ошибка: {str(e)}')

        self.bot.polling()



if __name__ == "__main__":
    TOKEN = '6703266772:AAH_1PafH2tXrDWuW9YwCHSzj7A75vk6T0U'
    OWM_API_KEY = '45a2df05dbb25bb9a503b70ebc25f74b'
    OWM_API_URL = 'http://api.openweathermap.org/data/2.5/weather'

    weather_bot = WeatherBot(TOKEN, OWM_API_KEY, OWM_API_URL)
    weather_bot.run()

