import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  RefreshControl,
  Alert,
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';
import { apiService } from '@/services/api';
import { useFocusEffect } from '@react-navigation/native';

interface Device {
  id: number;
  device_id: string;
  device_name: string;
  created_at: string;
  last_active: string;
  is_active: boolean;
}

const DevicesScreen: React.FC = () => {
  const [devices, setDevices] = useState<Device[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const [loading, setLoading] = useState(true);
  const { token, showSnackbar } = useAuth();

  const loadDevices = async () => {
    try {
      const deviceList = await apiService.getDevices(token!);
      setDevices(deviceList);
    } catch (error: any) {
      showSnackbar(error.message || 'Failed to load devices');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      loadDevices();
    }, [token])
  );

  const onRefresh = () => {
    setRefreshing(true);
    loadDevices();
  };

  const revokeDevice = (deviceId: string, deviceName: string) => {
    Alert.alert(
      'Revoke Device',
      `Are you sure you want to revoke access for "${deviceName}"?`,
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Revoke',
          style: 'destructive',
          onPress: () => handleRevokeDevice(deviceId),
        },
      ]
    );
  };

  const handleRevokeDevice = async (deviceId: string) => {
    try {
      await apiService.revokeDevice(deviceId, token!);
      showSnackbar('Device revoked successfully!');
      loadDevices();
    } catch (error: any) {
      showSnackbar(error.message || 'Failed to revoke device');
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const DeviceCard: React.FC<{ device: Device }> = ({ device }) => (
    <View style={styles.deviceCard}>
      <View style={styles.deviceInfo}>
        <View style={styles.deviceHeader}>
          <Text style={styles.deviceName}>
            {device.device_name}
          </Text>
          <View style={[
            styles.statusBadge,
            device.is_active ? styles.statusActive : styles.statusInactive
          ]}>
            <Text style={[
              styles.statusText,
              device.is_active ? styles.statusActiveText : styles.statusInactiveText
            ]}>
              {device.is_active ? '🟢 Active' : '🔴 Inactive'}
            </Text>
          </View>
        </View>
        
        <Text style={styles.deviceDate}>
          Created: {formatDate(device.created_at)}
        </Text>
        <Text style={styles.deviceDate}>
          Last Active: {formatDate(device.last_active)}
        </Text>
      </View>

      {device.is_active && (
        <TouchableOpacity
          style={styles.revokeButton}
          onPress={() => revokeDevice(device.device_id, device.device_name)}
        >
          <MaterialIcons name="delete" size={20} color="white" />
          <Text style={styles.revokeButtonText}>Revoke</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Loading devices...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Linked Devices</Text>
        <TouchableOpacity style={styles.refreshButton} onPress={onRefresh}>
          <MaterialIcons name="refresh" size={24} color="#667eea" />
        </TouchableOpacity>
      </View>

      <ScrollView
        style={styles.scrollView}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {devices.length === 0 ? (
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyIcon}>📱</Text>
            <Text style={styles.emptyTitle}>No linked devices found</Text>
            <Text style={styles.emptySubtitle}>
              Scan a QR code to link your first device!
            </Text>
          </View>
        ) : (
          devices.map((device) => (
            <DeviceCard key={device.id} device={device} />
          ))
        )}
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: '#333',
  },
  refreshButton: {
    padding: 8,
    borderRadius: 8,
    backgroundColor: 'white',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
  },
  scrollView: {
    flex: 1,
    paddingHorizontal: 20,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
  },
  deviceCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 15,
    flexDirection: 'row',
    alignItems: 'center',
    elevation: 3,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
  },
  deviceInfo: {
    flex: 1,
  },
  deviceHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  deviceName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    flex: 1,
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  statusActive: {
    backgroundColor: '#d4edda',
  },
  statusInactive: {
    backgroundColor: '#f8d7da',
  },
  statusText: {
    fontSize: 12,
    fontWeight: '600',
  },
  statusActiveText: {
    color: '#155724',
  },
  statusInactiveText: {
    color: '#721c24',
  },
  deviceDate: {
    fontSize: 12,
    color: '#666',
    marginBottom: 2,
  },
  revokeButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#dc3545',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    marginLeft: 10,
  },
  revokeButtonText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
    marginLeft: 4,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 20,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 10,
    textAlign: 'center',
  },
  emptySubtitle: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    lineHeight: 20,
  },
});

export default DevicesScreen;
