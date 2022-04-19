import sqlite3
import textwrap
import json

from bot_vars import *


class DataBase:

    def __init__(self, name=DB_FILE_PATH):
        self.name = name
        self.con = sqlite3.connect(name)
        cur = self.con.cursor()
        cur.execute(textwrap.dedent(
            '''CREATE TABLE IF NOT EXISTS `search_page_links` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `link` TEXT NOT NULL,
                `price_limit` FLOAT,
                `channel_id` TEXT,
                `last_scraped` DATETIME DEFAULT NULL
            );'''
        ))
        cur.execute(textwrap.dedent('''
            CREATE TABLE IF NOT EXISTS `products` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `search_page_links_id` INT NOT NULL,
                `link` TEXT,
                `name` TEXT,
                `price` FLOAT,
                `img_link` TEXT,
                `category` TEXT,
                `availability` TEXT,
                `last_sent_price` FLOAT DEFAULT '-1',
                `last_sent_time` DATETIME
            );'''
        ))
        self.con.commit()
        cur.close()
    
    def query_db(self, query, args=(), one=False):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.connection.close()
        return (r[0] if r else None) if one else r

    def add_link(self, link, price_limit, channel_id=None, last_scraped=None):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute(textwrap.dedent('''
            INSERT INTO `search_page_links` (link, price_limit, channel_id, last_scraped) VALUES(?, ?, ?, ?)
            '''
        ), (link, price_limit, channel_id, last_scraped))
        self.con.commit()
        cur.close()
    
    def get_links(self):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM `search_page_links`")
        all_data = cur.fetchall()
        self.con.commit()
        # print(all_data)
        cur.close()
        return all_data
    
    def get_links_json(self):
        res = self.query_db("SELECT * FROM `search_page_links`")
        return res

    def delete_link(self, index):
        all_data = self.get_links()
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        id = all_data[index][0]
        print(id)
        cur.execute("DELETE FROM search_page_links WHERE id = ?", (id,))
        self.con.commit()
        cur.close()
    
    def update_search_page_last_scraped(self, index, last_scraped):
        all_data = self.get_links()
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        id = all_data[index][0]
        cur.execute("UPDATE search_page_links SET last_scraped = ? WHERE id = ?", (last_scraped, id))
        self.con.commit()
        cur.close()
    
    def add_product(self, link, name, price, img_link, category, availability, search_page_links_id):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute(textwrap.dedent('''
            INSERT INTO `products` (link, name, price, img_link, category, availability, search_page_links_id) VALUES(?, ?, ?, ?, ?, ?, ?)
            '''
        ), (link, name, price, img_link, category, availability, search_page_links_id))
        self.con.commit()
        cur.close()
    
    def add_product_json(self, product):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute(textwrap.dedent('''
            INSERT INTO `products` (link, name, price, img_link, category, availability, search_page_links_id) VALUES(?, ?, ?, ?, ?, ?, ?)
            '''
        ), (product['link'], product['name'], product['price'], product['img_link'], product['category'], product['availability'], product['search_page_links_id']))
        self.con.commit()
        cur.close()
    
    def update_product_json(self, product):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute(textwrap.dedent('''
            UPDATE products SET link = ?, name = ?, price = ?, img_link = ?, category = ?, availability = ?, search_page_links_id = ? WHERE id = ?
            '''
        ), (product['link'], product['name'], product['price'], product['img_link'], product['category'], product['availability'], product['search_page_links_id'], product['id']))
        self.con.commit()
        cur.close()
    
    def get_products(self):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM `products`")
        all_data = cur.fetchall()
        self.con.commit()
        # print(all_data)
        cur.close()
        return all_data
    
    def get_products_json(self):
        res = self.query_db("SELECT * FROM `products`")
        return res
    
    def delete_product(self, index):
        all_data = self.get_products()
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        id = all_data[index][0]
        print(id)
        cur.execute("DELETE FROM products WHERE id = ?", (id,))
        self.con.commit()
        cur.close()
    
    def search_product(self, name, link):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute("SELECT * FROM `products` WHERE name=? AND link=?", (name, link))
        all_data = cur.fetchall()
        self.con.commit()
        # print(all_data)
        cur.close()
        return all_data
    
    def search_product_json(self, name, link):
        res = self.query_db("SELECT * FROM `products` WHERE name=? AND link=?", (name, link))
        return res

    def update_product_price(self, index, price):
        all_data = self.get_products()
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        id = all_data[index][0]
        cur.execute("UPDATE products SET price = ? WHERE id = ?", (price, id))
        self.con.commit()
        cur.close()
   

    def close(self):
        self.con.commit()
        self.con.close()

if __name__ == "__main__":
    db = DataBase("test.db")
    # db.save_summary("here 34234'it is 23423", 2)
    # print(db.get_summary(2))

    # db.add_link("https://google", 500)
    # db.add_link("https://fb", 234)
    # db.add_link("https://gg.com", 280, None, "2020-01-01 16:12:00")

    # # db.delete_link(1)
    # print(db.get_links())
    # all_search_pages = db.get_links()
    # all_search_pages_links = [search_page[1] for search_page in all_search_pages]
    # print(all_search_pages_links)
    # db.delete_link(0)
    # db.add_product("https://google.com", "test234234", "234", "https://google.com", "test", "test", 1)
    # db.add_product("https://google.com", "testing_salt234234", "234", "https://google.com", "test", "test", 1)
    # db.delete_product(2)

    # print(db.search_product("test234234"))
    # print(db.get_products())
    res = db.get_links_json()
    print(res)
    print(type(res))
    