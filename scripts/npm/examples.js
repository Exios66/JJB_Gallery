#!/usr/bin/env node
/**
 * Example Usage of API Integration Clients
 * 
 * Run with: node scripts/npm/examples.js
 * 
 * Make sure to set environment variables:
 *   - GITHUB_TOKEN
 *   - HF_TOKEN
 *   - OPENAI_API_KEY
 *   - ANTHROPIC_API_KEY
 *   - SERPER_API_KEY
 *   - MONGODB_URL
 */

import {
  GitHubClient,
  HuggingFaceClient,
  OpenAIClient,
  AnthropicClient,
  SerperClient,
  MongoDBHelper,
  testAllConnections,
} from "./integrations.js";
import dotenv from "dotenv";

dotenv.config();

// Example 1: GitHub Repository Information
async function exampleGitHub() {
  console.log("\n📦 Example 1: GitHub Repository Info\n");
  
  if (!process.env.GITHUB_TOKEN) {
    console.log("⚠️  GITHUB_TOKEN not set, skipping GitHub example");
    return;
  }

  try {
    const github = new GitHubClient();
    
    // Get repository information
    const repo = await github.getRepository("Exios66", "JJB_Gallery");
    console.log(`Repository: ${repo.full_name}`);
    console.log(`Description: ${repo.description}`);
    console.log(`Stars: ${repo.stargazers_count}`);
    console.log(`Forks: ${repo.forks_count}`);
    
    // Get repository statistics
    const stats = await github.getStats("Exios66", "JJB_Gallery");
    console.log("\n📊 Repository Statistics:");
    console.log(JSON.stringify(stats, null, 2));
    
    // Get latest releases
    const releases = await github.getReleases("Exios66", "JJB_Gallery", 3);
    console.log("\n🏷️  Latest Releases:");
    releases.forEach((release) => {
      console.log(`  - ${release.tag_name}: ${release.name}`);
    });
  } catch (error) {
    console.error("❌ GitHub Error:", error.message);
  }
}

// Example 2: Hugging Face Model Inference
async function exampleHuggingFace() {
  console.log("\n🤗 Example 2: Hugging Face Model\n");
  
  if (!process.env.HF_TOKEN) {
    console.log("⚠️  HF_TOKEN not set, skipping Hugging Face example");
    return;
  }

  try {
    const hf = new HuggingFaceClient();
    
    // Get model information
    const modelInfo = await hf.getModelInfo("gpt2");
    console.log(`Model: ${modelInfo.modelId}`);
    console.log(`Downloads: ${modelInfo.downloads || "N/A"}`);
    
    // Simple text generation (if model supports it)
    console.log("\n💬 Running inference...");
    const result = await hf.inference("gpt2", "Hello, my name is");
    console.log("Result:", JSON.stringify(result, null, 2).substring(0, 200) + "...");
  } catch (error) {
    console.error("❌ Hugging Face Error:", error.message);
  }
}

// Example 3: OpenAI Chat Completion
async function exampleOpenAI() {
  console.log("\n🤖 Example 3: OpenAI Chat Completion\n");
  
  if (!process.env.OPENAI_API_KEY) {
    console.log("⚠️  OPENAI_API_KEY not set, skipping OpenAI example");
    return;
  }

  try {
    const openai = new OpenAIClient();
    
    const messages = [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "What is the capital of France? Answer in one sentence." },
    ];
    
    console.log("💬 Sending chat completion request...");
    const response = await openai.chatCompletion(messages, "gpt-3.5-turbo", {
      temperature: 0.7,
      max_tokens: 100,
    });
    
    console.log("Response:", response.choices[0].message.content);
  } catch (error) {
    console.error("❌ OpenAI Error:", error.message);
  }
}

// Example 4: Anthropic Claude
async function exampleAnthropic() {
  console.log("\n🧠 Example 4: Anthropic Claude\n");
  
  if (!process.env.ANTHROPIC_API_KEY) {
    console.log("⚠️  ANTHROPIC_API_KEY not set, skipping Anthropic example");
    return;
  }

  try {
    const anthropic = new AnthropicClient();
    
    console.log("💬 Sending message to Claude...");
    const response = await anthropic.messages(
      "Explain quantum computing in one sentence.",
      "claude-3-5-sonnet-20241022",
      { max_tokens: 100 }
    );
    
    console.log("Response:", response.content[0].text);
  } catch (error) {
    console.error("❌ Anthropic Error:", error.message);
  }
}

// Example 5: Serper Web Search
async function exampleSerper() {
  console.log("\n🔍 Example 5: Serper Web Search\n");
  
  if (!process.env.SERPER_API_KEY) {
    console.log("⚠️  SERPER_API_KEY not set, skipping Serper example");
    return;
  }

  try {
    const serper = new SerperClient();
    
    console.log("🔍 Searching for 'machine learning'...");
    const results = await serper.search("machine learning", { num: 3 });
    
    console.log(`Found ${results.organic?.length || 0} results:`);
    results.organic?.slice(0, 3).forEach((result, index) => {
      console.log(`\n${index + 1}. ${result.title}`);
      console.log(`   ${result.link}`);
      console.log(`   ${result.snippet?.substring(0, 100)}...`);
    });
  } catch (error) {
    console.error("❌ Serper Error:", error.message);
  }
}

// Example 6: MongoDB Connection
async function exampleMongoDB() {
  console.log("\n🍃 Example 6: MongoDB Connection\n");
  
  if (!process.env.MONGODB_URL) {
    console.log("⚠️  MONGODB_URL not set, skipping MongoDB example");
    return;
  }

  try {
    const mongo = new MongoDBHelper();
    const status = await mongo.getStatus();
    
    console.log("MongoDB Connection Status:");
    console.log(JSON.stringify(status, null, 2));
  } catch (error) {
    console.error("❌ MongoDB Error:", error.message);
  }
}

// Example 7: Test All Connections
async function exampleTestAll() {
  console.log("\n🔌 Example 7: Test All API Connections\n");
  
  const results = await testAllConnections();
  
  console.log("Connection Status:");
  Object.entries(results).forEach(([service, { status, error }]) {
    const icon = status === "connected" || status === "ready" || status === "valid" ? "✅" : 
                 status === "no_token" || status === "no_url" ? "⚠️ " : "❌";
    console.log(`${icon} ${service.toUpperCase()}: ${status}`);
    if (error) {
      console.log(`   └─ ${error}`);
    }
  });
}

// Main execution
async function main() {
  console.log("🚀 API Integration Examples\n");
  console.log("=" .repeat(50));
  
  // Run all examples
  await exampleGitHub();
  await exampleHuggingFace();
  await exampleOpenAI();
  await exampleAnthropic();
  await exampleSerper();
  await exampleMongoDB();
  await exampleTestAll();
  
  console.log("\n" + "=".repeat(50));
  console.log("✅ Examples completed!");
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
  });
}

export {
  exampleGitHub,
  exampleHuggingFace,
  exampleOpenAI,
  exampleAnthropic,
  exampleSerper,
  exampleMongoDB,
  exampleTestAll,
};

