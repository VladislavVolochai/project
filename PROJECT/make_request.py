import requests
import inspect


G = ''
GROUP = ''
DATA = {}

#GROUP = 'group1'
GROUP = 'group2'
#GROUP = 'group3'

#G = '?rerergfпомидорCucumber=cat' # 天妈仙üöäß
G = '?карандш=pan'
#DATA = {'помидорa':'hello','üöäß':'天妈仙'}
DATA = {'text':'else','else':[1,2]}

#r = requests.get(f'http://127.0.0.1:8000/mock_service/get_mock/{GROUP}{G}', auth=('Volochai', '12345'))

r = requests.post(f'http://127.0.0.1:8000/mock_service/get_mock/{GROUP}', data=DATA)
#r = requests.get(f'http://127.0.0.1:8000/mock_service/get_requests/')

#r = requests.get(f'http://127.0.0.1:8000/mock_service/get_mock/r_s?googletranslatecom')
#r = requests.get('http://127.0.0.1:8000/mock_service/get_mock/r_s/https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.HttpResponse-HttpRequest')

#r = requests.get(f'https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.HttpResponse')

print(r)
print(r.text)
print(r.headers)


