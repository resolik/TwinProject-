[app]
title = Twin
package.name = twin
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
version = 0.3

# Оставляем только самый минимум. Cython и прочее Гитхаб поставит сам.
requirements = python3,kivy==2.3.0

orientation = portrait
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21

# Вот тут магия: принудительно заставляем его использовать конкретную версию
android.ndk = 25b
android.ndk_api = 21

# Добавь эту строку, если её нет, или проверь, чтобы было именно так:
android.skip_update = False
android.accept_sdk_license = True

# Оставляем только одну архитектуру (это ускорит билд и уменьшит шанс ошибки)
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
