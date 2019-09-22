import pymysql


class DataBase:

    def __init__(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', charset='utf8mb4',
                                  autocommit=True, port=3306)
        db = connect.cursor()
        self.db = db

    def db_reconnect(self):
        connect = pymysql.connect(host='localhost', user='root', password='1qazxc', db='oasis', charset='utf8mb4',
                                  autocommit=True, port=3306)
        db = connect.cursor()
        self.db = db

    def get_applist(self, table):
        """
        :param table: Which table you want to use
        :return: app data tuple (appid, name)
        """
        sql = '''SELECT appid, name FROM oasis.''' + str(table)
        self.db.execute(sql)
        apps = self.db.fetchall()
        return apps

    # TODO: 테이블 이름 지금은 app_info2임 나중에 필요하면 다른 테이블로 바꿔야함
    def insert_data(self, data):
        sql = '''INSERT INTO oasis.app_info2(appid, name, developer, publisher, release_date,
        recent_review_evaluation, recent_review_count, recent_review_positive_percentage,
        all_review_evaluation, all_review_count, all_review_positive_percentage, tags, date) 
        VALUES ("%d","%s","%s","%s","%s","%s","%d","%d","%s","%d","%d","%s","%s") '''
        self.db.execute(sql % (int(data['appid']), data['name'], data['developer'],
                               data['publisher'], data['release_date'],
                               data['recent_review']['evaluation'], int(data['recent_review']['count']),
                               int(data['recent_review']['positive_percentage']),
                               data['all_review']['evaluation'], int(data['all_review']['count']),
                               int(data['all_review']['positive_percentage']),
                               data['tags'], data['date']))


