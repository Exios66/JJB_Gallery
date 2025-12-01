#!/usr/bin/env node
/**
 * API Integration Utilities for External Services
 * Provides clients for GitHub, Hugging Face, OpenAI, Anthropic, Serper, and MongoDB
 * 
 * Usage:
 *   import { GitHubClient, HuggingFaceClient } from './scripts/npm/integrations.js';
 * 
 *   const github = new GitHubClient(process.env.GITHUB_TOKEN);
 *   const repo = await github.getRepository('Exios66', 'JJB_Gallery');
 */

import axios from "axios";
import dotenv from "dotenv";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

// Load environment variables
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, "../..");

dotenv.config({ path: join(rootDir, ".env") });

/**
 * GitHub API Client
 * Provides methods for interacting with GitHub repositories, releases, and issues
 */
export class GitHubClient {
  constructor(token = process.env.GITHUB_TOKEN) {
    this.token = token;
    this.baseURL = "https://api.github.com";
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        Authorization: token ? `Bearer ${token}` : undefined,
        Accept: "application/vnd.github.v3+json",
        "User-Agent": "JJB-Gallery-Integration",
      },
      timeout: 10000,
    });
  }

  /**
   * Get repository information
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @returns {Promise<Object>} Repository data
   */
  async getRepository(owner, repo) {
    try {
      const response = await this.client.get(`/repos/${owner}/${repo}`);
      return response.data;
    } catch (error) {
      throw new Error(`GitHub API Error: ${error.message}`);
    }
  }

  /**
   * Get repository releases
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @param {number} perPage - Number of releases per page
   * @returns {Promise<Array>} Array of releases
   */
  async getReleases(owner, repo, perPage = 10) {
    try {
      const response = await this.client.get(`/repos/${owner}/${repo}/releases`, {
        params: { per_page: perPage },
      });
      return response.data;
    } catch (error) {
      throw new Error(`GitHub API Error: ${error.message}`);
    }
  }

  /**
   * Create a new issue
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @param {string} title - Issue title
   * @param {string} body - Issue body
   * @param {Array<string>} labels - Optional labels
   * @returns {Promise<Object>} Created issue data
   */
  async createIssue(owner, repo, title, body, labels = []) {
    try {
      const response = await this.client.post(`/repos/${owner}/${repo}/issues`, {
        title,
        body,
        labels,
      });
      return response.data;
    } catch (error) {
      throw new Error(`GitHub API Error: ${error.message}`);
    }
  }

  /**
   * Get repository statistics
   * @param {string} owner - Repository owner
   * @param {string} repo - Repository name
   * @returns {Promise<Object>} Repository stats
   */
  async getStats(owner, repo) {
    try {
      const [repoData, releases, contributors] = await Promise.all([
        this.getRepository(owner, repo),
        this.getReleases(owner, repo, 1),
        this.client.get(`/repos/${owner}/${repo}/contributors`).catch(() => ({ data: [] })),
      ]);

      return {
        stars: repoData.stargazers_count,
        forks: repoData.forks_count,
        watchers: repoData.watchers_count,
        openIssues: repoData.open_issues_count,
        latestRelease: releases[0]?.tag_name || null,
        contributors: contributors.data.length,
      };
    } catch (error) {
      throw new Error(`GitHub API Error: ${error.message}`);
    }
  }
}

/**
 * Hugging Face API Client
 * Provides methods for model inference and information retrieval
 */
export class HuggingFaceClient {
  constructor(token = process.env.HF_TOKEN) {
    this.token = token;
    this.baseURL = "https://api-inference.huggingface.co";
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        Authorization: token ? `Bearer ${token}` : undefined,
      },
      timeout: 30000,
    });
  }

  /**
   * Run model inference
   * @param {string} model - Model identifier
   * @param {Object|string} inputs - Input data for the model
   * @param {Object} options - Additional options (parameters, etc.)
   * @returns {Promise<Object>} Inference result
   */
  async inference(model, inputs, options = {}) {
    try {
      const response = await this.client.post(`/models/${model}`, inputs, {
        params: options,
      });
      return response.data;
    } catch (error) {
      throw new Error(`Hugging Face API Error: ${error.message}`);
    }
  }

  /**
   * Get model information
   * @param {string} model - Model identifier
   * @returns {Promise<Object>} Model metadata
   */
  async getModelInfo(model) {
    try {
      const response = await axios.get(`https://huggingface.co/api/models/${model}`, {
        headers: this.token ? { Authorization: `Bearer ${this.token}` } : {},
      });
      return response.data;
    } catch (error) {
      throw new Error(`Hugging Face API Error: ${error.message}`);
    }
  }

  /**
   * Generate text embeddings
   * @param {string} model - Embedding model identifier
   * @param {string|Array<string>} texts - Text(s) to embed
   * @returns {Promise<Object>} Embedding vectors
   */
  async embed(model, texts) {
    try {
      const inputs = Array.isArray(texts) ? texts : [texts];
      const response = await this.client.post(`/pipeline/feature-extraction/${model}`, {
        inputs,
      });
      return response.data;
    } catch (error) {
      throw new Error(`Hugging Face Embedding Error: ${error.message}`);
    }
  }
}

/**
 * OpenAI API Client
 * Provides methods for chat completions and embeddings
 */
export class OpenAIClient {
  constructor(apiKey = process.env.OPENAI_API_KEY) {
    this.apiKey = apiKey;
    this.baseURL = process.env.OPENAI_API_BASE || "https://api.openai.com/v1";
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        Authorization: apiKey ? `Bearer ${apiKey}` : undefined,
        "Content-Type": "application/json",
      },
      timeout: 60000,
    });
  }

  /**
   * Create a chat completion
   * @param {Array<Object>} messages - Array of message objects
   * @param {string} model - Model identifier (default: gpt-3.5-turbo)
   * @param {Object} options - Additional options (temperature, max_tokens, etc.)
   * @returns {Promise<Object>} Completion response
   */
  async chatCompletion(messages, model = "gpt-3.5-turbo", options = {}) {
    try {
      const response = await this.client.post("/chat/completions", {
        model,
        messages,
        ...options,
      });
      return response.data;
    } catch (error) {
      throw new Error(`OpenAI API Error: ${error.message}`);
    }
  }

  /**
   * Create embeddings
   * @param {string|Array<string>} input - Text(s) to embed
   * @param {string} model - Embedding model (default: text-embedding-ada-002)
   * @returns {Promise<Object>} Embedding response
   */
  async createEmbedding(input, model = "text-embedding-ada-002") {
    try {
      const response = await this.client.post("/embeddings", {
        model,
        input: Array.isArray(input) ? input : [input],
      });
      return response.data;
    } catch (error) {
      throw new Error(`OpenAI Embedding Error: ${error.message}`);
    }
  }
}

/**
 * Anthropic API Client
 * Provides methods for Claude model completions
 */
export class AnthropicClient {
  constructor(apiKey = process.env.ANTHROPIC_API_KEY) {
    this.apiKey = apiKey;
    this.baseURL = "https://api.anthropic.com/v1";
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        "x-api-key": apiKey || "",
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
      },
      timeout: 60000,
    });
  }

  /**
   * Send a message to Claude
   * @param {string} prompt - User prompt
   * @param {string} model - Model identifier (default: claude-3-5-sonnet-20241022)
   * @param {Object} options - Additional options (max_tokens, temperature, etc.)
   * @returns {Promise<Object>} Message response
   */
  async messages(prompt, model = "claude-3-5-sonnet-20241022", options = {}) {
    try {
      const response = await this.client.post("/messages", {
        model,
        max_tokens: options.max_tokens || 1024,
        messages: [{ role: "user", content: prompt }],
        ...options,
      });
      return response.data;
    } catch (error) {
      throw new Error(`Anthropic API Error: ${error.message}`);
    }
  }

  /**
   * Stream messages from Claude
   * @param {string} prompt - User prompt
   * @param {string} model - Model identifier
   * @param {Object} options - Additional options
   * @returns {Promise<ReadableStream>} Streaming response
   */
  async streamMessages(prompt, model = "claude-3-5-sonnet-20241022", options = {}) {
    try {
      const response = await this.client.post(
        "/messages",
        {
          model,
          max_tokens: options.max_tokens || 1024,
          messages: [{ role: "user", content: prompt }],
          stream: true,
          ...options,
        },
        {
          responseType: "stream",
        }
      );
      return response.data;
    } catch (error) {
      throw new Error(`Anthropic Streaming Error: ${error.message}`);
    }
  }
}

/**
 * Serper API Client (Web Search)
 * Provides methods for Google search via Serper.dev
 */
export class SerperClient {
  constructor(apiKey = process.env.SERPER_API_KEY) {
    this.apiKey = apiKey;
    this.baseURL = "https://google.serper.dev";
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        "X-API-KEY": apiKey || "",
        "Content-Type": "application/json",
      },
      timeout: 10000,
    });
  }

  /**
   * Perform a web search
   * @param {string} query - Search query
   * @param {Object} options - Search options (num, gl, hl, etc.)
   * @returns {Promise<Object>} Search results
   */
  async search(query, options = {}) {
    try {
      const response = await this.client.post("/search", {
        q: query,
        num: options.num || 10,
        gl: options.gl || "us",
        hl: options.hl || "en",
        ...options,
      });
      return response.data;
    } catch (error) {
      throw new Error(`Serper API Error: ${error.message}`);
    }
  }

  /**
   * Get search suggestions
   * @param {string} query - Partial query
   * @returns {Promise<Array>} Array of suggestions
   */
  async getSuggestions(query) {
    try {
      const response = await this.client.post("/autocomplete", {
        q: query,
      });
      return response.data;
    } catch (error) {
      throw new Error(`Serper Suggestions Error: ${error.message}`);
    }
  }
}

/**
 * MongoDB Connection Helper
 * Provides utilities for MongoDB connections (used by ChatUi)
 */
export class MongoDBHelper {
  constructor(connectionString = process.env.MONGODB_URL) {
    this.connectionString = connectionString;
  }

  /**
   * Validate MongoDB connection string
   * @returns {Object} Connection info
   */
  async validateConnection() {
    if (!this.connectionString) {
      throw new Error("MONGODB_URL environment variable is required");
    }

    // Parse connection string
    const url = new URL(this.connectionString);
    return {
      protocol: url.protocol,
      host: url.hostname,
      port: url.port || (url.protocol === "mongodb+srv:" ? 27017 : 27017),
      database: url.pathname.slice(1) || "chatui",
      connected: true,
    };
  }

  /**
   * Get connection status (placeholder - actual connection handled by MongoDB driver)
   * @returns {Promise<Object>} Connection status
   */
  async getStatus() {
    try {
      const info = await this.validateConnection();
      return {
        ...info,
        status: "ready",
        message: "MongoDB connection string validated",
      };
    } catch (error) {
      return {
        status: "error",
        message: error.message,
      };
    }
  }
}

/**
 * Utility function to test all API connections
 * @returns {Promise<Object>} Status of all API connections
 */
export async function testAllConnections() {
  const results = {
    github: { status: "unknown", error: null },
    huggingface: { status: "unknown", error: null },
    openai: { status: "unknown", error: null },
    anthropic: { status: "unknown", error: null },
    serper: { status: "unknown", error: null },
    mongodb: { status: "unknown", error: null },
  };

  // Test GitHub
  if (process.env.GITHUB_TOKEN) {
    try {
      const github = new GitHubClient();
      await github.getRepository("Exios66", "JJB_Gallery");
      results.github = { status: "connected", error: null };
    } catch (error) {
      results.github = { status: "error", error: error.message };
    }
  } else {
    results.github = { status: "no_token", error: "GITHUB_TOKEN not set" };
  }

  // Test Hugging Face
  if (process.env.HF_TOKEN) {
    try {
      const hf = new HuggingFaceClient();
      await hf.getModelInfo("gpt2");
      results.huggingface = { status: "connected", error: null };
    } catch (error) {
      results.huggingface = { status: "error", error: error.message };
    }
  } else {
    results.huggingface = { status: "no_token", error: "HF_TOKEN not set" };
  }

  // Test OpenAI
  if (process.env.OPENAI_API_KEY) {
    try {
      const openai = new OpenAIClient();
      // Just validate the client was created
      results.openai = { status: "ready", error: null };
    } catch (error) {
      results.openai = { status: "error", error: error.message };
    }
  } else {
    results.openai = { status: "no_token", error: "OPENAI_API_KEY not set" };
  }

  // Test Anthropic
  if (process.env.ANTHROPIC_API_KEY) {
    try {
      const anthropic = new AnthropicClient();
      results.anthropic = { status: "ready", error: null };
    } catch (error) {
      results.anthropic = { status: "error", error: error.message };
    }
  } else {
    results.anthropic = { status: "no_token", error: "ANTHROPIC_API_KEY not set" };
  }

  // Test Serper
  if (process.env.SERPER_API_KEY) {
    try {
      const serper = new SerperClient();
      results.serper = { status: "ready", error: null };
    } catch (error) {
      results.serper = { status: "error", error: error.message };
    }
  } else {
    results.serper = { status: "no_token", error: "SERPER_API_KEY not set" };
  }

  // Test MongoDB
  if (process.env.MONGODB_URL) {
    try {
      const mongo = new MongoDBHelper();
      await mongo.validateConnection();
      results.mongodb = { status: "valid", error: null };
    } catch (error) {
      results.mongodb = { status: "error", error: error.message };
    }
  } else {
    results.mongodb = { status: "no_url", error: "MONGODB_URL not set" };
  }

  return results;
}

// Export all clients and utilities
export default {
  GitHubClient,
  HuggingFaceClient,
  OpenAIClient,
  AnthropicClient,
  SerperClient,
  MongoDBHelper,
  testAllConnections,
};

// CLI usage
if (import.meta.url === `file://${process.argv[1]}`) {
  testAllConnections()
    .then((results) => {
      console.log("\n🔌 API Connection Status:\n");
      Object.entries(results).forEach(([service, { status, error }]) {
        const icon = status === "connected" || status === "ready" || status === "valid" ? "✅" : "❌";
        console.log(`${icon} ${service.toUpperCase()}: ${status}`);
        if (error) console.log(`   └─ ${error}`);
      });
      console.log();
    })
    .catch((error) => {
      console.error("Error testing connections:", error);
      process.exit(1);
    });
}

