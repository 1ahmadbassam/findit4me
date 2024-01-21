import sqlite3
from sqlite3 import Error


class DatabaseHelper():
    CREATE_SHOPS_TABLE = """CREATE TABLE IF NOT EXISTS shops (
                                        _id integer PRIMARY KEY AUTOINCREMENT,
                                        shopName text NOT NULL,
                                        password text NOT NULL,
                                        location text NOT NULL,
                                        phoneNumber text NOT NULL
                                    );"""
    ADD_SHOP = """ INSERT INTO shops(shopName,password,location,phoneNumber) VALUES(?,?,?,?) """
    ADD_ITEM = """ INSERT INTO shop%s(itemName,itemQuantity,image) VALUES(?,?,?) """
    CREATE_SHOP_TABLE = """CREATE TABLE IF NOT EXISTS shop%s (
                                        _id integer PRIMARY KEY AUTOINCREMENT,
                                        itemName text NOT NULL,
                                        itemQuantity int DEFAULT 0,
                                        image text
                                    );"""
    dbfile = r"database.db"

    @staticmethod
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print("[E] " + str(e))

        return conn

    @staticmethod
    def create_shops_table(conn):
        try:
            cursor = conn.cursor()
            cursor.execute(DatabaseHelper.CREATE_SHOPS_TABLE)
        except Error as e:
            print("[E] " + str(e))

    @staticmethod
    def create_shop(conn, shop):
        try:
            cursor = conn.cursor()
            cursor.execute(DatabaseHelper.ADD_SHOP, shop)
            conn.commit()
            cursor.execute(DatabaseHelper.CREATE_SHOP_TABLE %
                           (cursor.lastrowid))
            return 0
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def get_shop_id(conn, shopname):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT _id FROM shops WHERE shopName = ?""", (shopname,))
            return (''.join(str(x[0]) for x in cursor.fetchall()))
        except Error as e:
            print("[E] " + str(e))
        return -1

    @staticmethod
    def locate_shop(conn, shopname, password):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM shops WHERE shopName = ? AND password = ?""", (shopname, password,))
            rows = cursor.fetchall()

            result = len(rows) - 1
            return result
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def locate_shopname(conn, shopname):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM shops WHERE shopName = ?""", (shopname,))
            rows = cursor.fetchall()

            result = len(rows) - 1
            return result
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def locate_item_exist_in_shop(conn, shopname, itemname):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()

                SQLITE_QUERY = """SELECT * FROM shop%s WHERE itemName = ?"""

                cursor.execute(SQLITE_QUERY % (shopid), (itemname,))
                rows = cursor.fetchall()

                result = len(rows) - 1
                return result
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def add_item_to_shop(conn, shopname, item):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                cursor.execute(DatabaseHelper.ADD_ITEM % (shopid), item)
                conn.commit()
                return 0
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def get_shop_items(conn, shopname):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                SQLITE_QUERY = """SELECT itemName, itemQuantity FROM shop%s"""
                cursor.execute(SQLITE_QUERY % (shopid))
                return cursor.fetchall()
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return None

    @staticmethod
    def delete_item(conn, shopname, itemname):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                SQLITE_DELETE = """DELETE FROM shop%s WHERE itemName=?"""
                cursor.execute(SQLITE_DELETE % (shopid), (itemname,))
                conn.commit()
                return 0
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def update_item(conn, shopname, originalname, itemname, quantity, image):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                SQLITE_UPDATE = """UPDATE shop%s SET itemName = ?, itemQuantity = ?, image = ? WHERE itemName=?"""
                cursor.execute(SQLITE_UPDATE % (shopid), (itemname, quantity, image, originalname,))
                conn.commit()
                return 0
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return 1
    
    @staticmethod
    def delete_all_items(conn, shopname):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                SQLITE_DELETE = """DELETE FROM shop%s"""
                cursor.execute(SQLITE_DELETE % (shopid))
                conn.commit()
                return 0
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def delete_account(conn, shopname):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                SQLITE_DELETE_SHOP_TABLE = """DROP TABLE shop%s"""
                cursor.execute(SQLITE_DELETE_SHOP_TABLE % (shopid))
                cursor.execute("""DELETE FROM shops WHERE shopName=?""", (shopname,))
                conn.commit()
                return 0
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return 1

    @staticmethod
    def get_all_shop_ids(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT _id FROM shops""")
            rows = cursor.fetchall()
            return rows
        except Error as e:
            print("[E] " + str(e))
        return None
    
    @staticmethod
    def get_shopname_from_id(conn, shopid):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT shopName FROM shops WHERE _id = ? """, (shopid,))
            return ''.join(str(x[0]) for x in cursor.fetchall())
        except Error as e:
            print("[E] " + str(e))
        return None

    @staticmethod
    def query_string_location(conn, query, location):
        try:
            cursor = conn.cursor()
            shops = DatabaseHelper.get_all_shop_ids(conn)
            if shops is not None:
                global itemrows
                itemrows = []
                for shop in shops:
                    shopid = shop[0]
                    cursor.execute("""SELECT location FROM shops WHERE _id = ?""", (shopid,))
                    shoplocation = ''.join(str(x[0]) for x in cursor.fetchall())
                    if shoplocation == location:
                        cursor = conn.cursor()
                        cursor.execute("""SELECT itemName, itemQuantity FROM shop%s  WHERE itemName LIKE ?""" % (shopid), ('%'+query+'%',))
                        shopname = DatabaseHelper.get_shopname_from_id(conn, shopid)
                        rows=list(cursor.fetchall())
                        if shopname is not None and rows is not None:
                            for row in rows:
                                listrow=list(row)
                                listrow.append(shopname)
                                itemrows.append(listrow)
                return itemrows
            else:
                print("[E] Error during retreiving shop ids")
        except Error as e:
            print("[E] " + str(e))
        return None
    
    @staticmethod
    def get_phone_for_shop(conn, shopname):
        try:
            cursor = conn.cursor()
            cursor.execute("""SELECT phoneNumber FROM shops WHERE shopName = ?""", (shopname,))
            return cursor.fetchall()[0]
        except Error as e:
            print("[E] " + str(e))
        return ''

    @staticmethod
    def get_image_for_item(conn, shopname, itemname):
        try:
            shopid = DatabaseHelper.get_shop_id(conn, shopname)
            if shopid != -1:
                cursor = conn.cursor()
                cursor.execute("""SELECT image FROM shop%s WHERE itemName = ?""" % (shopid), (itemname,))
                return cursor.fetchall()[0]
            else:
                print("[E] Error during retreiving shop id")
        except Error as e:
            print("[E] " + str(e))
        return ''        
