import zipfile
from datetime import datetime
from pathlib import Path

current_time = datetime.now()

with zipfile.ZipFile('Project Zip Files/project_' + current_time.strftime("%H-%M-%S") + '.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file in Path('.').iterdir():
        if file.is_file():
            print("Checking ", file.name)
            if ('.py' in file.name) and file.name != 'zip.py':
                zipf.write(file)
            
