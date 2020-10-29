from SeleniumLibrary import SeleniumLibrary
from .keywords import BrowserKeywords
from .webelement.pcnwebelement_extended import *
import sys

__version__ = '1.0.0'


class Booking(SeleniumLibrary):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        SeleniumLibrary.__init__(self, 30)
        self.add_library_components(
            [
                BrowserKeywords(self),
            ]
        )
        ####################################################################################
        # Make sure pydevd installed: pip install pydevd
        # AND Uncomment following codes to enable debug mode
        # sys.path.append("pycharm-debug-py3k.egg")
        # import pydevd
        # pydevd.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
        ####################################################################################
