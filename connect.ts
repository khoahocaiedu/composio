import dotenv from "dotenv";
dotenv.config({ override: true });

import { Composio } from "@composio/core";

async function main() {
  console.log("Initializing Composio with new API key...");
  const composio = new Composio();

  console.log("Creating session with specified toolkits...");
  const session = await composio.create("pg-test-f88a0cbe-fcae-46a0-b516-4204597f4607", {
    toolkits: [
      "gmail",
      "composio",
      "github",
      "googlecalendar",
      "googlesheets",
      "googledrive",
      "youtube",
      "facebook",
      "openrouter"
    ],
    manageConnections: {
      waitForConnections: true
    },
  });

  console.log("Session created successfully!");
  console.log("Session ID:", session.sessionId);
  console.log("MCP Url:", session.mcp.url);
}

main().catch(console.error);
