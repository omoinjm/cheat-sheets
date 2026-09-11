#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Set Java to version 21 if we are in the local Codespace and JAVA_HOME isn't already set correctly
LOCAL_JAVA_21="/usr/local/sdkman/candidates/java/21.0.10-ms"
if [ -z "$JAVA_HOME" ] || [ ! -d "$JAVA_HOME" ]; then
    if [ -d "$LOCAL_JAVA_21" ]; then
        export JAVA_HOME="$LOCAL_JAVA_21"
        export PATH="$JAVA_HOME/bin:$PATH"
    fi
fi

echo "☕ Using Java version:"
java -version

echo "🚀 Starting Android Build Process..."

# 1. Build the web version of the mobile app
echo "📦 Building web assets in apps/mobile..."
cd apps/mobile
if [ ! -f "index.html" ]; then
    echo "❌ CRITICAL ERROR: apps/mobile/index.html not found!"
    ls -la
    exit 1
fi
# Use npx vite directly to be sure about path resolution
npx vite build --config vite.config.js
cd ../..

# 2. Check if android platform exists, if not add it
if [ ! -d "apps/mobile/android" ]; then
    echo "➕ Adding Android platform to Capacitor..."
    cd apps/mobile
    npx cap add android
    cd ../..
fi

# 3. Sync the web assets into the Android project
echo "🔄 Syncing assets with Capacitor..."
cd apps/mobile
npx cap sync android

# 4. Build the Android APK using Gradle
if [ -z "$ANDROID_HOME" ] && [ ! -f "apps/mobile/android/local.properties" ]; then
    echo "⚠️  Android SDK not found (ANDROID_HOME is not set)."
    echo "💡 To generate the APK, please either:"
    echo "   a) Run this script on a machine with Android Studio installed."
    echo "   b) Open the 'apps/mobile/android' folder in Android Studio on your local machine."
    echo "   c) Set up a GitHub Action to build the APK in the cloud."
    echo ""
    echo "Web assets have been synced to the Android project. You can now build manually."
    exit 0
fi

BUILD_TYPE=${BUILD_TYPE:-debug}
GRADLE_TASK="assemble${BUILD_TYPE^}"

echo "🏗️ Building APK with Gradle (Task: $GRADLE_TASK)..."
cd android
./gradlew $GRADLE_TASK

# 5. Output the result
APK_DIR="app/build/outputs/apk/$BUILD_TYPE"
APK_PATH="$APK_DIR/app-$BUILD_TYPE.apk"
if [ -f "$APK_PATH" ]; then
    echo "✅ Success! APK generated at: apps/mobile/android/$APK_PATH"
else
    # Fallback for release APK which might be differently named or in a different place
    echo "🔎 Searching for generated APK..."
    find . -name "*.apk"
fi