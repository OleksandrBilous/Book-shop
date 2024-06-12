from flask import request
from datetime import datetime
import json
from functools import wraps

def log_request(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        # Log the request data
        data = {
            'path': request.path,
            'time': datetime.now().isoformat(),
            'user_agent': request.headers.get('User-Agent'),
            'ip': request.remote_addr
        }
        with open('moduls/requests_log.json', 'a') as file:
            file.write(json.dumps(data) + '\n')
        
        # Call the actual function
        return func(*args, **kwargs)
    return wrapped
