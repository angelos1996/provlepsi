[app]

# (str) Title of your application
title = REVG – Πρόβλεψη μισθοδοσίας

# (str) Package name
package.name = revg

# (str) Package domain (must be a valid domain)
package.domain = org.revg.app

# (str) Source code where your main.py is located
source.dir = app

# (str) Main .py file (without extension)
main.py = main

# (list) Extensions to include from the source folder
source.include_exts = py,kv,png,jpg,atlas

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (portrait, landscape or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Icon of the application
# icon.filename = %(source.dir)s/icon.png

# (str) Supported Android API
android.api = 33

# (str) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) Android logcat filters to use
log_level = 2

# (bool) Copy the default .pyo files instead of compiling them (Python2 only)
copy_libs = 1

# (bool) Enable logcat during build
logcat_on_launch = 1

# (str) Android entry point, default is ok
android.entrypoint = org.kivy.android.PythonActivity

# (list) Permissions (add more if needed)
android.permissions = INTERNET

# (str) Package version
version = 1.0

# (str) Application version code (used in Play Store)
android.version_code = 1

# (bool) Use AndroidX libraries
android.enable_androidx = True

# (bool) Include SQLite3 support
android.sqlite3 = True

# (bool) Enable crasher logging
android.logcat_filters = *:S python:D

# (str) Custom package name
#android.archs = arm64-v8a

# (str) Custom entry point activity
#android.entrypoint = org.kivy.android.PythonActivity

# (bool) Build with debug symbols
android.debug = True

# (str) Additional Java classpath
#android.add_jars = libs/*.jar

# (str) Additional AARs
#android.add_aars = libs/*.aar

# (bool) Enable multiprocess
#android.multiprocess = False

# (list) Android services to declare
#android.services =

# (str) Android boot script
#android.boot_script =

# (bool) Want to build with buildozer without launching Android Studio
android.accept_sdk_license = True
