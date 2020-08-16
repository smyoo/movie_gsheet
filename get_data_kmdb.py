import movie_data as mv

# 입력값
prdtyear_start = "1957" # 제작년도 시작
prdtyear_end = "1968" # 제작년도 끝
sheet_name = "영화정보(kobis)"
list_cnt = 0
start_cnt = 0
url = "http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&ServiceKey={0}&createDts={1}&createDte={2}&listCount={3}&startCount={4}".format(key, prdtyear_start, prdtyear_end, list_cnt, start_cnt)
