[app]

# (str) Title of your application
title = English Master

# (str) Package name
package.name = englishmaster

# (str) Package domain (needed for android/ios packaging)
package.domain = com.englishmaster

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json,ttf,ttf

# (str) The version of your application
version = 1.0.0

# (list) Application requirements
requirements = python3,kivy>=2.2.0,kivymd>=1.1.1

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

#
# Android specific
#

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK API to use. This is the minimum API your app will support, it should match android.minapi.
android.ndk_api = 21

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads for save time and/or bandwidth
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# This can be useful for CI environments or when you don't have interactive access
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) enables Android auto backup feature (Android API >=23)
android.allow_backup = True

# (str) XML formatting rules for the manifest file
android.manifest_rules =

# (list) Gradle dependencies
android.gradle_dependencies =

# (list) Java/JAR additions
android.add_jars =

# (list) Java class additions
android.add_src =

# (str) python-for-android branch to use
p4a.branch = master

# (str) python-for-android bootstrap to use
p4a.bootstrap = sdl2

# (str) python-for-android architecture
p4a.arch = arm64-v8a

#
# iOS specific
#

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_path = ../kivy-ios

# (str) Name of the certificate to use for signing the debug variant
#ios.certificate = 

# (str) Name of the profile to use for signing the release variant
#ios.profile = 

#
# Buildozer specific
#

# (int) Log level (0 = error only, 1 = info, 2 = debug (with commands))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
