from peewee import *

db = SqliteDatabase('musicians.db')


class User(Model):
    id = PrimaryKeyField()
    chat_id = IntegerField()
    city = CharField()

    class Meta:
        database = db  # модель будет использовать базу данных 'musicians.db'


class Artist(Model):
    id = PrimaryKeyField()
    b_in_t_id = IntegerField()
    name = CharField()
    information = TextField()

    class Meta:
        database = db


class Relation(Model):
    user_id = IntegerField()
    artist_id = IntegerField()

    class Meta:
        database = db


def add_user(chat_id):

    User.get_or_create(chat_id=chat_id, city="moscow")


def add_relation(chat_id, artist_b_in_t_id, artist_name, events):

    artist = Artist.select().where(Artist.b_in_t_id == artist_b_in_t_id)
    if not artist:
        Artist.create(b_in_t_id=artist_b_in_t_id, name=artist_name, information=events)
        artist = Artist.select().where(Artist.b_in_t_id == artist_b_in_t_id)

    user = User.select().where(User.chat_id == chat_id)
    Relation.get_or_create(user_id=user.dicts().get()['id'], artist_id=artist.dicts().get()['id'])


def del_relation(chat_id, artist_b_in_t_id):
    artist = Artist.select().where(Artist.b_in_t_id == artist_b_in_t_id)
    user = User.select().where(User.chat_id == chat_id)
    if artist:
        user_id = user.dicts().get()['id']
        artist_id = artist.dicts().get()['id']
        relation = Relation.delete().where(Relation.user_id == user_id, Relation.artist_id == artist_id).execute()
    else:
        relation = 0
    return relation


def get_relations(chat_id):

    user = User.select().where(User.chat_id == chat_id)

    artists_name = []
    for relation in Relation.select().where(Relation.user_id == user.dicts().get()['id']):
        artist = Artist.select().where(Artist.id == relation.artist_id)
        artists_name.append(artist.dicts().get()['name'])

    return artists_name


def add_tables():

    try:
        User.create_table()
    except OperationalError:
        print("User table already exists!")

    try:
        Artist.create_table()
    except OperationalError:
        print("Artist table already exists!")

    try:
        Relation.create_table()
    except OperationalError:
        print("Relation table already exists!")


if __name__ == "__main__":

    add_tables()
    # user = User.create(chat_id=126789, city="Moscow")

    # for user in User.select():
    #     print(user.id, " ", user.chat_id)

    # for artist in Artist.select():
    #     print(artist.id, " ", artist.b_in_t_id," ", artist.information)

    # # show relations
    # for relation in Relation.select():
    #     print(relation.user_id, " ", relation.artist_id)

    # user = User.select().where(User.id == 1)
    # print(user.dicts().get()['id'])

    # show users
    # for artist in User.select().where(User.id == 1):
    #     print(artist.chat_id)
