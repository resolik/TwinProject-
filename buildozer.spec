[app]
title = Twin
package.name = twin
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

# Изменил на 0.2, чтобы GitHub Actions не использовал старый битый кэш
version = 0.2

# Убрал hostpython3, оставил только базу
requirements = python3,kivy

orientation = portrait

# Android specific
fullscreen = 0
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21

# ФИКС ОШИБКИ: явно задаем стабильную версию NDK
android.ndk = 25b
android.ndk_api = 21

android.accept_sdk_license = True

# Оставил только одну архитектуру для надежности первого билда
android.archs = arm64-v8a

android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
