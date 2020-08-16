import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql
import time
import configparser
import pprint
pp = pprint.PrettyPrinter(indent=4)

config = configparser.ConfigParser()
config.read('../config.ini')

# 영화정보 가져오는 함수

def request_data(url):
    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        data = response.read()
        print(">>> [Success] Result Code : {0}".format(rescode))
    else:
        print(">>> [Fail] Result Code : {0}".format(rescode))
    return json.loads(data)

# 영화정보가져오기 - 영화관입장권통합전산망 오픈API
def get_movie_info_kobis(prdtyear_start, prdthyear_end, items, page):
    key = config['api_key']['kobis']
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={2}&itemPerPage={3}&curPage={4}".format(key, prdtyear_start, prdthyear_end, items, page)
    data = request_data(url)
    movie_list = data['movieListResult']['movieList']
    tot_cnt = data['movieListResult']['totCnt']
    return [movie_list, tot_cnt]


def connect_googlesheet(spreadsheet_url, sheet_name):
    scope = ['https://spreadsheets.google.com/feeds']
    json_file_name = '/Users/smyoo/prj/smyoo_test.json'
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
    gc = gspread.authorize(credentials)
    doc = gc.open_by_url(spreadsheet_url)
    worksheet = doc.worksheet(sheet_name)
    return worksheet

# 테스트필요..
def _save_to_mysql(data):
    c = config['mysql']
    db = pymysql.connect(
            user=c['user'], 
            passwd=c['pwd'], 
            host=c['host'], 
            port=int(c['port']),
            db=c['db'], 
            charset='utf8'
        )
    cursor = db.cursor()
    cursor.execute("select * from movie.aaa")
    r = cursor.fetchall()
    pp.pprint(r)

def _conn_mysql():
    c = config['mysql']
    conn = pymysql.connect(
            user=c['user'], 
            passwd=c['pwd'], 
            host=c['host'], 
            port=int(c['port']),
            db=c['db'], 
            charset='utf8'
        )
    return conn

def init_table(table_name):
    conn = _conn_mysql()
    cur = conn.cursor()
    cur.execute("truncate table {0};".format(table_name))
    conn.close()

def insert_into_table(sql_list):
    conn = _conn_mysql()
    cur = conn.cursor()
    for s in sql_list:
        cur.execute(s)
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    data = "aaa"
    save_to_mysql(data)