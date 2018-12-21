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
