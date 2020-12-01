import bcrypt

password = 'bravery cookie'.encode('utf-8')
salt = bcrypt.gensalt()
second_salt = bcrypt.gensalt()

digest1 = bcrypt.hashpw(password, salt)
digest2 = bcrypt.hashpw(password, second_salt)

print(digest1.decode('utf-8'))
print(digest2)
if bcrypt.checkpw(password, digest1):
	print('Auth passed')
else:
	print('Fail..')

if bcrypt.checkpw(password, digest2):
	print('Auth passed')
else:
	print('Fail..')