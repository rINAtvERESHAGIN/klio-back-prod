# klio

kliogem.ru redesign


1. Клонируешь проект в папку
2. Дальше два пути.  
    1. Используешь pycharm.  
        1. Открываешь проект в pycharm.
            1. Нажимаешь File/New
            2. Выбираешь папку с проектом(корень там где лежит этот файл)
            3. Нажимаешь создать, пайчарм говорит что в папке уже есть файлы, нажимаешь 
               create from existing source.
        2. Pycharm создаст тебе виртуально окружение.  
        3. Создаешь конфигурацию запуска, для этого ищешь в верхней полоске выпадающий список рядом со стрелкой запуска.
            1. В выпадающем списке нажимаешь Edit Configuration
            2. В открывшемся окне нажимаешь на плюс и выбираешь там Django server
            3. Откроются параметры конфигурации запуска, ищешь Environment Variable
            4. Вносишь заполненные заранее параметры 
               (для того что бы они нормально вставлялись, нужно убрать комментарии и не вставлять никаких пробелов между равно, названием и значением)
                ```
                # Параметр отвечающий за отправку уведомлений админу при создании заказа
                NOTIFIABLE_ADMIN_EMAIL_WHEN_ORDER_CREATED=1;
                # Настройки процесинга оплаты
                B2P_SECTOR=1
                B2P_SECRET=1
                B2P_BASE_URL=1
                B2P_FAIL_REDIRECT=1
                B2P_SUCCESS_REDIRECT=1
                # Почта от которой все шлется
                DEFAULT_FROM_EMAIL=1
                # Настройки подключения к почтовому серверу
                EMAIL_HOST=1
                EMAIL_PORT=1
                EMAIL_USE_TLS=1
                EMAIL_HOST_USER=1
                EMAIL_HOST_PASSWORD=1
                ```
            5. Внизу параметров будет надпись о том, что у тебя не включена джанга, и ссылка где ее включать, нажимаешь
            6. В открывшемся окне в параметре Django project root нужно выбрать внутреннюю папку klio, так что бы путь заканчивался на klio/klio
            7. В параметре Settings выбираешь локальные настройки config/settings/local.py
            8. Параметр Manage script должен выбраться автоматически, но проверяешь что бы там стояло manage.py
        4. Используя терминал в pycharm устанавливаешь все из requirements командой `pip install -r requirements.txt`
            > проверь что бы были правильные версии у djangorestframework-simplejwt==4.5.0(раньше стояла 4.4.0, а ее с пипа дропнули)
            > и не забудь установить requests==2.26.0 если его нет в requirements
        5. В настройках config/settings/local нужно прописать настройку подключения к локальной PG
            ```
            DATABASES = values.DatabaseURLValue('<type>://<user>:<password>@<host>/<dbname>')
            ```
            где,
            - `<type>` - это тип базы данных, например для PG postgres
            - `<user>` - это пользователь имеющий доступ к нужной бд
            - `<password>` - это пароль от пользователя
            - `<host>` - это адрес бд, для локали `127.0.0.1`
            - `<dbname>`- это имя базы данных если импортировал с прода то `kliomaindb`
        6. Для работы терминала с окружением Django нужно залезть в File/Settings/Tools/Terminal и внести туда параметры из пункта c
    2. Если ты не используешь pycharm и создаешь виртуальное окружение руками.
        1. Создать виртуальное окружение.
        2. В файле activate для виртуального окружения прописать параметр из пунтка i.c, добавив к каждому export если пишешь под линуксом.
        3. В терминале зайти в виртуальное окружение и зайти в папку проекта
        4. Находясь в окружении выполнить установку параметров `pip install -r requirements.txt`(аналогично i.d)
        5. Аналогично пункту i.e настроить подключение к базе данных
        6. Перейти во внутреннюю папку klio где лежит manage.py
        7. Набрать команду запуска ./manage.py runserver

На этом запуск будет завершен и проект будет открываться по урлу

Для входа в админскую часть можно создать себе юзера через createsuperuser.