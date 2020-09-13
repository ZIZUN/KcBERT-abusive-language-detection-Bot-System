# KcBERT기반 악성댓글탐지봇 시스템

일반적으로 사전학습 되어 공개된 한국어 BERT는 잘 정제된 여러 문서(e.g. 뉴스, 위키, 책)들을 이용하여 학습이 되어 문어체의 특성이 반영되어 있고 신조어, 구어체의 특성이 들어가 있지 않다고 볼 수 있다. KcBERT(Korean comments BERT)는 네이버 뉴스의 댓글로 학습되어 신조어, 구어체에 강인한 사전학습된 언어모델이라 할 수 있다. 따라서 악성댓글 탐지를 위해 KcBERT를 욕설, 혐오, 비난이 섞인 댓글과 그렇지 않은 댓글로 분류하는 다운스트림 태스크에 맞게 파인튜닝한다. 파인튜닝된 모델과 파라미터들을 이용하여 데이터베이스에 올라온 댓글들에 대해 악성여부를 탐지하는 최적화된 알고리즘을 구성해 안정된 봇서버를 만들어 시스템을 구축한다.

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
$ python manage.py migrate
$ python manage.py collectstatic
$ python manage.py createsuperuser
$ python manage.py runserver 127.0.0.1:8000
```
- http://127.0.0.1:8000 으로 접속가능하다.

## 봇서버 구동

- 설치된 폴더의 botserver 디렉토리로 이동

```bash
$ python BotServer.py
```



## 결과

|                     | Accuracy (%) |
| ----------------- | ------------ |
| KcBERT            | **80.93**    |
| KoBERT            | 77.68        |
| Attention Bi-LSTM | 73.79      |


## 참조
- [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/pdf/1810.04805)
- [Huggingface/Transformers](https://github.com/huggingface/transformers)
- [Beomi/KcBERT](https://github.com/Beomi/KcBERT)
- [kocohub/Korean-hate-speech-dataset](https://github.com/kocohub/korean-hate-speech)
- [SKTBrain/KoBERT](https://github.com/SKTBrain/KoBERT)
- [ZIZUN/Att Bi-LSTM](https://github.com/ZIZUN/Naver-news-article-classification-using-attention-based-bi-lstm-with-pytorch)
- [AmirAhrari/django-blog]

