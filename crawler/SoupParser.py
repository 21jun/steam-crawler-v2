from selenium import webdriver
from bs4 import BeautifulSoup
from crawler.HeadlessChrome import HeadLessChrome
from datetime import datetime


def get_full_date():
    # return string type yyyy-mm-dd hh:mm:ss
    # for MySQL DATETIME column
    now = datetime.now()
    result = '%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    return result


def month_converter(month):
    return {
        'JAN': '1',
        'FEB': '2',
        'MAR': '3',
        'APR': '4',
        'MAY': '5',
        'JUN': '6',
        'JUL': '7',
        'AUG': '8',
        'SEP': '9',
        'OCT': '10',
        'NOV': '11',
        'DEC': '12'
    }[month.upper()]


class SoupParser:

    def _init(self):
        self.recent_review = {
            'count': 0,
            'evaluation': 'None',
            'positive_percentage': 0
        }
        self.all_review = {
            'count': 0,
            'evaluation': 'None',
            'positive_percentage': 0
        }
        self.developer = 'None'
        self.publisher = 'None'
        self.release_date = '0000-00-00'
        self.date = get_full_date()
        self.tags = ''

    def __init__(self):
        self._init()
        print('init complete')

    def clean_tags(self, tags):
        result = tags.replace('\t', '')
        result = result.replace('\r', '')
        result = result.replace('\n', ' ')
        result = result.replace('+', '')
        result = result.replace('  ', '')
        result = result.split(' ')
        result.remove('')

        # Free to Play Exception
        if 'Free' in result:
            result.remove('Free')
            result.remove('to')
            result.remove('Play')
            result.append('Free to Play')

        return result

    @staticmethod
    def clean_info(info):
        info = info.replace('\t', '').replace('\r', '').split('\n')
        while '' in info:
            info.remove('')
        return info

    @staticmethod
    def clean_number(num):
        num = num.replace('(', '')
        num = num.replace(')', '')
        num = num.replace(',', '')
        return num

    @staticmethod
    def clean_percentage(input_string):
        for i in range(len(input_string)):
            if input_string[i] == '%':
                percentage = input_string[i - 2:i]
                return percentage
        return 0

    @staticmethod
    def clean_date(release_date):
        release_date = release_date.replace(',', '')
        release_date = release_date.split(' ')
        # print(release_date)
        day = release_date[0]
        month = month_converter(release_date[1])
        year = release_date[2]
        date = '%s-%s-%s' % (year, month, day)
        return date

    def parse(self, soup):
        self._init()
        # tags
        tags = soup.select(
            '#game_highlights > div > div > div > div > div.glance_tags.popular_tags'
        )
        if tags:
            tags = self.clean_tags(tags[0].text)
            # tag 를 하나씩 분리해서 저장하려면 이 부분을 수정
            self.tags = ','.join(tags)
        # tag 가 없으면
        else:
            print('No tags')

        # info
        info = soup.select(
            '#game_highlights > div > div > div.glance_ctn_responsive_left > div '
        )

        if info:
            info = self.clean_info(info[0].text)
            for index, i in enumerate(info):
                if 'Recent Reviews' in i:
                    if self.clean_number(info[index + 2]).isdigit():
                        self.recent_review['evaluation'] = info[index + 1]
                        self.recent_review['count'] = self.clean_number(info[index + 2])
                        self.recent_review['positive_percentage'] = self.clean_percentage(info[index + 3])
                    else:
                        pass

                if 'All Reviews' in i:
                    if self.clean_number(info[index + 2]).isdigit():
                        self.all_review['evaluation'] = info[index + 1]
                        self.all_review['count'] = self.clean_number(info[index + 2])
                        self.all_review['positive_percentage'] = self.clean_percentage(info[index + 3])
                    else:
                        print('not enough all reviews')

                if 'Developer' in i:
                    self.developer = info[index + 1]

                if 'Publisher' in i:
                    self.publisher = info[index + 1]

                if 'Release Date' in i:
                    self.release_date = self.clean_date(info[index + 1])

        # info 정보가 없으면
        else:
            print('No info')
            pass

        result = {
            'recent_review': self.recent_review,
            'all_review': self.all_review,
            'developer': self.developer,
            'publisher': self.publisher,
            'tags': self.tags,
            'release_date': self.release_date,
            'date': self.date
        }

        return result
