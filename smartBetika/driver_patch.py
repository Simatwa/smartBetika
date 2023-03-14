"""
Copyright 2023 bc03

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without limitation in the rights to use, copy, modify, merge, publish, and/ or distribute copies of the Software in an educational or personal context, subject to the following conditions: 

- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

Permission is granted to sell and/ or distribute copies of the Software in a commercial context, subject to the following conditions:

- Substantial changes: adding, removing, or modifying large parts, shall be developed in the Software. Reorganizing logic in the software does not warrant a substantial change. 

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
import requests
import platform
import os
import json
from sys import exit


class DownloadChromedriver:
    def __init__(self, user_data_dir: str, logging: object):
        self.logging = logging
        self.exit = lambda msg: exit(logging.critical(msg))
        if not os.path.isdir(user_data_dir):
            try:
                os.makedirs(user_data_dir)
                logging.debug(f"Directory created - {user_data_dir}")
            except Exception as e:
                self.exit(f"Error while creating data dir : {e}")
        self.platform = platform.system()
        self.chrome_version = self.get_chrome_version()
        self.url = self.get_download_url()
        self.path = user_data_dir

    def get_chrome_version(self):
        """Get the chrome version"""
        try:
            if platform.system() == "Windows":
                self.platform = "win32"
                command = 'reg query "HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon" /v version'
            elif platform.system() == "Linux":
                self.platform = "linux64"
                command = "google-chrome --version"
            elif platform.system() == "Darwin":
                self.platform = "mac64"
                command = "defaults read /Applications/Google\ Chrome.app/Contents/Info.plist CFBundleShortVersionString"
            else:
                exit("Unsupported system " + platform)
            chrome_version = os.popen(command).read().split()[-1]
            return chrome_version
        except Exception as e:
            self.exit(f"Error occured while identifying chrome version - {e}")

    def get_download_url(self):
        """Get the download url"""
        self.logging.info(
            "Getting chromedriver for browser version - " + self.chrome_version
        )
        url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{}".format(
            self.chrome_version[:3]
        )
        response = requests.get(url)
        if response.status_code == 200:
            self.chrome_version = response.text
            download_url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_{}.zip".format(
                self.chrome_version, self.platform
            )
            return download_url
        else:
            self.exit(f"Chromedriver not found for - {self.chrome_version}")

    def download_chromedriver(self):
        """Download the chromedriver"""
        self.logging.info(f"Downloading Chromedriver - v{self.chrome_version}")
        response = requests.get(self.url)
        if response.status_code == 200:
            try:
                with open(os.path.join(self.path, "chromedriver.zip"), "wb") as f:
                    f.write(response.content)
                    self.logging.info("Chromedriver downloaded successfully")
            except Exception as e:
                self.exit(f"Error occured while saving chromedriver - {e}")
        else:
            self.exit(
                f"Error while downloading chromedriver - response code {response.status_code}"
            )

    def unzip_contents(self):
        """Unzipping contents"""
        try:
            from zipfile import ZipFile

            with ZipFile(os.path.join(self.path, "chromedriver.zip")) as zipped:
                zipped.extractall(self.path)
        except Exception as e:
            self.exit(f"Error occured while unzipping chromedriver.zip - {e}")

    def make_driver_executable(self) -> tuple:
        """Makes driver executable by system"""
        from stat import S_IRWXU as add_exc

        try:
            for file in os.listdir(self.path):
                if file.lower().startswith("chromedriver") and not file.endswith("zip"):
                    driver_path = os.path.join(self.path, file)
                    os.chmod(driver_path, add_exc)
                    return (True, driver_path)
        except Exception as e:
            self.exit(f"Error occured while adding exec permission to driver - {e}")
            return (False, str(e))

    def verify_version(self, cached_path: str) -> tuple:
        """Ensures current driver version matches the Browser"""
        if os.path.isfile(cached_path):
            with open(cached_path) as file:
                contents = json.loads(file.read())
                try:
                    return (True, contents[self.chrome_version])
                except KeyError:
                    return [False] * 2
        else:
            return [False] * 2

    def main(self):
        """Main method"""
        cached_path = os.path.join(self.path, "driver_info.json")
        check_out = self.verify_version(cached_path)

        def handle_driver():
            self.unzip_contents()
            return self.make_driver_executable()

        if check_out[0]:
            handle_driver()
            return check_out
        else:
            self.download_chromedriver()
            resp = handle_driver()
            if resp[0]:
                with open(cached_path, "w") as file:
                    file.write(json.dumps({self.chrome_version: resp[1]}, indent=4))
            return resp


if __name__ == "__main__":
    import logging

    start = DownloadChromedriver(os.getcwd(), logging)
    print(start.main())
