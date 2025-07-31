[app]
title = MyApp
package.name = myapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,kivymd,requests,opencv-python,pyzbar,pillow,numpy,python-dateutil
orientation = portrait
fullscreen = 1
android.archs = armeabi-v7a,arm64-v8a
android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.2
android.allow_backup = 1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
# Prevent freetype/hb build error (configure error)
p4a.branch = develop
p4a.extra_args = --ignore-setup-py --with-harfbuzz=no
