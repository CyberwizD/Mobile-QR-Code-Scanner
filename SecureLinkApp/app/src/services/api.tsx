const API_BASE_URL = 'http://localhost:8000';

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    username: string;
    email: string;
    created_at: string;
    is_active: boolean;
  };
}

interface Device {
  id: number;
  device_id: string;
  device_name: string;
  created_at: string;
  last_active: string;
  is_active: boolean;
}

class ApiService {
  private async makeRequest(url: string, options: RequestInit = {}) {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  async login(username: string, password: string): Promise<LoginResponse> {
    return this.makeRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    });
  }

  async register(username: string, email: string, password: string): Promise<any> {
    return this.makeRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, email, password }),
    });
  }

  async scanQR(sessionId: string, token: string): Promise<any> {
    return this.makeRequest('/qr/scan', {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId }),
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async getDevices(token: string): Promise<Device[]> {
    return this.makeRequest('/devices', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }

  async revokeDevice(deviceId: string, token: string): Promise<any> {
    return this.makeRequest(`/devices/${deviceId}`, {
      method: 'DELETE',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  }
}

export const apiService = new ApiService();
