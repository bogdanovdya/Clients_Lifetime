"""тут будет коннект к бд"""
from mysql.connector import MySQLConnection, Error
from app_settings import DBSetting


class DBConnect:
    @staticmethod
    def connect():
        """
        :return: class DB connection or connection error
        """
        try:
            conn = MySQLConnection(
                host=DBSetting.host,
                database=DBSetting.database,
                user=DBSetting.user,
                password=DBSetting.password
            )
            return conn

        except Error as e:
            return e

    @staticmethod
    def select(query):
        """
        SELECT query
        :param query: string
        :return: dict by KEY or connection error
        """
        try:
            conn = DBConnect.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            result = {}
            for row in cursor:
                result[row[0]] = row[1:]
            return result

        except Error as e:
            return e

        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def insert(query):
        """
        INSERT query
        :param query: string
        :return: error
        """
        try:
            connection = DBConnect.connect()
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()

        except Error as error:
            return error

        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def save_auth(domain, token, refresh_token):
        """
        INSERT or UPDATE BX24 connections tokens
        :param domain: string 3domain name
        :param token: string access token
        :param refresh_token: string refresh token
        """
        query = "INSERT INTO b24_portal_reg(`PORTAL`, `ACCESS_TOKEN`, `REFRESH_TOKEN`) " \
                "values ('{0}', '{1}', '{2}')ON DUPLICATE KEY " \
                "UPDATE `ACCESS_TOKEN` = '{1}', `REFRESH_TOKEN` = '{2}'".format(domain, token, refresh_token)
        DBConnect.insert(query)

    @staticmethod
    def select_token_collection():
        """
        SELECT BX24 connections tokens
        :return: dict BX24 connections tokens
        """
        query = 'SELECT * FROM b24_portal_reg'
        return DBConnect.select(query)
