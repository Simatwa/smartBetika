"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

# Queries for team names in the specified db
# Query their preds and update them in db
from .common import *
import cloudscraper
import json
from sys import exit, platform
from os import path


class api_interactor:
    def __init__(self, user, paswd, url, test=False):
        self.req = cloudscraper.create_scraper(
            delay=False,
            debug=False,
            disableCloudflareV1=True,
            browser={
                "platform": "windows" if "win" in platform else platform.lower(),
                "browser": "chrome",
                "desktop": True,
            },
        )
        auth = self.post({"user": user, "paswd": paswd}, path.join(url, "login"))
        if auth[0] and auth[1].get("status_code") == 200:
            if not test:
                logging.info("Login successfull @smartbets_API")
        else:
            resp = auth[1]
            if type(resp) is dict:
                logging.critical(
                    f"Login failed @smartbets_API: Code=[{resp['status_code']}] Type=[{resp['type']}]"
                )
            else:
                logging.critical(str(resp))
            exit("Exitting")
        self.url = url

    # sends get request to the api
    def get(self, url=False, param=False):
        if not url:
            url = path.join(self.url, "predict")
        try:
            if param:
                resp = self.req.get(url=url, params=param)
            else:
                resp = self.req.get(url=url)
            return (
                True,
                {
                    "status_code": resp.status_code,
                    "type": resp.headers["Content-type"],
                    "data": resp.text,
                },
            )
        except Exception as e:
            return (False, str(e))

    # Sends post request to the api
    def post(self, param, url=False):
        if not url:
            url = path.join(self.url, "predict")
        try:
            resp = self.req.post(url=url, data=param)
            return (
                True,
                {
                    "status_code": resp.status_code,
                    "type": resp.headers["Content-type"],
                    "data": resp.text,
                },
            )
        except Exception as e1:
            return (False, str(e1))


class predictor:
    def __init__(self, args, tbl_name: str):
        self.args = args
        self.table = tbl_name
        self.web = api_interactor(args.username, args.paswd, args.host)

    # Finalizes by updating pick,choice and PROBABILITY of occuring
    def update_pred(self, id, data):
        try:
            info = json.loads(data)
            database.queryDb(
                f"""
            UPDATE {self.table} SET Pick="{info['pick']}", Prob="{info['choice']}",
            Choice="{info['result']}" WHERE ID={id}
            """
            )
        except Exception as e:
            logging.error(str(e))

    # Converts match to dict as per API need
    def sort_teams(self, match: tuple):
        return {"home": match[0], "away": match[1], "net": self.args.net}

    # Def get_details
    def get_teams(self):
        if self.table.lower() in ("normal") and self.args.league:
            inf = database.queryDb(
                f"""SELECT Id,Home,Away from {self.table} WHERE league LIKE 
            '{self.args.league}%' OR league LIKE '%{self.args.league}' OR League LIKE '%{self.args.league}%'
             ORDER BY ID LIMIT {self.args.amount}"""
            )
        else:
            inf = database.queryDb(
                f"""
            SELECT Id,Home,Away from {self.table} ORDER BY ID LIMIT {self.args.amount}
            """
            )
        if inf == "0":
            rp = False
        else:
            rp = inf
        return rp

    # Main predict controller
    def predictor(self):
        matches = self.get_teams()
        logging.info(f"Total matches [{len(matches)}]")
        if matches:
            from tqdm import tqdm
            from colorama import Fore

            logging.info("Predicting on each match!")
            with tqdm(
                total=len(matches),
                bar_format="%s{bar}%s %s{l_bar}%s"
                % (Fore.MAGENTA, Fore.RESET, Fore.RED, Fore.RESET),
            ) as pbar:
                for entry in matches:
                    data = self.sort_teams(entry[1:])
                    if self.args.post:
                        resp = self.web.post(data)
                    else:
                        resp = self.web.get(param=data)
                    if (
                        resp[0]
                        and resp[1]["status_code"] == 200
                        and "json" in resp[1]["type"]
                    ):
                        self.update_pred(entry[0], resp[1].get("data"))
                    else:
                        logging.error(f"Unable to process {data}")
                    pbar.update(1)
        else:
            logging.warning(f"No matches found in {self.table}")
