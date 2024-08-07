# next-feature-bot

Бот для тестирования функционала BotX

## Инструкция по развёртыванию

1. Воспользуйтесь инструкцией [Руководство 
   администратора](https://express.ms/admin_guide.pdf) `-> Эксплуатация корпоративного
   сервера -> Управление контактами -> Чат-боты`, чтобы создать бота в панели
   администратора eXpress.
   Чтобы узнать `secret_key` и `bot_id`, необходимо нажать на имя созданного
   бота. `cts_host` -- это хост панели панели администратора.


2. Скачайте репозиторий на сервер:

```bash
git clone --recurse-submodules https://github.com/ExpressApp/next-feature-bot.git /opt/express/bots/next-feature-bot
cd /opt/express/bots/next-feature-bot
```

3. Отредактируйте `docker-compose.yml` подставив вместо `cts_host`,
   `secret_key` и `bot_id` реальные значения.


4. Запустите контейнер командой:

```bash
docker-compose up -d
```

5. Убедитесь, что в логах нет ошибок.

```bash
docker-compose logs
```

6. Найдите бота через поиск корпоративных контактов, напишите ему что-нибудь
   для проверки.
