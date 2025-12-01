<script>
	import { onMount } from 'svelte';
	import ChatInterface from '../components/ChatInterface.svelte';
	
	let messages = [];
	let isLoading = false;
	
	onMount(() => {
		// Initialize chat interface
		console.log('Chat UI initialized');
	});
</script>

<svelte:head>
	<title>Chat UI</title>
</svelte:head>

<main>
	<div class="container">
		<header>
			<h1>Chat UI</h1>
			<p>A modern chat interface for open source models</p>
		</header>
		
		<ChatInterface {messages} {isLoading} />
	</div>
</main>

<style>
	.container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 2rem;
	}
	
	header {
		text-align: center;
		margin-bottom: 2rem;
	}
	
	header h1 {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
	}
	
	header p {
		color: #666;
		font-size: 1.1rem;
	}
</style>

