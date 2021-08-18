import requests
import inspect


G = ''
GROUP = ''

G = '?rerergfпомидорcucumber=cat' # 天妈仙üöäß
#GROUP = 'group1'

r = requests.get(f'http://127.0.0.1:8000/mock_service/get_mock/{GROUP}{G}', auth=('Volochai', '12345'))

#r = requests.post(f'http://127.0.0.1:8000/mock_service/get_mock/{GROUP}', data={'помидорa':'hello','üöäß':'天妈仙'})


#r = requests.get(f'http://127.0.0.1:8000/mock_service/get_requests/')

print(r)
print(r.text)
print(r.headers)


