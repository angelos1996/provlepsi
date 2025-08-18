[app]
title = REVG – Πρόβλεψη μισθοδοσίας
package.name = revg
package.domain = org.example
source.dir = app
source.include_exts = py,png,jpg,kv,txt
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer
orientation = portrait

[buildozer]
log_level = 2
warn_on_root = 0

[app:android]
android.api = 31
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
android.accept_sdk_license = True
