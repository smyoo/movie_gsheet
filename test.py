import urllib.request as ul
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
pp = pprint.PrettyPrinter(indent=4)

############################################################################
# 영화관입장권통합전산망 오픈API 테스트
# http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do
############################################################################
key = "7d6adcbd79ec916a9d400b3f76f3ddfd"
prdtyear = "1958"
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={1}&itemPerPage=100&curPage=1".format(key, prdtyear)
#url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear=1956&prdtEndYear=1956&itemPerPage=100&curPage=2".format(key)
#url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear=1956&prdtEndYear=1956".format(key)

request = ul.Request(url)
response = ul.urlopen(request)
rescode = response.getcode()

if(rescode == 200):
    data = response.read()
    print(">>>> [Success] Result Code : {0}".format(rescode))
else:
    print(">>>> [Fail] Result Code : {0}".format(rescode))

result = json.loads(data)
#print(type(result))
#pp.pprint(result)
movie_list = result['movieListResult']['movieList']
print(len(movie_list))
print(">>> 총 영화수 : {0}".format(result['movieListResult']['totCnt']))
print('--------------------------\n')


############################################################################
# 구글시트 연동 테스트
############################################################################
scope = ['https://spreadsheets.google.com/feeds']
json_file_name = '/Users/smyoo/prj/smyoo_test.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file_name, scope)
gc = gspread.authorize(credentials)
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/163aCZbPpV04HZKyFlGVp9sd2ISm5jjn0MdVDEqtnRYg/edit#gid=0'

# 문서 불러오기
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet('영화')

# 읽기 - 셀
cell_data = worksheet.acell('B3').value
print(type(cell_data))
print(cell_data)
print('--------------------------\n')

# 읽기 - 범위
row_data = worksheet.row_values(3)
print(type(row_data))
print(row_data)
print('--------------------------\n')

# 읽기 - 범위
range_list = worksheet.range('A1:D3')
for cell in range_list:
    print(cell.value)

# 쓰기 - 셀
worksheet.update_acell('B1', 'b1 updated')

# 쓰기 - 행 추가
worksheet.append_row(['new1', 'new2', 'new3', 'new4'])

# 쓰기 - 특정 행 추가
worksheet.insert_row(['new1', 'new2', 'new3', 'new4'], 10)

# 쓰기 - 시트 크기 맞추기
worksheet.resize(10,4)

# 쓰기 - 삭제
worksheet.delete_rows(2, worksheet.row_count)
