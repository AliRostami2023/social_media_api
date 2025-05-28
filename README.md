
# Social Media

یک شبکه اجتماعی قدرتمند و مقیاس‌پذیر ساخته‌شده با Django و Django REST Framework که امکاناتی مشابه توییتر ارائه می‌دهد. کاربران می‌توانند پست ایجاد کنند، لایک و کامنت بگذارند، نوتیفیکیشن دریافت کنند و فعالیت‌های اخیر خود را مشاهده نمایند.


## 🚀 امکانات کلیدی

- ✏️ ایجاد پست توسط کاربران
- ❤️ لایک و 💬 کامنت برای هر پست
- 🔔 نوتیفیکیشن لحظه‌ای برای رویدادهای مهم
- 📜 نمایش فعالیت‌های اخیر کاربران
- ⚙️ طراحی ماژولار و مقیاس‌پذیر
- 🧠 استفاده از WebSocket برای دریافت نوتیفیکیشن‌ها به‌صورت Real-time
- 🎯 استفاده از Celery برای پردازش‌های غیربلادرنگ
- 🐳 Docker و Docker Compose برای اجرای ساده و توسعه سریع



## 🛠️ تکنولوژی‌های استفاده‌شده

- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery](https://docs.celeryq.dev/)
- [Redis](https://redis.io/) (برای Broker و Cache)
- [Docker](https://www.docker.com/)
- [WebSocket (Django Channels)](https://channels.readthedocs.io/en/stable/)
- [PostgreSQL](https://www.postgresql.org/)



## 📦 نصب و اجرا

### 1. کلون کردن پروژه

```bash
git clone https://github.com/AliRostami2023/social_media_api
cd config

## 📁 ساختار پروژه

social_media_api/
├── config/                           # پوشه اصلی شامل تنظیمات و اپ‌ها
│   ├── __init__.py
│   ├── settings.py                   # تنظیمات Django
│   ├── urls.py                       # روت‌های اصلی پروژه
│   ├── wsgi.py
│   ├── asgi.py
│
│   ├── user_account/                      # اپ حساب کاربری (ورود، ثبت‌نام، پروفایل)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── ...
│
│   ├── post/                         # اپ پست (پست، لایک، ری‌پست)
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── ...
│
│   ├── core/                 
│   │   ├── models.py
│   │   ├── consumers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│
│   ├── activity/                    # اپ فعالیت کاربران
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── ...
│
│   └── follower/                       # مربوط به نوتیفیکیشن و سیستم فالو
│       ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── ...
│
├── manage.py                         # فایل مدیریت پروژه Django
├── .gitignore                        # فایل‌های نادیده گرفته‌شده توسط Git
├── requirements.txt                 # لیست پکیج‌های مورد نیاز
└── README.md

