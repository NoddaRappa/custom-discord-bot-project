from fileinput import filename
import json
import os
import dotenv

dotenv.load_dotenv()

file_name = 'headcount.json'

async def hurt_count():
    if os.path.exists(file_name):
        with open(file_name, 'r+') as f:
            count = json.load(f)
            count += 1
            f.seek(0)
            json.dump(count, f)
            f.truncate()
    else:
        with open(file_name, 'w') as f:
            json.dump(1, f)
