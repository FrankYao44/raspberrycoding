import re
s=r'^(www\.|WWW)(\d{6,11})\@(qq|QQ)\.com$'
m=re.match(s,'www.2544762897@QQ.com')
for i in range(4):
    print(m.group(i))
s=r'^\<([0-9a-zA-Z\_\.]{5,15})\>([a-zA-z]{2,10})\@([0-9a-zA-Z]{2,10})\.(com|org)$'
semail=re.compile(s)
s='<mysql>linus@163.com'
result=semail.match(s)
print(result.group(2))

    
