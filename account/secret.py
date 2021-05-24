#암호화 대칭키는 6개월에 한번씩 바꿔준다!

from cryptography.fernet import Fernet

###암호화 공부 파일######################################
##암복호화에 사용할 대칭키 생성
# key = Fernet.generate_key()
# print(f'대칭키:{key}')

##암호화
key = b'hPDO4gtOsDV1dHTn9CJ4a8Qyoa2a-ukIwkW3j3FgPyU='
fernet = Fernet(key)