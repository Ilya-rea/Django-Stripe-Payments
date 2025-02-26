# Django Stripe Payments

 ##Описание проекта

Этот проект представляет собой Django-приложение с интеграцией **Stripe API**. Оно позволяет:

- Создавать товары (Items)
- Оформлять оплату через Stripe Checkout
- Объединять товары в заказы (Orders)
- Применять скидки и налоги при оплате

##  Запуск проекта с Docker

###  1. Клонирование репозитория

Сначала клонируйте проект на локальную машину:

```sh
git clone https://github.com/Ilya-rea/Django-Stripe-Payments.git
cd Django-Stripe-Payments
```

###  2. Создание `.env` файла

Создайте в корневой директории файл `.env` и добавьте туда конфигурацию:

```sh
SECRET_KEY=your_django_secret_key
STRIPE_PUBLIC_KEY=your_stripe_public_key
STRIPE_SECRET_KEY=your_stripe_secret_key
```

###  3. Запуск контейнеров

Запустите приложение в контейнере с помощью Docker Compose:

```sh
docker-compose up --build
```

После успешного запуска приложение будет доступно по адресу: ``

##  Доступ в Django Admin

После запуска проекта можно войти в административную панель:

- **Адрес:** `http://localhost:8000/admin/`
- **Логин:** `ilya`
- **Пароль:** `123`

##  API Методы

| Метод | URL             | Описание                                  |
| ----- | --------------- | ----------------------------------------- |
| `GET` | `/item/{id}/`   | Страница товара с кнопкой оплаты          |
| `GET` | `/buy/{id}/`    | Получение Stripe Session для оплаты       |
| `GET` | `buy/order/{id}/` | Оплата заказа (с учетом скидок и налогов) |

##  Дополнительная информация

- **Документация Stripe API:** [stripe.com/docs](https://stripe.com/docs)
- **Автор:** [Ilya-rea](https://github.com/Ilya-rea)

