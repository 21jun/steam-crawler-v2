from selenium import webdriver
from bs4 import BeautifulSoup


class HeadLessChrome:

    def __init__(self, driver_path='C:/chromedriver_win32/chromedriver'):
        self.driver_path = driver_path
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        # options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(self.driver_path, chrome_options=options)
        self.driver.implicitly_wait(1)

    def _age_check_with_birthday(self):
        try:
            self.driver.find_element_by_name('ageYear')
            return True
        except:
            return False

    def _age_check(self):
        if 'agecheck' in self.driver.current_url:

            print('age check')
            if self._age_check_with_birthday():
                print("YEAR")
                el = self.driver.find_element_by_name('ageYear')
                for option in el.find_elements_by_tag_name('option'):
                    if option.text == '1980':
                        option.click()
                        break
                try:
                    self.driver.find_element_by_xpath('//*[@id="app_agegate"]/div[1]/div[4]/a[1]').click()
                    return
                except:
                    pass
                try:
                    self.driver.find_element_by_xpath('//*[@id="app_agegate"]/div[1]/div[3]/a[1]').click()
                    return
                except:
                    pass

            try:
                self.driver.find_element_by_xpath('//*[@id="app_agegate"]/div[1]/div[3]/a[1]').click()
                return
            except:
                pass

            try:
                self.driver.find_element_by_xpath('//*[@id="app_agegate"]/div[3]/a[1]/span').click()
                print("Just Click")
                return
            except:
                pass

    def get_soup(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(1)
        try:    self._age_check()
        except: return None
        # 페이지에 접속할 수 없으면 None 리턴
        if self.driver.current_url == 'https://store.steampowered.com/':
            print("Unable to access url", url)
            return None

        print(self.driver.current_url)

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def __del__(self):
        self.driver.quit()