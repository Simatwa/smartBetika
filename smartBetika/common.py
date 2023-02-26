"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

import logging, sqlite3
from bs4 import BeautifulSoup as bts
from datetime import datetime
from os import system, path, remove
from time import sleep as wait

fmt4 = datetime.today().strftime("%d_%b_%Y__%H_%M_%S")
logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s",
    datefmt="%H:%M:%S %d-%b-%Y",
    level=logging.INFO,
)
dbnm = "smartbets3.db"


# takes screenshot of the pages
def screenshot(driver: object, args: object, name: str) -> None:
    if args.screenshot:
        try:
            wait(0.2)
            driver.save_screenshot(f"{args.path}/{name}.png")
        except Exception as e:
            ex = str(e).split("\n")[0]
            logging.warning(f"Failed to screenshot,{name} - {ex}")


# Removes the initial db used by the program
def remove_db():
    if path.isfile(dbnm):
        try:
            remove(dbnm)
        except Exception as e:
            logging.error(f"Failed to delete database - {str(e)}")
    if path.isfile("chromedriver"):
        try:
            remove("chromedriver")
        except Exception as e:
            logging.error(f"Failed to delete chromedriver - {str(e)}")


# Controls other function in try
def control(func):
    try:
        func()
    except Exception as e:
        logging.error(str(e))
        return (False, str(e))
    else:
        return True


# Converts datatype to list
def convToList(data):
    file8 = []
    for dat in data:
        file8 = file8 + list(dat)
    return file8


# Performs file related operations
class file_operation:
    def __init__(self, fnm):
        self.fnm = fnm

    # opens file
    def open(self):
        try:
            with open(self.fnm) as file:
                return file.read()
        except Exception as e:
            logging.error(str(e))
            return False

    # save file contents
    def save(self, data, mode="w"):
        try:
            with open(self.fnm, mode) as file:
                file.write(str(data))
        except Exception as e:
            logging.error(str(e))
            return False


# Soups str data
class soup:
    def __init__(self, html):
        self.soup1 = bts(str(html), "html.parser")

    def souper(self):
        return self.soup1

    def decompose(self, sep="\n"):
        for data in self.soup1(["style", "script"]):
            data.decompose
        return f"{sep}".join(self.soup1.stripped_strings)

    def prettify(self):
        return self.soup1.prettify()


# Handles dbs related functions
class database:
    # Runs sql commands against the db
    def queryDb(self, sql):
        conn = sqlite3.connect(dbnm)
        csr = conn.cursor()
        try:
            dat = csr.execute(sql)
            data = csr.fetchall()
        except Exception as e:
            logging.debug(f"{str(e)}\n{sql}")
            data = "0"
        else:
            conn.commit()
            if not data:
                data = "0"
        finally:
            csr.close()
            conn.close()
        return data

    # Inserts two columns  in a db-table
    def insertDb(self, table, col1, col2, data1, data2):
        conn = sqlite3.connect(dbnm)
        csr = conn.cursor()
        run = f"INSERT INTO {table}({col1},{col2}) VALUES(?,?)"
        try:
            csr.execute(run, (data1, data2))
            csr.close()
        except Exception as e:
            logging.error(str(e))
        conn.commit()
        conn.close()

    # Inserts rows in db-table in multiple columns
    def insertDb2(self, table, col: tuple, data: tuple):
        quiz = []
        for x in range(len(col)):
            quiz.append("?")
        conn = sqlite3.connect(dbnm)
        csr = conn.cursor()
        run = f"INSERT INTO {table}({','.join(col)}) VALUES({','.join(quiz)})"
        try:
            csr.execute(run, tuple(data))
            csr.close()
        except Exception as e:
            logging.error(str(e))
            pass
        conn.commit()
        conn.close()

    # Inserts rows in a table at once
    def insert_once(self, table, col: tuple, data: tuple) -> None:
        run = f"""INSERT INTO {table}({','.join(col)}) VALUES{','.join(data)};"""
        self.queryDb(run)

    # Updating db data
    def updateDb(self, id, column, data, table):
        if type(id) is str or int:
            id = ["Id", id]
        try:
            conn = sqlite3.connect(dbnm)
            csr = conn.cursor()
            run = (
                f"""UPDATE  {table} SET  {column}='{data}'  WHERE {id[0]}='{id[1]}' """
            )
            csr.execute(run)
            csr.close()
            conn.commit()
            conn.close()
        except Exception as e:
            logging.error(str(e))
            pass


database = database()
logging.info("smartBets3 started")
