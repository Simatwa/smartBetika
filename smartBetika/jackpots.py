"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .common import *
from time import sleep


class category:
    def __init__(self, driver, args):
        self.driver = driver
        self.args = args
        self.column = ("home", "away", "h_odds", "x_odds", "a_odds")

    # Updates the html content with the js fetched contents
    def update_html(self):
        self.driver.execute_script("return document.body.innerHTML;")
        sleep(self.args.sleep)
        return self.driver.page_source

    # Creates relevant table in the database
    def create_table(self, tbnm: str):
        database.queryDb(f"DROP Table {tbnm}")
        database.queryDb(
            f"""
        CREATE TABLE IF NOT EXISTS {tbnm}(Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Home TEXT, Away TEXT, h_odds TEXT, x_odds TEXT, a_odds TEXT, Pick TEXT, Choice TEXT, Prob TEXT,
        C_time NOT NULL DEFAULT CURRENT_TIMESTAMP)"""
        )

    def nav_down(self):
        self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_DOWN)

    # Handles Grand_jackpot
    def grand_jackpot(self):
        logging.info("Hunting down Grand-jackpot matches!")
        self.driver.get("https://www.betika.com/en-ke/jackpots/")
        for x in range(3):
            self.nav_down()
            screenshot(self.driver, self.args, f"grand_jackpot{x}")
        return self.extract_jp("grandjp")

    # Handles mid-week jackpots
    def midweek_jackpot(self):
        logging.info("Hunting down midweek-jackpot matches!")
        self.driver.get("https://www.betika.com/en-ke/jackpots/midweekjp")
        for x in range(2):
            self.nav_down()
            screenshot(self.driver, self.args, f"mid_week_jackpot{x}")
        return self.extract_jp("midjp")

    # Extracts jackpots data
    def extract_jp(self, table: str):
        tbl = table.capitalize()
        html, sorted = self.update_html(), []
        matches = (
            soup(html).souper().find_all("table", {"class": "jackpot-event__match"})
        )
        for data in matches:
            try:
                info = soup(data).decompose(sep=",").split(",")
                home, away, odd1, oddx, odd2 = (
                    info[4],
                    info[5],
                    info[7],
                    info[9],
                    info[11],
                )
                sorted.append(str((home, away, odd1, oddx, odd2)))
            except Exception as e:
                logging.debug(str(e))
        if matches:
            logging.info(f"{tbl} matches found [{len(sorted)}]")
            self.create_table(table)
            database.insert_once(table=table, col=self.column, data=sorted)
            return table
        else:
            logging.warning(f"{tbl} matches NOT available")

    # handles sababisha matches
    def sababisha(self):
        logging.info("Hunting down sababisha matches!")
        self.driver.get("https://www.betika.com/en-ke/jackpots/sababisha/")
        for x in range(2):
            self.nav_down()
            screenshot(self.driver, self.args, f"sababisha{x}")
        return self.sababisha_extract()

    # Extracts all relevant data from the html [sababisha]
    def sababisha_extract(self):
        logging.debug("Extracting and saving the matches")
        all_bets = self.driver.find_element(
            By.XPATH,
            '//div[@class="jackpot__event__details overlay-menu__strocked-card"]',
        )
        self.driver.execute_script("arguments[0].click();", all_bets)
        sorted, table = [], "Sababisha"
        for data in soup(self.update_html()).souper().find_all("tr"):
            try:
                t = soup(data).decompose(sep=",").split(",")
                home, away, odd1, oddx, odd2 = t[0], t[1], t[3], t[5], t[7]
                sorted.append(str((home, away, odd1, oddx, odd2)))
            except Exception as e:
                logging.debug(str(e))
        if sorted:
            logging.info(f"{table} matches found [{len(sorted)}]")
            self.create_table(table)
            database.insert_once(table=table, col=self.column, data=sorted)
            return table
        else:
            logging.warning(f"{table} matches NOT available!")

    # Main function
    def main(self) -> list:
        resp = []  # Contains table_name in database where match-data have been saved
        if self.args.sababisha:
            tbl = self.sababisha()
            if tbl:
                resp.append(tbl)
        if self.args.midjp:
            tbl = self.midweek_jackpot()
            if tbl:
                resp.append(tbl)
        if self.args.grandjp:
            tbl = self.grand_jackpot()
            if tbl:
                resp.append(tbl)
        return resp
