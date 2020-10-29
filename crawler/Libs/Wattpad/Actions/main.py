import json
import requests
import urllib3
from SeleniumLibrary.base import keyword, LibraryComponent
from robot.libraries.BuiltIn import BuiltIn

from Libs.Share.Actions import Main as CommonFunction

__version__ = '1.0.0'


class Main(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def get_data(self):
        return CommonFunction.get_setup_data(self)

    @keyword
    def parse_url(self):
        return self.get_data().get(BuiltIn().get_variable_value("${RESOURCE}")).get('url')

    @keyword
    def query_by_keyword(self, query_string):
        story_id = []
        offset = 15
        headers = {
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
        }
        urllib3.disable_warnings()
        for i in range(100):
            response = requests.get(self.parse_url() + "/v4/search/stories?query="+query_string+"&fields=stories%28id%29&filter=complete&limit=15&offset="+str(offset),
                                headers=headers, verify=False)
            offset += 15
            temp = json.loads(response.content.decode("utf-8"))
            if len(temp) == 0:
                break
            for story in temp.get('stories'):
                story_id.append(story.get("id"))
        result = list(set(story_id))
        print(result)
        print(len(result))
        with open('data.json', 'w') as outfile:
            json.dump(result, outfile)
        return story_id

    @keyword
    def query_story_by_id(self, id):
        headers = {
            "Content-Type": "application/json",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }
        urllib3.disable_warnings()
        response = requests.get(self.parse_url() + "v3/stories/" + id, headers=headers, verify=False)
        print(response)
        return json.loads(response.content.decode("utf-8"))