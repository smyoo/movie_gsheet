import movie_data as mv
import math


############################################################################
# 영화관입장권통합전산망 오픈API 테스트
# http://www.kobis.or.kr/kobisopenapi/homepg/main/main.do
############################################################################

# 입력값
prdtyear_start = "1940" # 제작년도 시작
prdtyear_end = "1968" # 제작년도 끝

# 구글시트정보
spreadsheet_url = mv.config['googlesheet']['url_smyoo']
sheet_name = "영화정보(kobis)"

# 조건을 만족하는 총 영화 건수를 가져옴
# api 호출건당 최대 100건만 가능하므로 page수를 파악하여 호출건수 제어하기 위함
a = mv.get_movie_info_kobis(prdtyear_start, prdtyear_end, 1, 1)
tot_cnt = a[1]
print(">>> 총 영화수 : {0}".format(tot_cnt))
print('--------------------------\n')

# 조건을 만족하는 전체 영화데이터 가져옴.
# 한번에 100건씩 pages 만큼 호출
items=100 # 페이지당 데이터 수
pages=math.ceil(tot_cnt/items)
column_cnt = 14 # 구글시트 데이터 항목 컬럼 수
tot_items = 0
# 구글시트 초기화
worksheet = mv.connect_googlesheet(spreadsheet_url, sheet_name)
# DB 초기화
mv.init_table('movie_info_kobis')
if worksheet.row_count > 3: worksheet.delete_rows(4, worksheet.row_count)
for page in range(1, pages+1):
    print('>>> [INFO] Get Movie Info (page:{0})'.format(page))
    r = mv.get_movie_info_kobis(prdtyear_start, prdtyear_end, items, page)
    movie_list = []
    sql_list = []
    movie_dict = r[0]
    for m in movie_dict:
        tot_items = tot_items + 1
        movie_list.append(
            [
                m['movieCd'],
                m['movieNm'],
                m['movieNmEn'],
                m['prdtYear'],
                m['openDt'],
                m['typeNm'],
                m['prdtStatNm'],
                m['nationAlt'],
                m['genreAlt'],
                m['repNationNm'],
                m['repGenreNm'],
                '' if not m['directors'] else m['directors'][0]['peopleNm'],
                '' if not m['companys'] else m['companys'][0]['companyCd'],
                '' if not m['companys'] else m['companys'][0]['companyNm'],
            ]
        )
        # DB입력을 위한 SQL생성
        columns = []
        values = []
        for d in m.keys():
            if not (type(m[d]) is list or type(m[d]) is dict):
                columns.append(d)
                values.append(m[d].replace("'","\\'"))
        sql = "insert into movie_info_kobis ({0}) values ('{1}');".format(','.join(columns), "','".join(values))
        sql_list.append(sql)
    
    # 구글시트에 저장
    worksheet.append_rows(movie_list)
    # DB에 저장ㅋㅁㄴㅋ
    mv.insert_into_table(sql_list)
    print(">>> [INFO] Upload Completed ... {0}/{1}\n".format(tot_items, tot_cnt))


""" 
    (참고) 컬랙션형 데이터가 들어가 있는 형태.. 문서상에는 문자열이라 되어 있음
    'companys': [{'companyCd': '20060351', 'companyNm': '서울영화사'}],
    'directors': [{'peopleNm': '신상옥'}],
"""

print(">>> Completed...")

