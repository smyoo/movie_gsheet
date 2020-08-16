import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import pprint
pp = pprint.PrettyPrinter(indent=4)

# 입력값
prdtyear_start = "1957" # 제작년도 시작
prdtyear_end = "1968" # 제작년도 끝
sheet_name = "영화정보(kobis)"

# Google Sheet API
scope = ['https://spreadsheets.google.com/feeds']
json_file_name = '/Users/smyoo/prj/smyoo_test.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/163aCZbPpV04HZKyFlGVp9sd2ISm5jjn0MdVDEqtnRYg/edit#gid=0' # 내꺼
#spreadsheet_url = 'https://docs.google.com/spreadsheets/d/11zMaVONUI8NLGAoR-pVdhw_nSOp3uAEdQVkLJPqayEY/edit?ts=5f379fb2#gid=0' # 승진이꺼
############################################################################

############################################################################

# 영화정보 가져오는 함수
def get_movie_info(prdtyear_start, prdthyear_end, list_cnt, start_cnt):
    key = "7d6adcbd79ec916a9d400b3f76f3ddfd"
    url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={0}&createDts={1}&createDte={2}&listCount={3}&startCount={4}".format(key, prdtyear_start, prdtyear_end, list_cnt, start_cnt)
    request = ul.Request(url)
    response = ul.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        data = response.read()
        print(">>>> [Success] Result Code : {0}".format(rescode))
    else:
        print(">>>> [Fail] Result Code : {0}".format(rescode))
    result = json.loads(data)
    movie_list = result['movieListResult']['movieList']
    tot_cnt = result['movieListResult']['totCnt']
    return [movie_list, tot_cnt]

a = get_movie_info 