from werkzeug.security import generate_password_hash, check_password_hash  
a=generate_password_hash('Bottleofwater43')
print(a)

s=check_password_hash('pbkdf2:sha256:260000$9u3IsA1rWdqXWDZF$8e48fcf0559107eb3cac5927985e3f38d9bd311186f21097ccd911a4354773af','Bottleofwater43')
print(s)