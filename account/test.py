from urllib.parse import quote
from urllib.request import Request, urlopen
import ssl
import json

kor_url = quote('서울특별시 서초구 서초2동 서초대로74길 14')
API_key = "AIzaSyCZLUWkw3BFjJ6WU05hgWwqfEJWv1d5Mkc"

url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+ kor_url +'&key=' + API_key + '&language=ko&region=KR'
req = Request(url, headers={ 'X-Mashape-Key': API_key })

print(req.data)