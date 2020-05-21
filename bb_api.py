import json
import urllib.parse
from pprint import pprint

from lxml import etree
import requests


class BlackBoardAPI:
    def __init__(self, student_id, password):
        self.session = BlackBoardAPI.connect_to_black_board(student_id, password)

    @classmethod
    def connect_to_black_board(cls, student_id, password):
        consent_cookie = {
            "domain": "calbaptist.blackboard.com",
            "name": "COOKIE_CONSENT_ACCEPTED",
            "path": "/",
            "secure": "false",
            "value": "true"
        }
        session = requests.Session()
        session.cookies.set(**consent_cookie)
        r = session.get("https://calbaptist.blackboard.com/")
        html_tree = etree.HTML(r.text)
        elements = html_tree.xpath('/html/body/div[1]/div/div/div[7]/section/ul[1]/li[2]/div/form/input[3]')
        security_val = elements[0].get('value')
        url = "https://calbaptist.blackboard.com/webapps/login/"
        payload = 'action=login&blackboard.platform.security.NonceUtil.nonce={security_val}&login=Login&new_loc=&password={password_url_encoded}&user_id={student_id}'.format(
            security_val=security_val, student_id=student_id, password_url_encoded=urllib.parse.quote(password))
        headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Sec-Fetch-Dest': 'document',
            'Origin': 'https://calbaptist.blackboard.com',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
        }
        session.request("POST", url, headers=headers, data=payload)
        return session

    def get_all_assignments(self):
        url = "https://calbaptist.blackboard.com/webapps/calendar/calendarData/selectedCalendarEvents?start=1587884400000&end=1591513200000&course_id=&mode=personal"
        headers = {
            'Host': 'calbaptist.blackboard.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://calbaptist.blackboard.com/webapps/calendar/viewPersonal',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        response = self.session.get(url, headers=headers)

        return pprint(json.loads(response.text))

    def get_classes(self):
        url = "https://calbaptist.blackboard.com/webapps/calendar/calendarData/calendars?mode=personal&course_id=&_=1589778737365"
        headers = {
            'Host': 'calbaptist.blackboard.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://calbaptist.blackboard.com/webapps/calendar/viewMyBb?globalNavigation=false',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'text/plain',
        }
        response = self.session.get(url, headers=headers)
        response = json.loads(response.text)
        class_list = list()
        for calendar in response.get('calendars'):
            if calendar.get('id') != 'INSTITUTION' and calendar.get('id') != 'PERSONAL' and calendar.get(
                    'id') != 'ONG-COE':
                class_list.append(calendar.get('id'))

        return class_list

    def get_assignments_for_class(self, class_name):
        url = "https://calbaptist.blackboard.com/webapps/calendar/calendarData/events?start=1587884400000&end=1591513200000&course_id=&calendarIds={0}".format(
            class_name)
        headers = {
            'Host': 'calbaptist.blackboard.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Referer': 'https://calbaptist.blackboard.com/webapps/calendar/viewPersonal',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        response = self.session.get(url, headers=headers)

        return json.loads(response.text)


test = BlackBoardAPI(student_id=644941, password='Manafest1!')

for class_name in test.get_classes():
    pprint(class_name)
    pprint(test.get_assignments_for_class(class_name))
