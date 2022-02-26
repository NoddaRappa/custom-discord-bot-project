import json
import os
import dotenv

dotenv.load_dotenv()
PATH = os.getenv("PATH")

save_path = PATH
file_name = 'headcount.json'
directory = os.path.join(save_path, file_name)


async def hurt_count():
    file = open(directory, 'r+')
    count = json.load(file)
    count += 1
    file.seek(0)
    json.dump(count, file)
    file.truncate()
    file.close()
