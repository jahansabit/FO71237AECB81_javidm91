import sqlite3
import textwrap

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
                `last_sent_price` FLOAT,
                `last_sent_time` DATETIME
            );'''
        ))
        self.con.commit()
        cur.close()

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
        print(all_data)
        cur.close()
        return all_data

    def delete_link(self, index):
        all_data = self.get_links()
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        id = all_data[index][0]
        print(id)
        cur.execute("DELETE FROM search_page_links WHERE id = ?", (id,))
        self.con.commit()
        cur.close()

    def save_summary(self, summary, user_id):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute("INSERT INTO data(summary, user_id) VALUES(?, ?)", (summary, user_id))
        summary = summary.replace("'", "''")
        cur.execute(f"UPDATE data SET summary = '{summary}' WHERE user_id = {user_id}")
        self.con.commit()
        cur.close()

    def get_summary(self, user_id):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute("SELECT summary FROM data WHERE user_id=?", (user_id,))
        summary = cur.fetchone()
        self.con.commit()
        cur.close()
        if summary:
            return summary
        else:
            return None

    def validate(self, username, password):
        self.con = sqlite3.connect(self.name)
        cur = self.con.cursor()
        cur.execute("SELECT password FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        self.con.commit()
        cur.close()
        if user:
            if user[0] == password:
                return True
            else:
                return False
        else:
            return False

    def close(self):
        self.con.commit()
        self.con.close()

if __name__ == "__main__":
    db = DataBase("test.db")
    # db.save_summary("here 34234'it is 23423", 2)
    # print(db.get_summary(2))

    # db.add_link("https://google", 500, channel_id="@2342we", last_scraped="2020-03-42")
    db.delete_link(1)
    db.get_links()
    