python -m pip install --user virtualenv
python -m venv env
cmd /k "cd /d env\Scripts & activate & cd /d .. & cd /d .. & pip install -r requirements.txt & python -m nltk.downloader all"
pause