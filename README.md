# m3u-aiogram
Телеграм бот по просмотру программ показа каналов телевидения.
#
### Как запустить проект:

#### Предварительные требования:
- развернутый m3u-backend и Redis
- заполненныый .env, см. env.sample

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/abp-ce/m3u_aiogram.git
```

```
cd m3u_aiogram
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
Запустить проект:

```
python main.py
```
### Стек:
 - aiogram 3.0.0b6
 - httpx 0.23.3
 - redis==4.4.2
