## INSTALLATION INSTRUCTIONS

## Setup Instructions

1. **Initialize React Native Project:**
   ```bash
   npx react-native init SecureLinkApp --template react-native-template-typescript
   cd SecureLinkApp
   ```

2. **Install Dependencies:**
   ```bash
   npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
   npm install react-native-screens react-native-safe-area-context
   npm install react-native-gesture-handler react-native-reanimated
   npm install @react-native-async-storage/async-storage
   npm install react-native-vector-icons
   npm install react-native-linear-gradient
   npm install react-native-camera
   ```

3. **iOS Setup:**
   ```bash
   cd ios && pod install && cd ..
   ```

4. **Android Setup:**
   
   Add to `android/app/src/main/java/.../MainApplication.java`:
   ```java
   import com.swmansion.gesturehandler.react.RNGestureHandlerPackage;
   import com.swmansion.reanimated.ReanimatedPackage;
   ```

   Add to `android/app/build.gradle`:
   ```gradle
   apply from: file("../../node_modules/@react-native-vector-icons/fonts.gradle")
   ```

   Add camera permissions to `android/app/src/main/AndroidManifest.xml`:
   ```xml
   <uses-permission android:name="android.permission.CAMERA" />
   <uses-permission android:name="android.permission.RECORD_AUDIO"/>
   <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
   <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
   ```

5. **iOS Camera Permissions:**
   
   Add to `ios/SecureLinkApp/Info.plist`:
   ```xml
   <key>NSCameraUsageDescription</key>
   <string>This app needs access to camera to scan QR codes</string>
   <key>NSMicrophoneUsageDescription</key>
   <string>This app needs access to microphone for camera functionality</string>
   ```

6. **Configure API Base URL:**
   
   Update the `API_BASE_URL` in `src/services/api.ts` to match your FastAPI server:
   ```typescript
   const API_BASE_URL = 'http://YOUR_SERVER_IP:8000';
   ```

7. **Run the App:**
   ```bash
   # For Android
   npx react-native run-android
   
   # For iOS
   npx react-native run-ios
   ```

## Features Implemented

✅ **Splash Screen** with animated logo
✅ **Authentication** (Login/Register) with beautiful gradients
✅ **Bottom Tab Navigation** with 4 main screens
✅ **Home Screen** with welcome card and quick actions
✅ **QR Scanner** with camera integration and real-time scanning
✅ **Device Management** with device listing and revoke functionality
✅ **User Profile** with stats, settings, and logout
✅ **API Integration** with FastAPI backend
✅ **Secure Storage** using AsyncStorage
✅ **Error Handling** with user-friendly messages
✅ **Material Design**
