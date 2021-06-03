from cryptography.fernet import Fernet

###암호화 공부 파일######################################
##암복호화에 사용할 대칭키 생성
key = Fernet.generate_key()
print(f'대칭키:{key}')

##암호화
key = b'hPDO4gtOsDV1dHTn9CJ4a8Qyoa2a-ukIwkW3j3FgPyU='

fernet = Fernet(key)
encrypt_str = fernet.encrypt("01066278667".encode())

print("암호화된 문자열: ", encrypt_str)

##복호화
key = b'hPDO4gtOsDV1dHTn9CJ4a8Qyoa2a-ukIwkW3j3FgPyU='
encrypt_str = b'gAAAAABgpxR3ui6lVHTy-0BgDCk3GHX6xzy1Herw-9aV3kj70hcklXGHSVqpHX8kMHYBaOEd3S6p-2BTIxhzysqF2A-N2JHLwQ=='
fernet = Fernet(key)
decrypt_str = fernet.decrypt(encrypt_str)

print("복호화된 문자열: ", decrypt_str)