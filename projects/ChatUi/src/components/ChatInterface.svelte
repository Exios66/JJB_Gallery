<script>
	import { createEventDispatcher } from 'svelte';
	
	export let messages = [];
	export let isLoading = false;
	
	const dispatch = createEventDispatcher();
	
	let inputValue = '';
	
	function handleSubmit() {
		if (!inputValue.trim() || isLoading) return;
		
		const userMessage = {
			role: 'user',
			content: inputValue,
			timestamp: new Date().toISOString()
		};
		
		messages = [...messages, userMessage];
		inputValue = '';
		isLoading = true;
		
		dispatch('message', userMessage);
		
		// Simulate response (replace with actual API call)
		setTimeout(() => {
			const assistantMessage = {
				role: 'assistant',
				content: 'This is a placeholder response. Connect to your LLM API to get real responses.',
				timestamp: new Date().toISOString()
			};
			messages = [...messages, assistantMessage];
			isLoading = false;
		}, 1000);
	}
	
	function handleKeydown(event) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSubmit();
		}
	}
</script>

<div class="chat-container">
	<div class="messages">
		{#each messages as message}
			<div class="message message--{message.role}">
				<div class="message-content">
					{message.content}
				</div>
				<div class="message-timestamp">
					{new Date(message.timestamp).toLocaleTimeString()}
				</div>
			</div>
		{/each}
		
		{#if isLoading}
			<div class="message message--assistant">
				<div class="message-content loading">
					<span class="typing-indicator">
						<span></span><span></span><span></span>
					</span>
				</div>
			</div>
		{/if}
	</div>
	
	<form on:submit|preventDefault={handleSubmit} class="input-form">
		<textarea
			bind:value={inputValue}
			on:keydown={handleKeydown}
			placeholder="Type your message..."
			rows="1"
			disabled={isLoading}
		></textarea>
		<button type="submit" disabled={isLoading || !inputValue.trim()}>
			Send
		</button>
	</form>
</div>

<style>
	.chat-container {
		display: flex;
		flex-direction: column;
		height: 80vh;
		max-height: 800px;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		overflow: hidden;
		background: white;
	}
	
	.messages {
		flex: 1;
		overflow-y: auto;
		padding: 1rem;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
	
	.message {
		display: flex;
		flex-direction: column;
		max-width: 70%;
		animation: fadeIn 0.3s;
	}
	
	.message--user {
		align-self: flex-end;
	}
	
	.message--assistant {
		align-self: flex-start;
	}
	
	.message-content {
		padding: 0.75rem 1rem;
		border-radius: 12px;
		word-wrap: break-word;
	}
	
	.message--user .message-content {
		background: #007bff;
		color: white;
	}
	
	.message--assistant .message-content {
		background: #f0f0f0;
		color: #333;
	}
	
	.message-content.loading {
		background: #f0f0f0;
		padding: 1rem;
	}
	
	.message-timestamp {
		font-size: 0.75rem;
		color: #999;
		margin-top: 0.25rem;
		padding: 0 0.5rem;
	}
	
	.typing-indicator {
		display: flex;
		gap: 4px;
	}
	
	.typing-indicator span {
		width: 8px;
		height: 8px;
		border-radius: 50%;
		background: #999;
		animation: bounce 1.4s infinite;
	}
	
	.typing-indicator span:nth-child(2) {
		animation-delay: 0.2s;
	}
	
	.typing-indicator span:nth-child(3) {
		animation-delay: 0.4s;
	}
	
	.input-form {
		display: flex;
		padding: 1rem;
		border-top: 1px solid #e0e0e0;
		gap: 0.5rem;
		background: white;
	}
	
	.input-form textarea {
		flex: 1;
		padding: 0.75rem;
		border: 1px solid #e0e0e0;
		border-radius: 8px;
		resize: none;
		font-family: inherit;
		font-size: 1rem;
	}
	
	.input-form textarea:focus {
		outline: none;
		border-color: #007bff;
	}
	
	.input-form button {
		padding: 0.75rem 1.5rem;
		background: #007bff;
		color: white;
		border: none;
		border-radius: 8px;
		cursor: pointer;
		font-weight: 500;
	}
	
	.input-form button:hover:not(:disabled) {
		background: #0056b3;
	}
	
	.input-form button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}
	
	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}
	
	@keyframes bounce {
		0%, 60%, 100% {
			transform: translateY(0);
		}
		30% {
			transform: translateY(-10px);
		}
	}
</style>

