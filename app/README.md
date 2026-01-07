# Django + Stripe demo

Запуск локально:

1. Установите зависимости:

```bash
python -m pip install -r requirements.txt
```

2. Установите переменные окружения (пример для Windows PowerShell):

```powershell
$env:STRIPE_SECRET_KEY = 'sk_test_...'
$env:STRIPE_PUBLISHABLE_KEY = 'pk_test_...'
```

3. Примените миграции и создайте суперпользователя:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. Запустите сервер:

```bash
python manage.py runserver
```

5. Админка доступна по `/admin/`.

Примеры:
- Страница товара: `http://localhost:8000/item/1`
- Endpoint для создания Stripe Session: `http://localhost:8000/buy/1`

Примечания:
- Поле `Item.price` хранится в минимальных единицах валюты (cents для USD).
- Для тестирования используйте тестовые ключи Stripe.

Docker
------
Сборка и запуск через Docker Compose:

```bash
docker compose build
docker compose up
```

Копируйте `.env.example` в `.env` и заполните `STRIPE_SECRET_KEY` и `STRIPE_PUBLISHABLE_KEY` перед запуском.
