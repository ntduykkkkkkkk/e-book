from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from SeleniumLibrary.keywords import WaitingKeywords
from robot.libraries.BuiltIn import BuiltIn
import os, platform

__version__ = '1.0.0'


class BrowserKeywords(LibraryComponent):

    WINDOWS_FIREFOX_DRIVER_PATH = r'\Drivers\geckodriver.exe'
    WINDOWS_CHROME_DRIVER_PATH = r'\Drivers\chromedriver.exe'
    WINDOWS_EDGE_DRIVER_PATH = r'\Drivers\MicrosoftWebDriver.exe'
    LINUX_FIREFOX_DRIVER_PATH = r'\Drivers\geckodriver'
    LINUX_CHROME_DRIVER_PATH = r'\Drivers\chromedriver'
    FIREFOX_DOWNLOAD_LOCATION = r'\Results\Exported\Firefox_exported'
    CHROME_DOWNLOAD_LOCATION = r'\Results\Exported\Chrome_exported'

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.waiting_management = WaitingKeywords(ctx)
        self.browser_management = BrowserManagementKeywords(ctx)

    @keyword
    def get_current_os(self):
        return platform.system()

    @keyword
    def format_os_path(self, path):
        # /: Linux
        # \: Windows
        return path.replace('\\', '/') if os.sep == '/' else path.replace('/', '\\')

    @keyword
    def get_current_path_of_project(self):
        current_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.dirname(os.path.dirname(os.path.join("..", current_path)))

    @keyword
    def enable_download_in_headless_chrome(self, driver, download_dir):
        # add missing support for chrome "send_command"  to selenium webdriver
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        driver.execute("send_command", params)

    @keyword
    def open_my_browser(self, setup):
        curr_path = self.get_current_path_of_project()
        if setup.get('setup').get('browser').lower() == 'firefox':
            options = FirefoxOptions()
            if setup.get('setup').get('headless').lower() == 'true':
                options.headless = True
            else:
                options.headless = False
            options.set_preference('pdfjs.previousHandler.alwaysAskBeforeHandling', False)
            options.set_preference('browser.download.folderList', 2)
            options.set_preference('browser.download.dir', curr_path + self.format_os_path(self.FIREFOX_DOWNLOAD_LOCATION))
            options.set_preference('browser.download.panel.shown', False)
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/csv," + "text/csv," +
                                   "application/x-msexcel,application/excel," +
                                   "application/vnd.openxmlformats-officedocument.wordprocessingml.document," +
                                   "application/x-excel,application/vnd.ms-excel" +
                                   "application / xml")
            if self.get_current_os().lower() == 'windows':
                driver = webdriver.Firefox(capabilities=None, options=options, executable_path=curr_path + self.format_os_path(self.WINDOWS_FIREFOX_DRIVER_PATH))
            else:
                driver = webdriver.Firefox(capabilities=None, options=options, executable_path=curr_path + self.format_os_path(self.LINUX_FIREFOX_DRIVER_PATH))
            driver.maximize_window()
        else:
            options = ChromeOptions()
            if setup.get('setup').get('headless').lower() == 'true':
                options.add_argument("headless")
            else:
                options.add_argument("--start-maximized")
            prefs = {"profile.default_content_settings.popups": 0,
                     "download.default_directory": curr_path + self.format_os_path(self.CHROME_DOWNLOAD_LOCATION),
                     "directory_upgrade": True}
            options.add_experimental_option("prefs", prefs)
            if self.get_current_os().lower() == 'windows':
                driver = webdriver.Chrome(chrome_options=options,
                                          executable_path=curr_path + self.format_os_path(self.WINDOWS_CHROME_DRIVER_PATH))
            else:
                driver = webdriver.Chrome(chrome_options=options, executable_path=curr_path + self.format_os_path(self.LINUX_CHROME_DRIVER_PATH))
            if setup.get('setup').get('headless') == 'True':
                self.enable_download_in_headless_chrome(driver,
                                                        curr_path + self.format_os_path(self.CHROME_DOWNLOAD_LOCATION))
        driver.get(setup.get(BuiltIn().get_variable_value("${RESOURCE}")).get('url'))
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return self.ctx.register_driver(driver, None)

