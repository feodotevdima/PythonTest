запуск бд: docker-compose up

инициализация базы и добавлениие данных: python scripts/init_db.py

запуск приложения: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 

пользователи, добавленные в базу:
  {"username": "user1", "password": "password1"},
  {"username": "user2", "password": "password2"},
  {"username": "user3", "password": "password3"},

в приложении авторизация реализована с помощью jwt токенов, access для получения доступа, refresh для обнавления, не реализовывал сохранение ссесий, так как время ограниченно.

для автризации в swagger необходимо авторизоваться через endpoint login
<img width="1154" height="925" alt="image" src="https://github.com/user-attachments/assets/b6451802-ccab-4576-8219-f3f61b9de3cd" />

сопировать access токен из ответа сервера, открыть в правом верхнем углу кнпку authorize 
<img width="155" height="42" alt="image" src="https://github.com/user-attachments/assets/60b0940c-6b1c-43df-ba04-331fa813360b" />

откроется окно, в поле для ввода ввестим токен, нажать кнопку authorize, после чего, если правильный токен, будет доступ ко всем защищенным ендпоинтам.
Срок действия токена 30 минут, устанавливается в файле config, когда срок действия заканчивается, необходимо его обновить, по ендпоинту refresh пердать refresh токен, в ответ призодит новая пара access и refresh токенов.


Скрины swaggr:

Поиск по подстроке нмера:
<img width="1007" height="730" alt="image" src="https://github.com/user-attachments/assets/7cd4b545-0f4f-47e2-972e-5512e90964c3" />

поиск по точной стоимости и по диапазону:
<img width="974" height="781" alt="image" src="https://github.com/user-attachments/assets/62083e50-1281-43e3-ac9e-932cee4f65ec" />
<img width="974" height="772" alt="image" src="https://github.com/user-attachments/assets/34b30a90-7b93-41bc-add2-cc3200a2740d" />

добавление нового контейнера и попытка добавить дубликат:
<img width="974" height="826" alt="image" src="https://github.com/user-attachments/assets/38c85a33-47d4-461b-8901-60c15683dc0b" />
<img width="1129" height="932" alt="image" src="https://github.com/user-attachments/assets/921cf4ee-25cc-42c0-85ae-9ed9ee2d212d" />





