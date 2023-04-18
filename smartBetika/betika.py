#!/usr/bin/python3
"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
from . import __version__, __author__

program_info = "Football-Punter's favorite girlfriend - based on Betika platform!"
license_info = "[*] This program is disseminated under MIT-FPA license."
github_adlink = "https://github.com/Simatwa/smartBetika/raw/main/page-ad.txt"


def error_handler(quit=True):
    def wrapper(func):
        def main(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                err = e.args[1] if len(e.args) > 1 else str(e)
                if quit:
                    exit(logging.critical(err))
                else:
                    logging.error(err)

        return main

    return wrapper


@error_handler()
def get_args():
    import argparse

    parser = argparse.ArgumentParser(description=program_info, epilog=license_info)
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + "v" + __version__
    )
    parser.add_argument(
        "-pn", "--phone", help="Phone number for authenticating login [Betika]"
    )
    parser.add_argument(
        "-pas", "--password", help="Pass-key associated with the phone number"
    )
    parser.add_argument(
        "-lg",
        "--league",
        help="Filter specific league or country of the teams [Normal]",
    )
    parser.add_argument(
        "-amt",
        "--amount",
        help="Maximum number of matches to predict",
        type=int,
        default=20,
    )
    parser.add_argument(
        "-scr",
        "--scrolls",
        help="Number of times to scroll on updating matches [Normal]",
        default=8,
        type=int,
    )
    parser.add_argument(
        "-slp",
        "--sleep",
        help="Period for waiting after refreshing JS delivered contents",
        type=int,
        default=3,
    )
    parser.add_argument(
        "-api",
        "--host",
        help="Web url for the prediction API",
        default="http://localhost:8080/",
    )
    parser.add_argument(
        "-user",
        "--username",
        help="Username for authenticating at the API",
        default="API",
    )
    parser.add_argument(
        "-psd",
        "--paswd",
        help="Password for authenticating at the API",
        default="developer",
    )
    parser.add_argument(
        "-drv",
        "--driver",
        help="Chromedriver executable path [download - loads new]",
        default=False,
    )
    parser.add_argument(
        "-tbl",
        "--table",
        help="Table type to be used in formatting the data [tabulate]",
        default="fancy_grid",
        choices=["grid", "orgtbl", "pretty", "html"],
    )
    parser.add_argument(
        "-dir",
        "--path",
        help="Directory for saving the screenshots",
        default="Screenshots",
    )
    parser.add_argument(
        "--disable-incognito",
        help="Start browser in non-incognito mode",
        action="store_true",
        dest="disable_incognito",
    )
    parser.add_argument(
        "--normal",
        help="Specifies to handle match-highlights of the day",
        action="store_true",
    )
    parser.add_argument(
        "--grandjp",
        help="Specifies to handle grand-jackpot matches",
        action="store_true",
    )
    parser.add_argument(
        "--midjp",
        help="Specifies to handle midweek-jackpot matches",
        action="store_true",
    )
    parser.add_argument(
        "--sababisha", help="Specifies to handle sababisha matches", action="store_true"
    )
    parser.add_argument(
        "--upcoming", help="Specifies to handle upcoming matches", action="store_true"
    )
    parser.add_argument(
        "--predict", help="Proceed to predict on the matches", action="store_true"
    )
    parser.add_argument(
        "--screenshot",
        help="Take screenshot on every page visited",
        action="store_true",
    )
    parser.add_argument(
        "--net", help="Instruct API to fetch team_data from web", action="store_true"
    )
    parser.add_argument(
        "--post", help="Use post method when interacting with API", action="store_true"
    )
    parser.add_argument(
        "--verbose",
        help="Output all team data in the specified filepath",
        action="store_true",
    )
    parser.add_argument(
        "--no-clear",
        help="Not to delete the files used by the script",
        action="store_true",
        dest="noclear",
    )
    parser.add_argument(
        "--display", help="Run Chrome browser in GUI", action="store_true"
    )
    parser.add_argument(
        "--view",
        help="View the matches in Chrome after predicting - Linux",
        action="store_true",
    )
    parser.add_argument(
        "--get-API",
        help="Request the API program for making predictions from the DEVELOPER.",
        dest="get_api",
        action="store_true",
    )
    parser.add_argument(
        "output", nargs="?", help="Filepath for saving the predictions", default=None
    )
    return parser.parse_args()


# Gets current_time
args, exit_msg = get_args(), []
if args.get_api:
    from webbrowser import open

    open("https://t.me/+M4AuGkLGrx05YjY0")
    from sys import exit

    exit()
from .common import *
from sys import exit, platform


def date():
    from datetime import datetime

    now = datetime.today()
    return str(now.strftime("%d-%b-%Y %H:%M:%S"))


# Handles critical errors finally exit
def exit_error(msg: str) -> None:
    from colorama import Fore

    if not msg:
        if not exit_msg:
            logging.info(f"Exiting ~ Goodbye!")
            exit_msg.append(True)
            exit()
    else:
        exit(logging.critical(Fore.RED + str(msg) + Fore.RESET))
    if not args.noclear:
        remove_db()


if args.normal or args.grandjp or args.midjp or args.sababisha or args.upcoming:
    pass
else:
    from colorama import Fore

    reset = Fore.RESET
    logging.critical(
        Fore.RED
        + "None of [normal,upcoming,sababisha,midjp,grandjp] command is parsed!"
        + reset
    )
    exit_error(False)
if not args.predict:
    logging.warning(
        f"Won't proceed evaluating performance [--predict : {args.predict}]!"
    )
else:
    from .predict_maker import api_interactor

    api_interactor(args.username, args.paswd, args.host, test=True)
if args.screenshot:
    try:
        from os import mkdir, path

        if not path.isdir(args.path):
            mkdir(args.path)
    except PermissionError:
        args.screenshot = False
        logging.warning("Screenshots won't be saved! PermissionError")
    except:
        pass
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as webdriver
from time import sleep
from traceback import format_exc as fe

options = webdriver.ChromeOptions()
header_added, ht_tables = [], []


# Updates the html including the js fetched ones
def mod_chrome():
    mods = [
        False if args.display else "--headless",
        "--start-maximized",
        False if args.disable_incognito else "--incognito",
        "--disable-extensions",
        "--disable-plugin-discovery",
        "--profile-directory=default",
    ]
    for mod in mods:
        if mod:
            options.add_argument(mod)


mod_chrome()
options_passed = {"options": options}


# Handles chromedriver configurations
@error_handler()
def handle_driver():
    inf, ex = args.driver, "driver_executable_path"
    if inf:
        if not inf.lower() in ("load", "download"):
            from os import path

            if path.isfile(inf):
                options_passed[ex] = inf
                logging.info(f"Using chromedriver '{inf}'")
            else:
                exit_error(f"Chromedriver's path error '{inf}'")
        else:
            logging.info(f"Downoading Chromedriver for {platform}!")
            pass
    else:
        from .driver_patch import DownloadChromedriver as patcher
        from appdirs import AppDirs

        ex_path_name = patcher(
            AppDirs("bc03", "smartBetika").user_data_dir, logging
        ).main()
        if ex_path_name[0]:
            options_passed[ex] = ex_path_name[1]
            logging.debug("Using default chromedriver")
        else:
            logging.error("Failed to patch executable chromedriver")
            exit_error(ex_path_name[1])


try:
    handle_driver()
    driver = webdriver.Chrome(**options_passed)
except PermissionError:
    exit_error("PermissionError - Retry with sudo/admin privileges!")
except Exception as e:
    exit(logging.critical(e.args[1] if len(e.args) > 1 else str(e)))


def update_html():
    driver.execute_script("return document.body.innerHTML;")
    sleep(args.sleep)
    return driver.page_source


def html_style(title: str):
    ht_tables.append(1)
    total = len(ht_tables)
    if header_added:
        return f'<h4 class="hdr">{total}.{title}</h4><marquee id="time">Dated : {date()}</marquee>'
    header_added.append(True)
    rp = f"""
    <head>
    <title>SmartBetika predictions - Betika based betting tips</title>
    <meta name="description" content="Get accurate and reliable betting predictions for Betika platform. Our SmartBetika tips cover upcoming matches and jackpot games. Check our expert picks and increase your chances of winning.">
    <meta property="og:title" content="SmartBetika predictions - Betika based betting tips">
    <meta property="og:description" content="Get accurate and reliable betting predictions for Betika platform. Our SmartBetika tips cover upcoming matches and midweek jackpot games. Check our expert picks and increase your chances of winning.">
    <meta name="twitter:title" content="SmartBetika predictions - Betika based betting tips">
    <meta name="twitter:description" content="Get accurate and reliable betting predictions for Betika platform. Our SmartBetika tips cover upcoming matches and midweek jackpot games. Check our expert picks and increase your chances of winning.">
    <link rel="canonical" href="https://simatwa.github.io/smartBetika">
    <link rel="icon" type="image/x-icon" href="https://simatwa.github.io/smartBetika/favicon.ico"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <script type='text/javascript' src='//pl19107853.highrevenuegate.com/57/39/93/573993d8da28965f062ceca89805d006.js'></script>
    <style> .banner > a > img{{width:100%;max-height:200px;border-radius:25px;}}
    table{{margin-bottom:10px;}} body{{text-align:center;}}
    tr:nth-child(odd){{background-color:darkgray;color:black;}}
    tr:nth-child(even){{background-color:gray;color:black;}}
    table{{border-collapse:collapse;text-align:center;width:100%;}}
    .hdr{{list-style-type:decimal;}}
    tbody{{color:green;font-family:tahoma,sans-serif;}}
    h1{{color:darkblue;font-size:150%;text-decoration:underline;}}
    th{{background-color:darkgreen;;color:lime;}}
    h4{{text-decoration:underline;color:blue;font-weight:bold;font-family:Verdana,sans-serif;}}
    #time{{font-size:x-small;}}
    #time,h1,h4{{text-align:center;}}
    td{{border-left:1px solid rgb(42, 82, 65);border-right:1px solid green;}}
    tr{{border:none;}}</style></head>
    <h1>SmartBetika Predictions.</h1>
    <a href="#"><img style="display:none" src="https://visitor-badge.glitch.me/badge?page_id=Simatwa.smartBetika&left_color=red&right_color=lime&left_text=Punters" alt="Punters"/></a>
    <h4 class="hdr">{total}.{title}</h4>
    <marquee id="time">Dated : {date()}</marquee>"""
    return rp


# Handles interfacing data with users
class formatter:
    def __init__(self):
        self.verbose = args.verbose
        self.ad_tag = self.get_ads()

    def get_ads(self):
        try:
            from requests import get

            resp = get(github_adlink, timeout=20)
            if resp.ok:
                resp = resp.text
                ad_handler = resp
            else:
                resp = ""
            return resp
        except Exception as e:
            return ""

    def get_data(self, tbl: str) -> list:
        from tabulate import tabulate

        title, respo = [
            "Id",
            "Home",
            "Away",
            "H_odds",
            "X_odds",
            "A_odds",
            "Pick",
            "Choice",
            "Prob",
            "C_time",
        ], False
        title2 = (
            "Id",
            "League",
            "Date",
            "Time",
            "Home",
            "Away",
            "H_odds",
            "X_odds",
            "A_odds",
            "Pick",
            "Choice",
            "Prob",
        )
        if self.verbose:
            if tbl.lower() in ("sababisha", "midjp", "grandjp"):
                data = database.queryDb(
                    f"""SELECT {','.join(title)} FROM {tbl} ORDER BY Prob DESC"""
                )
                if type(data) is list:
                    respo = tabulate(data, headers=title, tablefmt=args.table)
                else:
                    logging.error(f"Zero data in {tbl}!")
            else:
                ht = False
                if args.table == "html":
                    title2 = (
                        "Id",
                        "League",
                        "Date",
                        "Time",
                        "Home",
                        "Away",
                        "H_odds",
                        "X_odds",
                        "A_odds",
                        "Pick",
                        "Choice",
                        "Prob",
                        "State",
                        "Category",
                        "Type",
                        "Markets",
                    )
                data = database.queryDb(
                    f"""SELECT {','.join(title2)} FROM {tbl} ORDER BY Prob DESC"""
                )
                if type(data) is list:
                    respo = tabulate(data, headers=title2, tablefmt=args.table)
                else:
                    logging.error(f"Zero data in {tbl}!")
        else:
            title = ["Id", "Home", "Away", "Pick", "Choice", "Prob"]
            if tbl.lower() in ("sababisha", "midjp", "grandjp"):
                data = database.queryDb(
                    f"""SELECT {','.join(title)} FROM {tbl} ORDER BY Prob DESC"""
                )
                if type(data) is list:
                    respo = tabulate(data, headers=title, tablefmt=args.table)
                else:
                    logging.error(f"Zero data in {tbl}!")
            else:
                data = database.queryDb(
                    f"""SELECT {','.join(title)} FROM {tbl} ORDER BY Prob DESC"""
                )
                if type(data) is list:
                    respo = tabulate(data, headers=title, tablefmt=args.table)
                else:
                    logging.error(f"Zero data in {tbl}!")
        if respo:
            if args.table == "html":
                respo = html_style(tbl.upper()) + respo
            else:
                pass
            if args.output:
                logging.info(f"Saving {tbl} matches in {args.output}")
                data43 = respo if args.table == "html" else tbl.upper() + "\n\n" + respo
                self.save_data(data43)
            else:
                logging.warning(f"Zero filename to save {tbl} predictions!")
            return respo
        else:
            return

    def save_data(self, data: str, ads: bool = True):
        try:
            if args.table == "html":
                from re import sub

                data = sub("\n", "", data) + f" {self.ad_tag if ads else '' }"
            with open(args.output, "a") as file:
                file.write("\n\n" + str(data))
        except Exception as e:
            logging.exception(e)


formatt = formatter()


# Main class betika website
class smartBetika:
    def __init__(self):
        # login setup
        driver.delete_all_cookies()
        if args.phone and args.password:
            logging.info(f"Login credentials {args.phone}:{args.password}")
            try:
                driver.get("https://www.betika.com/en-ke/login?next=%2F")
                update_html()
                driver.find_element(By.XPATH, '//input[@type="text"]').send_keys(
                    args.phone
                )
                driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(
                    args.password
                )
                screenshot(driver, args, "login")
                driver.find_element(
                    By.XPATH, '//div[@class="session__form__button__container"]'
                ).click()
            except Exception as e:
                err = str(e).split("\n")[0]
                try:
                    driver.quit()
                except:
                    pass
                exit_error(f"Failed to login - {err}")
        else:
            logging.info(
                f"Proceed without login Phone:{args.phone} Password:{args.password}"
            )
            driver.get("https://www.betika.com")

    def main(self):
        tables = []
        if args.normal or args.upcoming:
            from .normal_bets import normal_bets

            tbl_name = normal_bets(driver, args).main()
            if tbl_name:
                tables.append(tbl_name)
        if args.grandjp or args.midjp or args.sababisha:
            from .jackpots import category

            tbl_jackpots = category(driver, args).main()
            if tbl_jackpots:
                tables.extend(tbl_jackpots)
        logging.debug("Stopping webdriver!")
        try:
            driver.quit()
        except:
            pass
        from .predict_maker import predictor

        if tables:
            for data in tables:
                if args.predict:
                    logging.info(f"Making predictions on {data} match(es)!")
                    predictor(args, data).predictor()
                tbl = formatt.get_data(data)
                if tbl and not args.table in ("html"):
                    logging.info(f"Displaying {data} match-info.")
                    print(tbl)
        else:
            logging.info("Done hunting down matches!")


@error_handler()
def betika():
    def db_decide():
        if not args.noclear:
            remove_db()

    try:
        db_decide()
        smartBetika().main()
    except Exception as e:
        exit_error(logging.critical(str(e).split("\n")[0]))
        try:
            driver.quit()
        except:
            pass
    finally:
        if args.table == "html":
            formatt.save_data(
                """
        <div class="banner">
	<a href="https://oxygenblobsglass.com/bjih3uuhe?key=6b37fa529bff17e039a5697d32ef52f8">
    <img alt="banner" src="https://landings-cdn.adsterratech.com/referralBanners/png/468%20x%20120%20px.png"/>
    </a>
</div>
        """,
                False,
            )
        from platform import system as platform

        if all([args.view, platform() == "Linux", args.output]):
            from os import system

            logging.info(f"Opening {args.output} in Chrome.")
            system(f"google-chrome {args.output}")
        db_decide()
        exit_error(False)


if __name__ == "__main__":
    betika()
