[app]
title = REVG – Πρόβλεψη μισθοδοσίας
package.name = revg
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt
version = 0.2

# Σημαντικό: δηλώνουμε ρητά KivyMD + android ώστε να μη σκάει στο launch
requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer,android

orientation = portrait

# (προαιρετικά) εικονίδιο αν έχεις π.χ. icon.png
# icon.filename = icon.png

[buildozer]
log_level = 2
# Να βλέπουμε Python logs στο logcat
android.logcat_filters = *:S python:D *:E

[app:android]
android.api = 31
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
p4a.bootstrap = sdl2
