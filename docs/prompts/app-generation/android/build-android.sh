#!/usr/bin/env bash
set -euo pipefail

npm run build

if [[ ! -f "android/gradlew" ]]; then
  rm -rf android
  npx cap add android
fi

npm run android:sync
npm run android:build:debug
