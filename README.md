![dj_logo](https://i.pinimg.com/originals/73/b8/f2/73b8f2cac59ab9fb4078241808fbb507.jpg)
## Introduction

This package helps to integrate [payme.uz](http://payme.uz) and your application is built on [django](https://www.djangoproject.com/).

### Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install django
pip install djangorestframework
pip install requests

          or  

pip install -r requirements.txt
```

# supported versions
python 3.7 +
django 2 +
djangorestframework 3.7 +
````


## Usage

```python
# settings.py

INSTALLED_APPS = [
     ... 
    'rest_framework',
     ...
]

PAYME_SETTINGS = {
    'DEBUG':True,   #True - test mode, False - production mode
    'ID':'Your KASSA_ID',  
    'SECRET_KEY':'Your TEST KEY OR PRODUCTIN KEY',
    'ACCOUNTS':{
        'KEY_1':'order_id',
        'KEY_2':'',
    }
}


## Get started
```bash
python manage.py migrate
python manage.py runserver
```

**Let's try the first create card request:**
```
POST HTTP/1.1
Host: http://127.0.0.1:8000/paymeuz/card-create/
{
    "id": 123,
    "params": {
        "card": { "number": "4444444444444444", "expire": "0420"},
        "amount": 200000, 
        "save": true
    }
}
```

**Response:**
```
{
    "jsonrpc": "2.0",
    "result": {
        "sent": true,
        "phone": "99890*****66",
        "wait": 60000
    },
    "token": "5f460c3d4e6d0841074e7457_YgQMNCttjxKTMKcfN0GPSaaKyV4zPnJqRP4iezHfBGJBpfAyjJf0onx5QXIkmChPDdGJrUpXj2EqWFnTicR4W7p1nXFVvKPegirWSYObyNvrcz18IQbbAVXPTOq1cFQQVrfN1tBM3XdQChu3yr1kTokO7vmeGyCyPZzdO0G4SJeKIwsJiJJk8jvGYpYk0csZh0OhTd01sXIu1qQ4H79qN5vIi5U9rpQcwWra9ueCgJqgU4XgWE2OaGjY4G3qpDHr7ezOUg4Ud3M7S8A1CnsubOD0rhUnOdwWhIU6wuNVJX6xNYD5vjRd4W1StByQeEgIFWHTe4md6nCpSKANPUCH7xnfa3UUu2gz9WJ0PDmOoPwdVo53v9OpQ23kta0sUzMJgSJt"
}
```


**The second verify request:**
```
POST HTTP/1.1
Host: http://127.0.0.1:8000/paymeuz/card-verify/
{
    "id": 123,
    "params": {
        "token": "5f460c3d4e6d0841074e7457_YgQMNCttjxKTMKcfN0GPSaaKyV4zPnJqRP4iezHfBGJBpfAyjJf0onx5QXIkmChPDdGJrUpXj2EqWFnTicR4W7p1nXFVvKPegirWSYObyNvrcz18IQbbAVXPTOq1cFQQVrfN1tBM3XdQChu3yr1kTokO7vmeGyCyPZzdO0G4SJeKIwsJiJJk8jvGYpYk0csZh0OhTd01sXIu1qQ4H79qN5vIi5U9rpQcwWra9ueCgJqgU4XgWE2OaGjY4G3qpDHr7ezOUg4Ud3M7S8A1CnsubOD0rhUnOdwWhIU6wuNVJX6xNYD5vjRd4W1StByQeEgIFWHTe4md6nCpSKANPUCH7xnfa3UUu2gz9WJ0PDmOoPwdVo53v9OpQ23kta0sUzMJgSJt",
        "code": "213131"
    }
}
```

**Response:**
```
{
    "jsonrpc": "2.0",
    "id": 123,
    "result": {
        "card": {
            "number": "860006******6311",
            "expire": "03/99",
            "token": "5f460c3d4e6d0841074e7457_YgQMNCttjxKTMKcfN0GPSaaKyV4zPnJqRP4iezHfBGJBpfAyjJf0onx5QXIkmChPDdGJrUpXj2EqWFnTicR4W7p1nXFVvKPegirWSYObyNvrcz18IQbbAVXPTOq1cFQQVrfN1tBM3XdQChu3yr1kTokO7vmeGyCyPZzdO0G4SJeKIwsJiJJk8jvGYpYk0csZh0OhTd01sXIu1qQ4H79qN5vIi5U9rpQcwWra9ueCgJqgU4XgWE2OaGjY4G3qpDHr7ezOUg4Ud3M7S8A1CnsubOD0rhUnOdwWhIU6wuNVJX6xNYD5vjRd4W1StByQeEgIFWHTe4md6nCpSKANPUCH7xnfa3UUu2gz9WJ0PDmOoPwdVo53v9OpQ23kta0sUzMJgSJt",
            "recurrent": true,
            "verify": true,
            "type": "22618"
        }
    }
}
```


**The third payment request:**
```
POST HTTP/1.1
Host: http://127.0.0.1:8000//paymeuz/payment/
{
    "id": 123,
    "params": {   	"token":"5f460c3d4e6d0841074e7457_YgQMNCttjxKTMKcfN0GPSaaKyV4zPnJqRP4iezHfBGJBpfAyjJf0onx5QXIkmChPDdGJrUpXj2EqWFnTicR4W7p1nXFVvKPegirWSYObyNvrcz18IQbbAVXPTOq1cFQQVrfN1tBM3XdQChu3yr1kTokO7vmeGyCyPZzdO0G4SJeKIwsJiJJk8jvGYpYk0csZh0OhTd01sXIu1qQ4H79qN5vIi5U9rpQcwWra9ueCgJqgU4XgWE2OaGjY4G3qpDHr7ezOUg4Ud3M7S8A1CnsubOD0rhUnOdwWhIU6wuNVJX6xNYD5vjRd4W1StByQeEgIFWHTe4md6nCpSKANPUCH7xnfa3UUu2gz9WJ0PDmOoPwdVo53v9OpQ23kta0sUzMJgSJt",
        "amount": 200000,
        "account": {
            "order_id": 1
        }
    }
}
```


**Response:**
```
{
  "jsonrpc": "2.0",
  "id": 123,
  "result": {
    "receipt": {
      "_id": "2e0b1bc1f1eb50d487ba268d",
      "create_time": 1481113810044,
      "pay_time": 1481113810265,
      "cancel_time": 0,
      "state": 4,
      "type": 1,
      "external": false,
      "operation": -1,
      "category": null,
      "error": null,
      "description": "",
      "detail": null,
      "amount": 500000,
      "commission": 0,
      "account": [
        {
          "name": "order_id",
          "title": "Код заказа",
          "value": "5"
        }
      ],
      "card": {
        "number": "444444******4444",
        "expire": "0420"
      },
      "merchant": {
        "_id": "100fe486b33784292111b7dc",
        "name": "Online Shop LLC",
        "organization": "ЧП «Online Shop»",
        "address": "",
        "epos": {
          "merchantId": "106600000050000",
          "terminalId": "20660000"
        },
        "date": 1480582278779,
        "logo": null,
        "type": "Shop",
        "terms": null
      },
      "meta": null
    }
  }
}
```

Owner: www.khayitovdev.uz

