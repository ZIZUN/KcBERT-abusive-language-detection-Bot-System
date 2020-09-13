# KcBERT기반 악성댓글탐지봇 시스템

## 요구사항

- MySQL Server 8.0 이상
  - instance 기본설정 >>  hostname: localhost  port:3306  username: root  password:root
  - schema name : django_web 으로 하여 등록
  - 위 설정들은 원한다면 코드수정 후 변경가능
- Linux or Windows
- Python 3.8.3 이상

```bash
$ git clone https://github.com/ZIZUN/KcBERT-abusive-language-detection-Bot-System.git && cd django-web
$ pip install -r requirements.txt
```

- django==2.2.1
- django-crispy-forms==1.7.2
- pillow==6.0.0
- djangorestframework==3.9.4
- torch==1.5.1
- transformers==3.0.1
- mysql-connector-python==8.0.21
- emoji==0.6.0
- soynlp==0.0.493

## 웹 서버 키는 방법

- 위에 설명된 환경이 모두 설정되었다는 가정하에, 설치된 폴더의 django_web 디렉토리로 이동
- 아래의 코드 실행
```bash
$ python manage.py runserver 127.0.0.1:8000
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py createsuperuser
$ python manage.py runserver
```
- http://127.0.0.1:8000 으로 접속가능하다.

## 봇서버 구동

- 설치된 폴더의 botserver 디렉토리로 이동

```bash
$ python BotServer.py
```



## Results

|                     | Accuracy (%) |
| ----------------- | ------------ |
| KcBERT            | **80.93**    |
| KoBERT            | 77.68        |
| Attention Bi-LSTM | 73.79      |


## References
- [KcBERT](https://github.com/Beomi/KcBERT)
- [KoBERT](https://github.com/SKTBrain/KoBERT)
- [Att Bi-LSTM](https://github.com/ZIZUN/Naver-news-article-classification-using-attention-based-bi-lstm-with-pytorch)
- [Huggingface Transformers](https://github.com/huggingface/transformers)
- [Korean-hate-speech-dataset](https://github.com/kocohub/korean-hate-speech)
- [django-blog](https://github.com/AmirAhrari/django-blog)