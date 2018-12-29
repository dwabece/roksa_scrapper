HOST = 'localhost'

RABBIT_HOST = HOST
RABBIT_USER = 'guest'
RABBIT_PASSWORD = 'guest'
RABBIT_URL = f'amqp://{RABBIT_USER}:{RABBIT_PASSWORD}@{RABBIT_HOST}:5672/'

MONGO = {
    'host': 'localhost',
    'port': '27017',
    'db': 'rox',
    'user': None,
    'password': None
}


def get_mongo_url():
    return 'mongodb://{host}:{port}/{db}'.format(
        host=MONGO.get('host'),
        port=MONGO.get('port'),
        db=MONGO.get('db')
    )
