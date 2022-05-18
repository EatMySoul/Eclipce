import psycopg2
from config import host,user,password,db_name


class db():

     def __init__(self):
         pass



def create_database():
    try:
        connection = psycopg2.connect(host=host,
                                      user=user,
                                      password=password,
                                      database=db_name)

        with connection.cursor() as cursor:

            cursor.execute('''
               CREATE TABLE IF NOT EXISTS "chats"
               (
               "id" SERIAL PRIMARY KEY,
               "title" VARCHAR(30) UNIQUE,
               "status" INT,
               "icon" TEXT
               );''')

            cursor.execute('''
               CREATE TABLE IF NOT EXISTS "users"
               (
               "id" SERIAL PRIMARY KEY,
               "name" varchar(30),
               "password" varchar(255),
               "icon" TEXT
               );''')

            cursor.execute('''
               CREATE TABLE IF NOT EXISTS "massages"
               (
               "id" SERIAL PRIMARY KEY,
               "massage" TEXT,
               "date_time" TIMESTAMP,
               "chat_id" INT REFERENCES "chats"("id"),
               "user_id" INT REFERENCES "users"("id")
               );''')

            cursor.execute('''
               CREATE TABLE IF NOT EXISTS "chats_users"
               (
               "chat_id" INT REFERENCES "chats"("id"),
               "user_id" INT REFERENCES "users"("id"),
               "user_status" INT
               );''')

            connection.commit()


    except Exception as _e:
        print('[!] Error', _e)
    finally:
        if connection:
            connection.close()




def main():

    create_database()



if __name__ == "__main__":
    main()

