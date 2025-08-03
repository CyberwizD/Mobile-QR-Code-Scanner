import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  Alert,
  Linking,
} from 'react-native';
import { CameraView, Camera } from 'expo-camera';
import { LinearGradient } from 'expo-linear-gradient';
import { useFocusEffect } from '@react-navigation/native';
import { useAuth } from '../context/AuthContext';
import { apiService } from '../services/api';

const { width, height } = Dimensions.get('window');

const QRScannerScreen: React.FC = () => {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [scanning, setScanning] = useState(false);
  const [status, setStatus] = useState('Ready to scan');
  const { token, showSnackbar } = useAuth();

  const requestCameraPermission = async () => {
    try {
      const { status } = await Camera.requestCameraPermissionsAsync();
      console.log('Camera permission status:', status);
      
      if (status === 'granted') {
        setHasPermission(true);
      } else if (status === 'denied') {
        setHasPermission(false);
        Alert.alert(
          'Camera Permission Required',
          'This app needs camera access to scan QR codes. Please enable camera permissions in your device settings.',
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Open Settings', onPress: () => Linking.openSettings() }
          ]
        );
      } else {
        setHasPermission(false);
      }
    } catch (error) {
      console.error('Error requesting camera permission:', error);
      setHasPermission(false);
    }
  };

  useEffect(() => {
    requestCameraPermission();
  }, []);

  // Re-check permissions when screen comes into focus
  useFocusEffect(
    React.useCallback(() => {
      const checkPermissions = async () => {
        const { status } = await Camera.getCameraPermissionsAsync();
        setHasPermission(status === 'granted');
      };
      checkPermissions();
    }, [])
  );

  const handleBarCodeScanned = async ({ type, data }: { type: string; data: string }) => {
    if (!scanning) return;

    setScanning(false); // Stop scanning immediately to prevent multiple scans
    
    try {
      console.log('QR Code scanned:', data);
      setStatus('QR Code detected! Processing...');
      
      const qrData = JSON.parse(data);
      const sessionId = qrData.session_id;

      if (sessionId) {
        const response = await apiService.scanQR(sessionId, token!);
        showSnackbar('Device linked successfully! 🎉');
        setStatus('Device linked successfully!');
        
        // Reset after 3 seconds
        setTimeout(() => {
          setStatus('Ready to scan');
        }, 3000);
      } else {
        throw new Error('Invalid QR code format');
      }
    } catch (error: any) {
      console.error('QR scan error:', error);
      const errorMessage = error.message || 'Failed to process QR code';
      setStatus(`Error: ${errorMessage}`);
      showSnackbar(errorMessage);
      
      // Reset after 3 seconds
      setTimeout(() => {
        setStatus('Ready to scan');
      }, 3000);
    }
  };

  const toggleScanning = () => {
    if (scanning) {
      setScanning(false);
      setStatus('Scanning stopped');
    } else {
      setScanning(true);
      setStatus('Scanning for QR codes...');
    }
  };

  if (hasPermission === null) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>QR Code Scanner</Text>
          <Text style={styles.instructions}>
            Checking camera permissions...
          </Text>
        </View>
        <View style={styles.permissionContainer}>
          <Text style={styles.permissionText}>Requesting camera permission...</Text>
        </View>
      </View>
    );
  }

  if (hasPermission === false) {
    return (
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.title}>QR Code Scanner</Text>
          <Text style={styles.instructions}>
            Camera access is required to scan QR codes
          </Text>
        </View>
        <View style={styles.permissionContainer}>
          <Text style={styles.permissionIcon}>📷</Text>
          <Text style={styles.permissionText}>No access to camera</Text>
          <Text style={styles.permissionSubtext}>
            Please grant camera permission to scan QR codes and link devices
          </Text>
          <TouchableOpacity
            style={styles.permissionButton}
            onPress={requestCameraPermission}
          >
            <Text style={styles.permissionButtonText}>Grant Permission</Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>QR Code Scanner</Text>
        <Text style={styles.instructions}>
          Point your camera at a QR code to scan it and link a new device
        </Text>
      </View>

      <View style={styles.cameraContainer}>
        {scanning ? (
          <CameraView
            style={styles.camera}
            onBarcodeScanned={scanning ? handleBarCodeScanned : undefined}
            barcodeScannerSettings={{
              barcodeTypes: ['qr'],
            }}
          >
            <View style={styles.scannerOverlay}>
              <View style={styles.scannerFrame} />
              <Text style={styles.scannerText}>
                Position QR code within the frame
              </Text>
            </View>
          </CameraView>
        ) : (
          <View style={styles.cameraPlaceholder}>
            <Text style={styles.cameraPlaceholderIcon}>📷</Text>
            <Text style={styles.cameraPlaceholderText}>Camera Preview</Text>
            <Text style={styles.cameraPlaceholderSubtext}>
              Tap 'Start Scanning' to begin
            </Text>
          </View>
        )}
      </View>

      <View style={styles.controls}>
        <TouchableOpacity style={styles.scanButton} onPress={toggleScanning}>
          <LinearGradient
            colors={scanning ? ['#ff6b6b', '#ee5a24'] : ['#667eea', '#764ba2']}
            style={styles.scanButtonGradient}
          >
            <Text style={styles.scanButtonText}>
              {scanning ? 'Stop Scanning' : 'Start Scanning'}
            </Text>
          </LinearGradient>
        </TouchableOpacity>

        <Text style={styles.statusText}>{status}</Text>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    padding: 20,
    paddingTop: 60,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#333',
    marginBottom: 10,
  },
  instructions: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    lineHeight: 20,
  },
  cameraContainer: {
    flex: 1,
    margin: 20,
    borderRadius: 15,
    overflow: 'hidden',
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 5 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
  },
  camera: {
    flex: 1,
  },
  scannerOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.3)',
  },
  scannerFrame: {
    width: 200,
    height: 200,
    borderWidth: 2,
    borderColor: '#667eea',
    borderRadius: 10,
    backgroundColor: 'transparent',
  },
  scannerText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
    marginTop: 20,
    textAlign: 'center',
  },
  cameraPlaceholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#e9ecef',
  },
  cameraPlaceholderIcon: {
    fontSize: 48,
    marginBottom: 20,
  },
  cameraPlaceholderText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#666',
    marginBottom: 10,
  },
  cameraPlaceholderSubtext: {
    fontSize: 14,
    color: '#999',
    textAlign: 'center',
  },
  controls: {
    padding: 20,
    alignItems: 'center',
  },
  scanButton: {
    width: '100%',
    borderRadius: 12,
    overflow: 'hidden',
    marginBottom: 15,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
  },
  scanButtonGradient: {
    paddingVertical: 15,
    alignItems: 'center',
  },
  scanButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
  statusText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  permissionContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    paddingHorizontal: 40,
  },
  permissionIcon: {
    fontSize: 64,
    marginBottom: 20,
  },
  permissionText: {
    fontSize: 18,
    color: '#333',
    fontWeight: '600',
    marginBottom: 10,
    textAlign: 'center',
  },
  permissionSubtext: {
    fontSize: 14,
    color: '#666',
    marginBottom: 30,
    textAlign: 'center',
    lineHeight: 20,
  },
  permissionButton: {
    backgroundColor: '#667eea',
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 12,
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  permissionButtonText: {
    color: 'white',
    fontSize: 16,
    fontWeight: '600',
  },
});

export default QRScannerScreen;