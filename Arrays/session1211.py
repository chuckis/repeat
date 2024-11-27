# coding: utf-8
'123'<'13'
'!'<'?'
[1, 2, 3]<[2, 4]
s = 'abc12345@?)678'
digits=[]
for smb in s:
    if '0'<smb<'9':
        digits.append(smb)
print(digits)
