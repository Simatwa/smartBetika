"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
# Query for results from db limit 10 (results)
# Query for predictions order by id Desc limit 10
# Counter check all home and away teams and get their id
# Update outcome based on the id
from .common import logging
from .common import database as db
from threading import Thread as thr


class evaluater:
    def __init__(self):
        self.perc = []

    # Converts scores to int contained in list
    def getInt(self, score):
        bef = score.split("-")
        aft = []
        if bef[0].isdigit() and bef[1].isdigit():
            aft.append(int(bef[0]))
            aft.append(int(bef[1]))
        else:
            b = [0, 0]
            aft.extend(b)
        return aft

    # Determines win/loss then updates in db
    def marker(self, opt=False):
        data = "❌"
        if opt:
            self.perc.append(1)
            data = "✅"
        return data
        # updateDb(id,column,data,table)

    # Handles ov15 bet
    def ov15(self, outc):
        if sum(outc) >= 2:
            return self.marker(True)
        else:
            return self.marker()

    # Handles ov25 bet
    def ov25(self, outc):
        if sum(outc) >= 3:
            return self.marker(True)
        else:
            return self.marker()

    # Handles home-team win bet
    def one(self, outc):
        if outc[0] > outc[1]:
            return self.marker(True)
        else:
            return self.marker()

    # Handles home-team win or draw bet
    def oneEx(self, outc):
        if outc[0] > outc[1] or outc[0] == outc[1]:
            return self.marker(True)
        else:
            return self.marker()

    # Handles draw bet
    def ex(self, outc):
        if outc[0] == outc[1]:
            return self.marker(True)
        else:
            return self.marker()

    # Handles draw or Away-team win bet
    def exTwo(self, outc):
        if outc[1] > outc[0] or outc[0] == outc[1]:
            return self.marker(True)
        else:
            return self.marker()

    def two(self, outc):
        if outc[1] > outc[0]:
            return self.marker(True)
        else:
            return self.marker()

    # Handles both team to score bet
    def gg(self, outc):
        if outc[0] > 0 and outc[1] > 0:
            return self.marker(True)
            # GG.append(1)
        else:
            return self.marker()

    def mark(self, pick: str, outcome: str) -> str:
        outcome = self.getInt(outcome)
        pick = pick.lower()
        if pick == "ov15":
            rp = self.ov15(outcome)
        elif pick == "ov25":
            rp = self.ov25(outcome)
        elif pick == "1":
            rp = self.one(outcome)
        elif pick == "1x":
            rp = self.oneEx(outcome)
        elif pick == "x":
            rp = self.ex(outcome)
        elif pick == "x2":
            rp = self.exTwo(outcome)
        elif pick == "2":
            rp = self.two(outcome)
        elif pick == "gg":
            rp = self.gg(outcome)
        else:
            rp = "Unknown"
        return rp


class updater(evaluater):
    def __init__(self):
        super().__init__()

    def query_result(self):
        return db.queryDb(
            """
        SELECT Home,Away,Outcome FROM Results ORDER BY ID DESC LIMIT 10"""
        )

    def query_predictions(self):
        return db.queryDb(
            """
        SELECT Id,Home,Away,Choice FROM Predictions WHERE Outcome IS NULL LIMIT 10"""
        )

    def create_predictions_table(self) -> None:
        run = """CREATE TABLE IF NOT EXISTS Predictions(Id INTEGER PRIMARY KEY AUTOINCREMENT,
               Home TEXT, Away TEXT, Choice TEXT, Odds TEXT, Probability TEXT, Outcome TEXT, Mark TEXT, 
               Normal TEXT, Min TEXT,Time NOT NULL DEFAULT CURRENT_TIMESTAMP)"""
        db.queryDb(run)

    def main(self):
        self.create_predictions_table()
        check = lambda: db.queryDb(
            "SELECT COUNT(ID) FROM Predictions WHERE Mark IS NULL"
        )[0][0]
        bef = check()
        results = self.query_result()
        # print(results)
        preds = self.query_predictions()
        logging.debug(f"Results : ", results)
        logging.debug(f"Predictions : ", preds)
        if not preds[0][0] == "0":
            for row in preds:
                for row1 in results:
                    if row[1] == row1[0] and row[2] == row1[1]:
                        db.updateDb(row[0], "Outcome", row1[2], "Predictions")
                        db.updateDb(
                            row[0], "Mark", self.mark(row[3], row1[2]), "Predictions"
                        )
        logging.info(f"Matches marked [{bef-check()}]")


def mark():
    logging.info("Updating and marking scores [Threaded]")
    run = updater()
    t1 = thr(
        target=run.main,
    )
    t1.start()


if __name__ == "__main__":
    mark()
