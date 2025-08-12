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
import { apiService } from '@/services/api';

const ChatScreen: React.FC = () => {
    return (
        <View style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>Chat Screen</Text>
                <Text style={styles.instructions}>
                    Chat with friends and family
                </Text>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#f8f9fa'
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
    }
})

export default ChatScreen;