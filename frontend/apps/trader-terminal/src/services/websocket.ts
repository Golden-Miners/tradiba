type MessageHandler = (data: any) => void;

export class WebSocketService {
  private ws: WebSocket | null = null;
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private handlers: Map<string, Set<MessageHandler>> = new Map();

  constructor(url: string = 'ws://localhost:8000/ws') {
    this.url = url;
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) return;

    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.reconnectAttempts = 0;
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        const type = message.type;
        if (type && this.handlers.has(type)) {
          this.handlers.get(type)!.forEach((handler) => handler(message.payload));
        }
      } catch (err) {
        console.error('Failed to parse WS message', err);
      }
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.handleReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  private handleReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      const timeout = Math.pow(2, this.reconnectAttempts) * 1000;
      setTimeout(() => {
        console.log(`Reconnecting attempt ${this.reconnectAttempts + 1}...`);
        this.reconnectAttempts++;
        this.connect();
      }, timeout);
    }
  }

  subscribe(type: string, handler: MessageHandler) {
    if (!this.handlers.has(type)) {
      this.handlers.set(type, new Set());
    }
    this.handlers.get(type)!.add(handler);
  }

  unsubscribe(type: string, handler: MessageHandler) {
    if (this.handlers.has(type)) {
      this.handlers.get(type)!.delete(handler);
    }
  }

  send(message: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      console.warn('Cannot send message, WebSocket not open');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

export const wsService = new WebSocketService();
