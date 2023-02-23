#!/bin/env python3

import hmac
import hashlib
key='123456'
message='myname=zongqing&uid=1001&lstcmd=1&download=secret.txt'
mac = hmac.new(bytearray(key.encode('utf-8')),
                 msg=message.encode('utf-8', 'surrogateescape'),
                 digestmod=hashlib.sha256).hexdigest()
print(mac)