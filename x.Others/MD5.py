import hashlib

hl = hashlib.md5()

mobile = "185016678791"

hl.update(mobile.encode(encoding='utf-8'))

print('Before MD5 Encryption:  ' + mobile)
print('After MD5 Encryption:   ' + hl.hexdigest())
