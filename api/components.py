"""
API для работы с компьютерными комплектующими.
Документирование через flask-restx (Swagger).
"""

from flask_restx import Namespace, Resource, fields, reqparse
from models import components_db, next_id as get_next_id
import itertools

# namespace для API
api = Namespace('components', description='API для управления компьютерными комплектующими')

# модель данных для Swagger-документации
component_model = api.model('Component', {
    'id': fields.Integer(readonly=True, description='Уникальный идентификатор'),
    'name': fields.String(required=True, description='Название комплектующего'),
    'category': fields.String(required=True, description='Категория (CPU, GPU, RAM, SSD, HDD, PSU, Motherboard)'),
    'manufacturer': fields.String(required=True, description='Производитель'),
    'price': fields.Float(required=True, description='Цена в рублях'),
    'quantity': fields.Integer(required=True, description='Количество на складе'),
    'power_consumption': fields.Integer(required=True, description='Энергопотребление в Вт'),
})

# модель для статистики
stats_model = api.model('Stats', {
    'field': fields.String(description='Название числового поля'),
    'min': fields.Float(description='Минимальное значение'),
    'max': fields.Float(description='Максимальное значение'),
    'avg': fields.Float(description='Среднее значение'),
})

# парсер для сортировки
sort_parser = reqparse.RequestParser()
sort_parser.add_argument('sort_by', type=str, help='Поле для сортировки', location='args')
sort_parser.add_argument('order', type=str, choices=('asc', 'desc'), default='asc', help='Порядок сортировки', location='args')

# числовые поля - для статистики
NUMERIC_FIELDS = ['price', 'quantity', 'power_consumption']


@api.route('/')
class ComponentList(Resource):
    """
    GET: Получить список всех комплектующих (с возможностью сортировки).
    POST: Добавить новое комплектующее.
    """

    @api.doc('list_components')
    @api.expect(sort_parser)
    @api.marshal_list_with(component_model)
    def get(self):
        """Получить список всех комплектущих с сортировкой."""
        args = sort_parser.parse_args()
        result = components_db.copy()

        # сортировка
        if args['sort_by'] and args['sort_by'] in component_model:
            reverse = args['order'] == 'desc'
            result.sort(key=lambda x: x.get(args['sort_by'], 0), reverse=reverse)

        return result

    @api.doc('create_component')
    @api.expect(component_model)
    @api.marshal_with(component_model, code=201)
    def post(self):
        """Добавить новое комплектующее"""
        global get_next_id
        data = api.payload
        new_component = {
            'id': get_next_id,
            'name': data['name'],
            'category': data['category'],
            'manufacturer': data['manufacturer'],
            'price': float(data['price']),
            'quantity': int(data['quantity']),
            'power_consumption': int(data['power_consumption']),
        }
        components_db.append(new_component)
        get_next_id += 1
        return new_component, 201


@api.route('/<int:id>')
@api.param('id', 'Идентификатор комплектующего')
@api.response(404, 'Комплектующее не найдено')
class ComponentItem(Resource):
    """
    GET: Получить комплектующее по ID.
    PUT: Обновить комплектующее.
    DELETE: Удалить комплектующее.
    """

    @api.doc('get_component')
    @api.marshal_with(component_model)
    def get(self, id):
        """Получить комплектующее по ID"""
        for comp in components_db:
            if comp['id'] == id:
                return comp
        api.abort(404, f"Комплектующее с id {id} не найдено")

    @api.doc('update_component')
    @api.expect(component_model)
    @api.marshal_with(component_model)
    def put(self, id):
        """Обновить комплектующее по ID"""
        data = api.payload
        for comp in components_db:
            if comp['id'] == id:
                comp.update({
                    'name': data.get('name', comp['name']),
                    'category': data.get('category', comp['category']),
                    'manufacturer': data.get('manufacturer', comp['manufacturer']),
                    'price': float(data.get('price', comp['price'])),
                    'quantity': int(data.get('quantity', comp['quantity'])),
                    'power_consumption': int(data.get('power_consumption', comp['power_consumption'])),
                })
                return comp
        api.abort(404, f"Комплектующее с id {id} не найдено")

    @api.doc('delete_component')
    @api.response(204, 'Удалено')
    def delete(self, id):
        """Удалить комплектующее по ID"""
        global components_db
        for i, comp in enumerate(components_db):
            if comp['id'] == id:
                del components_db[i]
                return '', 204
        api.abort(404, f"Комплектующее с id {id} не найдено")


@api.route('/stats')
class ComponentStats(Resource):
    """
    GET: Получить статистику по всем числовым полям (min, max, avg).
    """

    @api.doc('get_stats')
    @api.marshal_list_with(stats_model)
    def get(self):
        """Получить статистику по числовым полям"""
        stats = []
        for field in NUMERIC_FIELDS:
            values = [comp[field] for comp in components_db]
            stats.append({
                'field': field,
                'min': min(values),
                'max': max(values),
                'avg': round(sum(values) / len(values), 2),
            })
        return stats