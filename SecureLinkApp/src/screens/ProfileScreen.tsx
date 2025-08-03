import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
  Modal,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { MaterialIcons } from '@expo/vector-icons';
import { useAuth } from '../context/AuthContext';

interface ProfileScreenProps {
  navigation: any;
}

const ProfileScreen: React.FC<ProfileScreenProps> = ({ navigation }) => {
  const { user, logout, showSnackbar } = useAuth();
  const [feedbackMessage, setFeedbackMessage] = useState<string>('');
  const [showLogoutModal, setShowLogoutModal] = useState(false);

  // Function to show feedback
  const showFeedback = (message: string) => {
    setFeedbackMessage(message);
    setTimeout(() => setFeedbackMessage(''), 3000);
  };

  const handleLogout = () => {
    console.log('🔴 LOGOUT BUTTON PRESSED');
    setShowLogoutModal(true);
  };

  const confirmLogout = async () => {
    try {
      setShowLogoutModal(false);
      showFeedback('Logging out...');
      
      await logout();
      showFeedback('Logged out successfully!');
      
      setTimeout(() => {
        if (navigation && navigation.reset) {
          navigation.reset({
            index: 0,
            routes: [{ name: 'Auth' }],
          });
        }
      }, 1500);
    } catch (error) {
      console.error('Logout error:', error);
      showFeedback('Failed to logout. Please try again.');
    }
  };

  const handleSettings = () => {
    console.log('⚙️ SETTINGS BUTTON PRESSED');
    showFeedback('Settings feature coming soon!');
  };

  const handleHelp = () => {
    console.log('❓ HELP BUTTON PRESSED');
    showFeedback('Help: Contact support@securelink.app');
  };

  const handleEditProfile = () => {
    console.log('👤 EDIT PROFILE BUTTON PRESSED');
    showFeedback('Edit Profile feature coming soon!');
  };

  const handleSecuritySettings = () => {
    console.log('🔒 SECURITY SETTINGS BUTTON PRESSED');
    showFeedback('Security Settings feature coming soon!');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
    });
  };

  return (
    <ScrollView style={styles.container} showsVerticalScrollIndicator={false}>
      {/* Feedback Message */}
      {feedbackMessage ? (
        <View style={styles.feedbackContainer}>
          <Text style={styles.feedbackText}>{feedbackMessage}</Text>
        </View>
      ) : null}

      {/* Profile Header */}
      <LinearGradient
        colors={['#667eea', '#764ba2']}
        style={styles.profileHeader}
      >
        <TouchableOpacity style={styles.avatarContainer} onPress={handleEditProfile}>
          <Text style={styles.avatar}>👤</Text>
          <View style={styles.editIcon}>
            <MaterialIcons name="edit" size={16} color="white" />
          </View>
        </TouchableOpacity>
        <Text style={styles.username}>{user?.username || 'Test User'}</Text>
        <Text style={styles.email}>{user?.email || 'test@example.com'}</Text>
      </LinearGradient>

      {/* Stats Section */}
      <View style={styles.statsContainer}>
        <View style={styles.statsGrid}>
          <View style={styles.statCard}>
            <MaterialIcons name="calendar-today" size={24} color="#667eea" />
            <Text style={styles.statTitle}>Member Since</Text>
            <Text style={styles.statValue}>
              {user?.created_at ? formatDate(user.created_at) : 'August 2025'}
            </Text>
          </View>
          <View style={styles.statCard}>
            <MaterialIcons name="verified-user" size={24} color="#28a745" />
            <Text style={styles.statTitle}>Account Status</Text>
            <Text style={styles.statValue}>Active</Text>
          </View>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.actionsContainer}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        
        <TouchableOpacity 
          style={styles.actionItem} 
          onPress={handleEditProfile}
          activeOpacity={0.7}
        >
          <LinearGradient
            colors={['#4facfe', '#00f2fe']}
            style={styles.actionGradient}
          >
            <MaterialIcons name="person" size={24} color="white" />
            <Text style={styles.actionText}>Edit Profile</Text>
            <MaterialIcons name="chevron-right" size={24} color="white" />
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.actionItem} 
          onPress={handleSecuritySettings}
          activeOpacity={0.7}
        >
          <LinearGradient
            colors={['#43e97b', '#38f9d7']}
            style={styles.actionGradient}
          >
            <MaterialIcons name="security" size={24} color="white" />
            <Text style={styles.actionText}>Security Settings</Text>
            <MaterialIcons name="chevron-right" size={24} color="white" />
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* Settings Section */}
      <View style={styles.actionsContainer}>
        <Text style={styles.sectionTitle}>Settings</Text>
        
        <TouchableOpacity 
          style={styles.actionItem} 
          onPress={handleSettings}
          activeOpacity={0.7}
        >
          <LinearGradient
            colors={['#f093fb', '#f5576c']}
            style={styles.actionGradient}
          >
            <MaterialIcons name="settings" size={24} color="white" />
            <Text style={styles.actionText}>App Settings</Text>
            <MaterialIcons name="chevron-right" size={24} color="white" />
          </LinearGradient>
        </TouchableOpacity>

        <TouchableOpacity 
          style={styles.actionItem} 
          onPress={handleHelp}
          activeOpacity={0.7}
        >
          <LinearGradient
            colors={['#667eea', '#764ba2']}
            style={styles.actionGradient}
          >
            <MaterialIcons name="help" size={24} color="white" />
            <Text style={styles.actionText}>Help & Support</Text>
            <MaterialIcons name="chevron-right" size={24} color="white" />
          </LinearGradient>
        </TouchableOpacity>
      </View>

      {/* Security Notice */}
      <View style={styles.securityContainer}>
        <View style={styles.securityCard}>
          <View style={styles.securityHeader}>
            <MaterialIcons name="security" size={20} color="#28a745" />
            <Text style={styles.securityTitle}>Security Notice</Text>
          </View>
          <Text style={styles.securityText}>
            Your account is protected with secure QR authentication. Only scan QR codes from trusted sources and never share your login credentials.
          </Text>
        </View>
      </View>

      {/* Logout Section */}
      <View style={styles.logoutContainer}>
        <TouchableOpacity 
          style={styles.logoutButton} 
          onPress={handleLogout}
          activeOpacity={0.8}
        >
          <MaterialIcons name="logout" size={24} color="white" />
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>

      {/* Logout Confirmation Modal */}
      <Modal
        visible={showLogoutModal}
        transparent={true}
        animationType="fade"
        onRequestClose={() => setShowLogoutModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalTitle}>Confirm Logout</Text>
            <Text style={styles.modalMessage}>Are you sure you want to logout?</Text>
            
            <View style={styles.modalButtons}>
              <TouchableOpacity 
                style={[styles.modalButton, styles.cancelButton]} 
                onPress={() => setShowLogoutModal(false)}
              >
                <Text style={styles.cancelButtonText}>Cancel</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={[styles.modalButton, styles.logoutModalButton]} 
                onPress={confirmLogout}
              >
                <Text style={styles.logoutButtonText}>Logout</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  feedbackContainer: {
    backgroundColor: '#28a745',
    paddingVertical: 12,
    paddingHorizontal: 20,
    marginHorizontal: 20,
    marginTop: 10,
    borderRadius: 8,
    alignItems: 'center',
  },
  feedbackText: {
    color: 'white',
    fontWeight: '600',
    fontSize: 14,
  },
  profileHeader: {
    alignItems: 'center',
    paddingVertical: 40,
    paddingTop: 60,
    marginHorizontal: 20,
    marginTop: 20,
    borderRadius: 20,
    elevation: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  avatarContainer: {
    position: 'relative',
    marginBottom: 15,
  },
  avatar: {
    fontSize: 64,
  },
  editIcon: {
    position: 'absolute',
    bottom: 0,
    right: 0,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 12,
    padding: 4,
  },
  username: {
    fontSize: 24,
    fontWeight: '700',
    color: 'white',
    marginBottom: 5,
  },
  email: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.9)',
  },
  statsContainer: {
    paddingHorizontal: 20,
    marginTop: 25,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statCard: {
    backgroundColor: 'white',
    flex: 1,
    marginHorizontal: 5,
    padding: 20,
    borderRadius: 16,
    alignItems: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  statTitle: {
    fontSize: 12,
    color: '#666',
    marginBottom: 8,
    marginTop: 8,
    textAlign: 'center',
    fontWeight: '500',
  },
  statValue: {
    fontSize: 16,
    fontWeight: '700',
    color: '#333',
    textAlign: 'center',
  },
  actionsContainer: {
    paddingHorizontal: 20,
    marginTop: 30,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#333',
    marginBottom: 15,
  },
  actionItem: {
    marginBottom: 15,
    borderRadius: 16,
    overflow: 'hidden',
    elevation: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
  },
  actionGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 18,
    paddingHorizontal: 20,
  },
  actionText: {
    flex: 1,
    fontSize: 16,
    fontWeight: '600',
    color: 'white',
    marginLeft: 15,
  },
  securityContainer: {
    paddingHorizontal: 20,
    marginTop: 30,
  },
  securityCard: {
    backgroundColor: '#f8fff9',
    padding: 20,
    borderRadius: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#28a745',
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  securityHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  securityTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginLeft: 8,
  },
  securityText: {
    fontSize: 14,
    color: '#666',
    lineHeight: 22,
  },
  logoutContainer: {
    paddingHorizontal: 20,
    paddingVertical: 30,
    paddingBottom: 40,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#dc3545',
    paddingVertical: 18,
    borderRadius: 16,
    elevation: 4,
    shadowColor: '#dc3545',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 3,
  },
  logoutText: {
    fontSize: 16,
    fontWeight: '700',
    color: 'white',
    marginLeft: 10,
  },
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContainer: {
    backgroundColor: 'white',
    borderRadius: 20,
    padding: 30,
    marginHorizontal: 40,
    elevation: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#333',
    textAlign: 'center',
    marginBottom: 15,
  },
  modalMessage: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 25,
    lineHeight: 22,
  },
  modalButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  modalButton: {
    flex: 1,
    paddingVertical: 12,
    borderRadius: 10,
    marginHorizontal: 5,
  },
  cancelButton: {
    backgroundColor: '#f8f9fa',
    borderWidth: 1,
    borderColor: '#dee2e6',
  },
  logoutModalButton: {
    backgroundColor: '#dc3545',
  },
  cancelButtonText: {
    color: '#666',
    fontWeight: '600',
    textAlign: 'center',
  },
  logoutButtonText: {
    color: 'white',
    fontWeight: '600',
    textAlign: 'center',
  },
});

export default ProfileScreen;