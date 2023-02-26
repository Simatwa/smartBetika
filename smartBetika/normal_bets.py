"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

# Places normal bets
from .common import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


class normal_bets:
    logging.info("Handling normal bets")

    def __init__(self, driver, args):
        self.driver = driver
        self.args = args
        if self.args.upcoming:
            self.update_html()
            try:
                area = self.driver.find_element(
                    By.XPATH, '//button[@class="prematch-nav__item"]'
                )
                self.driver.execute_script("arguments[0].click();", area)
            except:
                pass
        # Navigates the page so as to load more matches
        for x in range(self.args.scrolls):
            self.driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.PAGE_DOWN)
            screenshot(self.driver, self.args, f"normal_display_{str(x)}")
            sleep(0.6)

    # Updates the current html being displayed in page-source
    def update_html(self):
        self.driver.execute_script("return document.body.innerHTML;")
        sleep(self.args.sleep)
        return self.driver.page_source

    # Initially creating the normal bets table
    def create_normal_table(self):
        database.queryDb("DROP TABLE Normal")
        run = """CREATE TABLE IF NOT EXISTS Normal(ID INTEGER PRIMARY KEY AUTOINCREMENT,
        League TEXT, Date TEXT,Time TEXT, Home TEXT, Away TEXT, h_odds TEXT, x_odds TEXT,
        a_odds TEXT, State TEXT, Category TEXT, Type TEXT, Markets TEXT, Pick TEXT, Choice TEXT, Prob TEXT,
         C_time NOT NULL DEFAULT CURRENT_TIMESTAMP)"""
        database.queryDb(run)

    # Hunts down relevant data and save them in database
    def find_teams(self):
        logging.info("Finding teams")
        soup1 = soup(self.update_html()).souper()
        sorted = []
        for data in soup1.find_all(
            "div", {"class": "prebet-match"}, limit=self.args.amount
        ):
            info = soup(data).decompose(sep=",")
            try:
                data2 = tuple(info.split(",")[:12])
                sorted.append(str(data2))
            except Exception as e:
                logging.debug(str(e))
        if sorted:
            logging.info(f"Normal matches found [{len(sorted)}]")
            col = (
                "League",
                "Date",
                "Time",
                "Home",
                "Away",
                "H_odds",
                "X_odds",
                "A_odds",
                "State",
                "Category",
                "Type",
                "Markets",
            )
            self.create_normal_table()
            database.insert_once(table="Normal", col=col, data=sorted)
            return "Normal"
        else:
            logging.warning("Normal matches NOT available!")

    # Place bets on the predicted matches
    def place_bets(self):
        pass

    # Main function
    def main(self):
        return self.find_teams()


if __name__ == "__main__":
    pass
