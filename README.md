# Телеграм-бот для Летней Лингвистической Школы 2023

В этом году в течение ЛЛШ будет проходить анонимная переписка живыми письмами!
Для того, чтобы сохранить анонимность участников переписки, мы написали бота.

#### Участники переписки могут:
- зарегистрировать свой псевдоним;
- попросить бота напомнить свой псевдоним;
- узнать псевдоним своего собеседника, если жеребьевка уже была проведена.

В планах также добавить возможность поменять псевдоним, если жеребьевки еще не было.
 
#### Организаторы могут:
- узнать, сколько участников зарегистрировалось;
- провести жеребьевку (если число участников четное);
- скачать файл, в котором для каждого участника будут указаны имя-фамилия, псевдоним, а также его собеседник.

Для того, чтобы использовать функционал организатора, нужно ввести определенный пароль.

Для работы бота вам понадобится **еще один файл**: mysecrets.py.
В нем должно быть всего 2 строчки: токен вашего бота и пароль для организаторов. 
```
BOT_TOKEN = "token" 
ADMIN_PASSWORD = "password"
```
