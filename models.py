"""
Модель данных для компьютерных комплектующих.
"""

# хранилище данных в памяти
components_db = [
    {
        'id': 1,
        'name': 'Ryzen 7 7800X3D',
        'category': 'CPU',
        'manufacturer': 'AMD',
        'price': 45000.0,
        'quantity': 15,
        'power_consumption': 120
    },
    {
        'id': 2,
        'name': 'GeForce RTX 4070',
        'category': 'GPU',
        'manufacturer': 'NVIDIA',
        'price': 65000.0,
        'quantity': 8,
        'power_consumption': 200
    },
    {
        'id': 3,
        'name': 'DDR5 32GB Kit',
        'category': 'RAM',
        'manufacturer': 'Kingston',
        'price': 12000.0,
        'quantity': 30,
        'power_consumption': 10
    },
    {
        'id': 4,
        'name': 'Samsung 990 Pro 2TB',
        'category': 'SSD',
        'manufacturer': 'Samsung',
        'price': 18000.0,
        'quantity': 20,
        'power_consumption': 8
    },
]

# счётчик для генерации новых ID
next_id = 5