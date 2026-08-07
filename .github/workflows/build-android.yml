name: Build Kivy APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    container:
      image: kivy/buildozer:latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build APK with Buildozer
        run: |
          export HOME=/home/user
          buildozer android debug

      - name: Upload APK artifact
        if: success()
        uses: actions/upload-artifact@v4
        with:
          name: kivy-apk
          path: bin/*.apk
