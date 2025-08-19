import React, { createContext, useContext, useState, useEffect, ReactNode, useRef } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert } from 'react-native';
import { WS_BASE_URL } from '@/services/api';

// Use the WebSocket type from undici-types
import { WebSocket as UndiciWebSocket } from 'undici-types/websocket';

interface User {
  id: number;
  username: string;
  email: string;
  created_at: string;
  is_active: boolean;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  login: (token: string, userData: User) => Promise<void>;
  logout: () => Promise<void>;
  updateUser: (userData: User, newToken?: string) => Promise<void>;
  showSnackbar: (message: string) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  // Use the WebSocket type from undici-types
  const ws = useRef<UndiciWebSocket | null>(null);

  useEffect(() => {
    loadStoredData();
  }, []);

  useEffect(() => {
    if (token) {
      connectWebSocket();
    } else {
      disconnectWebSocket();
    }

    return () => {
      disconnectWebSocket();
    };
  }, [token]);

  const connectWebSocket = () => {
    if (ws.current) {
      ws.current.close();
    }

    const wsUrl = `${WS_BASE_URL}/ws/listen?token=${token}`;
    ws.current = new WebSocket(wsUrl) as UndiciWebSocket;

    if (ws.current) {
      ws.current.onopen = () => {
        console.log('🔌 WebSocket connected');
      };

      ws.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'profile_updated') {
            console.log('🎉 Profile updated message received!');
            updateUser(data.user, data.access_token);
          }
        } catch (error) {
          console.error('Error processing WebSocket message:', error);
        }
      };

      ws.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };

      ws.current.onclose = () => {
        console.log('🔌 WebSocket disconnected');
      };
    }
  };

  const disconnectWebSocket = () => {
    if (ws.current) {
      ws.current.close();
      ws.current = null;
    }
  };

  const loadStoredData = async () => {
    try {
      const storedToken = await AsyncStorage.getItem('token');
      const storedUser = await AsyncStorage.getItem('user');
      
      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
      }
    } catch (error) {
      console.error('Error loading stored data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (newToken: string, userData: User) => {
    try {
      await AsyncStorage.setItem('token', newToken);
      await AsyncStorage.setItem('user', JSON.stringify(userData));
      setToken(newToken);
      setUser(userData);
    } catch (error) {
      console.error('Error storing login data:', error);
    }
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem('token');
      await AsyncStorage.removeItem('user');
      setToken(null);
      setUser(null);
      disconnectWebSocket();
    } catch (error) {
      console.error('Error clearing stored data:', error);
    }
  };

  const updateUser = async (userData: User, newToken?: string) => {
    try {
      await AsyncStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);
      if (newToken) {
        await AsyncStorage.setItem('token', newToken);
        setToken(newToken);
      }
    } catch (error) {
      console.error('Error updating user data:', error);
    }
  };

  const showSnackbar = (message: string) => {
    Alert.alert('Notification', message);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isLoading,
        login,
        logout,
        updateUser,
        showSnackbar,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
