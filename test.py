import urllib.request as ul
import json
import pprint

pp = pprint.PrettyPrinter(indent=4)
key = "7d6adcbd79ec916a9d400b3f76f3ddfd"
prdtyear = "1958"
url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key={0}&prdtStartYear={1}&prdtEndYear={1}&itemPerPage=100&curPage=1".format(key, prdtyear)
print(url)
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
pp.pprint(result)
movie_list = result['movieListResult']['movieList']
print(len(movie_list))
print(">>> 총 영화수 : {0}".format(result['movieListResult']['totCnt']))

