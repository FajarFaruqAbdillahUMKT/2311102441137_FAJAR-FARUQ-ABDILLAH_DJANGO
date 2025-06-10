# main/settings.py
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'  # Ganti dengan kunci rahasia yang aman untuk produksi

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Application definition
INSTALLED_APPS = [
    'jazzmin', # Aplikasi untuk tampilan admin yang lebih baik

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',

    # Aplikasi kustom
    'dashboard',
    'rekomendasi_jurusan',
    'crispy_forms',
    'crispy_bootstrap5',
    'crispy_tailwind',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Makassar'  # Sesuaikan dengan WITA
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'dashboard.CustomUser'

# Login and Logout Redirects
LOGIN_URL = 'dashboard:login'
LOGIN_REDIRECT_URL = 'dashboard:list_mahasiswa'
LOGOUT_REDIRECT_URL = ''

# Crispy Forms Settings

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"  # atau "bootstrap4"
CRISPY_TEMPLATE_PACK = "tailwind"  # atau "bootstrap4"\

# ... (bagian bawah settings.py, setelah INSTALLED_APPS, dll.)

# ---------------- JAZZMIN CONFIGURATION ----------------
JAZZMIN_SETTINGS = {
    # Judul pada tab browser dan halaman login
    "site_title": "Admin SPK",

    # Judul di header halaman admin (logo teks)
    "site_header": "SPK Penjurusan",

    # Teks/logo kecil di pojok kiri atas
    "site_brand": "SPK Admin",

    # Logo untuk halaman login. Letakkan file gambar di folder 'static/' aplikasi Anda
    # "login_logo": "images/logo-login.png",

    # Logo untuk di pojok kiri atas.
    # "site_logo": "images/logo-sidebar.png",

    # Teks selamat datang di halaman login
    "welcome_sign": "Selamat Datang! Silakan Login",

    # Hak Cipta di bagian footer
    "copyright": "Proyek SPK Mahasiswa 2025",

    # Model yang ingin Anda cari di search bar global
    "search_model": ["auth.User", "rekomendasi_jurusan.Mahasiswa"],

    ############
    # UI Tweaks
    ############
    # Tema, ada banyak pilihan. Contoh: "cerulean", "cyborg", "darkly", "flatly", "journal", "litera", "lumen", "lux", "materia", "minty", "pulse", "sandstone", "simplex", "sketchy", "slate", "solar", "spacelab", "superhero", "united", "yeti"
    "theme": "litera",

    # Untuk tema gelap, gunakan "slate" atau "darkly"
    # "theme": "darkly",

    # Opsi untuk UI
    "show_ui_builder": False,  # Ubah jadi True jika ingin mencoba mengubah tema secara live

    "changeform_format": "horizontal_tabs",
    # "changeform_format": "single_tabs",
    # "changeform_format": "collapsible",

    "topmenu_links": [
        # Url bisa berupa nama view: 'admin:index'
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},

        # Link eksternal
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},

        # Model Admin
        {"model": "rekomendasi_jurusan.Mahasiswa"},
    ],

    # Kustomisasi menu/sidebar
    "side_menu_icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "rekomendasi_jurusan.Mahasiswa": "fas fa-user-graduate",
        "rekomendasi_jurusan.Kriteria": "fas fa-list-ol",
        "rekomendasi_jurusan.Alternatif": "fas fa-tasks",
        "rekomendasi_jurusan.NilaiMataKuliah": "fas fa-star-half-alt",
        "rekomendasi_jurusan.HasilRekomendasi": "fas fa-chart-bar",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
}
