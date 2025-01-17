fROM python:3.12.4


WORKDIR /


COPY ./requirements.txt /requirements.txt


RUN pip install --no-cache-dir --upgrade -r /requirements.txt


COPY . .


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" , "--workers", "7", "--limit-concurrency" , "500"]
#uvicorn app:app --timeout-keep-alive 5 --workers 4 --limit-concurrency 100