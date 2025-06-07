[app]
title = Mutuelle MTK
package.name = mutuellemtk
package.domain = org.mutuellemtk.app

source.dir = .
source.include_exts = py,kv,png,jpg,json
source.exclude_dirs = venv,__pycache__,bin,build

version = 1.0

# ✅ cython est requis et laissé
requirements = python3,cython,kivy,kivy_garden.webview,android,pyjnius,requests

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.minapi = 23
android.api = 31
android.target = 31
android.archs = arm64-v8a

android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.ndk_path = ~/.buildozer/android/platform/android-ndk-r23b

[buildozer]
log_level = 2
warn_on_root = 1