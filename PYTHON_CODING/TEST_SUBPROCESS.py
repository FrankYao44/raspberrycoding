import subprocess
print('$ ls')
r=subprocess.call(['python3','/home/pi/test.py' ])
print('exit code ', r)
print('$ cd test')
p=subprocess.Popen('python3 ',stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
output,err= p.communicate(b'print(\"hello\")')
print(output.decode('utf-8'))
print('Exit code:', p.returncode)



