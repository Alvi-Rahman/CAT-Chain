import requests
import json
import time
import random

id = ['15ab8357abeb6eacf1b591a1b5b1aedd','80cf219b4993391f6a6a0c08096c5ecb','8d46e96b1dae34c8932f46203e4f96ed','814e909f65f1d912cdb7cc3983b94329','9485b1ffdcd57a1e780d12cb2fbf0e49','79195dad1f933b67b79b19c194f9701a']

c = 0
while c<10:
    r1 = 0
    JSON = {
            "sender": id[random.randint(0, 5)],
            "receiver": str(random.getrandbits(128)),
            "amount": str(random.getrandbits(128))[:15],
            "category": 0
            }
    
    try:
            URL = "http://localhost:5001/add_transaction"
            r1 = requests.post(URL, data=json.dumps(JSON))
    except:
            pass
    
    print(r1)

    time.sleep(random.randrange(3))
    c=c+1
