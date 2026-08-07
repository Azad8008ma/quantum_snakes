[app]
title = Quantum Snake Mobile
package.name = quantumsnake
package.domain = com.quantumsnake
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3
version = 1.0.0

requirements = python3,kivy,kivymd,pygame,cython

orientation = portrait
fullscreen = 0
android.permissions = VIBRATE

android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25c
android.ndk_api = 21
android.accept_sdk_license = True

android.archs = arm64-v8a, armeabi-v7a
android.logcat_filters = *:S python:D

[buildozer]
log_level = 2
warn_on_root = 1
