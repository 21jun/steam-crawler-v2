from crawler.HeadlessChrome import HeadLessChrome
from crawler.SoupParser import SoupParser
from database.DataBase import DataBase
import schedule
from datetime import datetime
from time import sleep


def routine():
    # url = ['https://store.steampowered.com/app/578080/PLAYERUNKNOWNS_BATTLEGROUNDS/',
    #        'https://store.steampowered.com/app/570/Dota_2/']
    HC = HeadLessChrome()
    SP = SoupParser()
    DB = DataBase()

    # TEST HERE
    # HC.get_soup('https://store.steampowered.com/app/671210/FINAL_FANTASY_XV_WINDOWS_EDITION_PLAYABLE_DEMO/')

    applist = DB.get_applist(table='watching_games')
    num_applist = len(applist)
    for idx, app in enumerate(applist):
        appid, name = app
        if idx%50 == 0:    HC.reconn()
        print('--------------', idx, '/', num_applist, '--------------')
        try:
            print(appid, name)
            url = 'https://store.steampowered.com/app/' + str(appid)
            soup = HC.get_soup(url)
            if soup is None:
                continue

            result = SP.parse(soup)
            result['appid'] = appid
            result['name'] = name
            try:
                DB.insert_data(result)
            except:
                # logging
                print('DB ERROR')
        except:
            print("skip ", appid, name, '\n')
            HC.reconn()
            continue
    
    
    print(datetime.now())

if __name__ == '__main__':

    schedule.every().day.at("00:00").do(routine)
    
    while True:
        schedule.run_pending()
        sleep(100)