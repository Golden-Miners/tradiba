type EventCallback = (payload: any) => void;

class WebSocketManager {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private isIntentionalClose = false;
  private subscriptions: Record<string, EventCallback[]> = {};

  constructor(url: string) {
    this.url = url;
  }

  connect() {
    this.isIntentionalClose = false;
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type && this.subscriptions[data.type]) {
          this.subscriptions[data.type].forEach(cb => cb(data.payload));
        }
      } catch (e) {
        console.error('WebSocket parse error:', e);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      if (!this.isIntentionalClose) {
        this.attemptReconnect();
      }
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  disconnect() {
    this.isIntentionalClose = true;
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }

  subscribe(eventType: string, callback: EventCallback) {
    if (!this.subscriptions[eventType]) {
      this.subscriptions[eventType] = [];
    }
    this.subscriptions[eventType].push(callback);
    
    // Return unsubscribe function
    return () => {
      this.subscriptions[eventType] = this.subscriptions[eventType].filter(cb => cb !== callback);
    };
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    }
  }

  private attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000);
      console.log(`Attempting reconnect in ${delay}ms...`);
      setTimeout(() => {
        this.connect();
      }, delay);
    } else {
      console.error('Max WebSocket reconnect attempts reached');
    }
  }
}

// Assuming API_URL is something like http://localhost:8000, we convert it to ws://localhost:8000/ws
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const WS_URL = API_URL.replace('http://', 'ws://').replace('https://', 'wss://') + '/ws';

export const wsManager = new WebSocketManager(WS_URL);
