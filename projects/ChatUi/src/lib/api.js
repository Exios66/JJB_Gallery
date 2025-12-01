/**
 * API client for Chat UI
 * Handles communication with LLM backends
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3000';

export class ChatAPI {
	constructor(baseURL = API_BASE_URL) {
		this.baseURL = baseURL;
	}

	async sendMessage(message, model = 'default', options = {}) {
		try {
			const response = await fetch(`${this.baseURL}/api/chat`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					message,
					model,
					...options
				}),
			});

			if (!response.ok) {
				throw new Error(`API error: ${response.statusText}`);
			}

			const data = await response.json();
			return data;
		} catch (error) {
			console.error('Error sending message:', error);
			throw error;
		}
	}

	async streamMessage(message, model = 'default', onChunk) {
		try {
			const response = await fetch(`${this.baseURL}/api/chat/stream`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					message,
					model,
				}),
			});

			if (!response.ok) {
				throw new Error(`API error: ${response.statusText}`);
			}

			const reader = response.body.getReader();
			const decoder = new TextDecoder();

			while (true) {
				const { done, value } = await reader.read();
				if (done) break;

				const chunk = decoder.decode(value);
				const lines = chunk.split('\n').filter(line => line.trim());

				for (const line of lines) {
					if (line.startsWith('data: ')) {
						const data = JSON.parse(line.slice(6));
						onChunk(data);
					}
				}
			}
		} catch (error) {
			console.error('Error streaming message:', error);
			throw error;
		}
	}

	async getModels() {
		try {
			const response = await fetch(`${this.baseURL}/api/models`);
			if (!response.ok) {
				throw new Error(`API error: ${response.statusText}`);
			}
			return await response.json();
		} catch (error) {
			console.error('Error fetching models:', error);
			return [];
		}
	}
}

export const chatAPI = new ChatAPI();

