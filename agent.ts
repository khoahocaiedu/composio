import dotenv from "dotenv";
dotenv.config({ override: true });

import { createAnthropic } from "@ai-sdk/anthropic";
import { createOpenAI } from "@ai-sdk/openai";
import { Composio } from "@composio/core";
import { stepCountIs, streamText } from "ai";
import { experimental_createMCPClient as createMCPClient } from "@ai-sdk/mcp";

// Tự động kiểm tra và cấu hình provider thích hợp
const useAnthropic = !!process.env.ANTHROPIC_API_KEY;

const anthropicProvider = useAnthropic
  ? createAnthropic({ apiKey: process.env.ANTHROPIC_API_KEY as string })
  : null;

const openrouterProvider = !useAnthropic
  ? createOpenAI({
      baseURL: "https://openrouter.ai/api/v1",
      apiKey: (process.env.OPENROUTER_API_KEY || "") as string,
    })
  : null;

// Hàm wrapper để tương thích hoàn toàn với cú pháp model: anthropic("claude-sonnet-4-6") của bạn
const anthropic = (modelName: string) => {
  if (useAnthropic) {
    const realModelName = modelName === "claude-sonnet-4-6" ? "claude-3-5-sonnet-latest" : modelName;
    return anthropicProvider!(realModelName);
  } else {
    // Sử dụng model tự động định tuyến của OpenRouter để tự động dùng mô hình được cấu hình trong Key Limits của bạn
    return openrouterProvider!.chat("openrouter/auto");
  }
};

const composio = new Composio();
const userId = "user_jrw3p7i";

async function main() {
  console.log("Khởi tạo session Composio...");
  // Create a tool router session
  const session = await composio.create(userId);

  console.log("Kết nối đến MCP Server...");
  // Connect to MCP server and get tools
  const transport: any = {
    type: session.mcp.type,
    url: session.mcp.url,
  };
  if (session.mcp.headers) {
    transport.headers = session.mcp.headers;
  }
  const client = await createMCPClient({ transport });

  console.log("Tải danh sách công cụ (tools)...");
  const tools = await client.tools();
  console.log(`Đã tải thành công ${Object.keys(tools).length} công cụ.`);

  console.log("Đang bắt đầu thực thi agent...");
  const stream = await streamText({
    model: anthropic("claude-sonnet-4-6"),
    prompt: "Star the composiohq/composio repo on GitHub",
    stopWhen: stepCountIs(10),
    tools,
  });

  for await (const textPart of stream.textStream) {
    process.stdout.write(textPart);
  }
  console.log("\n[Hoàn thành thực thi]");
}

main().catch((err) => {
  console.error("Lỗi khi thực thi agent:", err);
});
