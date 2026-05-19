"""
Главный файл веб-сервиса.
Лабораторная работа №2, Вариант 6 - Компьютерные комплектующие.
"""

from flask import Flask
from flask_restx import Api
from api.components import api as components_ns

app = Flask(__name__)

# главный API-объект с документацией Swagger
api = Api(
    app,
    version='1.0',
    title='Компьютерные комплектующие API',
    description='Веб-сервис для управления складом компьютерных комплектующих.\n\n'
                'Лабораторная работа №2, Вариант 6.\n\n'
                '**Возможности:**\n'
                '- Просмотр списка комплектующих\n'
                '- Добавление, обновление, удаление\n'
                '- Сортировка по любому полю\n'
                '- Статистика по числовым полям (min, max, avg)',
    doc='/docs',  # Swagger UI будет доступен по адресу /docs
)

# подключение namespace
api.add_namespace(components_ns, path='/api/components')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)