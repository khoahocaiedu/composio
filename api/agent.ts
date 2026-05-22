import { createAnthropic } from "@ai-sdk/anthropic";
import { createOpenAI } from "@ai-sdk/openai";
import { Composio } from "@composio/core";
import { streamText } from "ai";
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

const anthropicModel = (modelName: string) => {
  if (useAnthropic) {
    const realModelName = modelName === "claude-sonnet-4-6" ? "claude-3-5-sonnet-latest" : modelName;
    return anthropicProvider!(realModelName);
  } else {
    // Sử dụng model tự động định tuyến của OpenRouter
    return openrouterProvider!.chat("openrouter/auto");
  }
};

export const config = {
  maxDuration: 60, // Hỗ trợ chạy tối đa 60 giây trên Vercel
};

// Caching biến toàn cục để tái sử dụng giữa các lần gọi (Warm Start)
let cachedTools: any = null;
let cachedToolCount = 0;

export default async function handler(req: any, res: any) {
  // Chỉ chấp nhận phương thức POST
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed. Use POST." });
    return;
  }

  const { prompt, refresh } = req.body;
  if (!prompt) {
    res.status(400).json({ error: "Missing prompt in request body." });
    return;
  }

  if (refresh) {
    cachedTools = null;
    cachedToolCount = 0;
  }

  // Thiết lập Server-Sent Events (SSE) để stream dữ liệu về Client
  res.writeHead(200, {
    "Content-Type": "text/event-stream",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
  });

  const sendEvent = (type: string, data: any) => {
    res.write(`data: ${JSON.stringify({ type, ...data })}\n\n`);
  };

  try {
    if (!cachedTools) {
      sendEvent("log", { message: "Khởi tạo session Composio Cloud..." });
      const composio = new Composio();
      const userId = "user_jrw3p7i";
      const session = await composio.create(userId);

      sendEvent("log", { message: "Đang kết nối đến Composio MCP Server..." });
      const transport: any = {
        type: session.mcp.type,
        url: session.mcp.url,
      };
      if (session.mcp.headers) {
        transport.headers = session.mcp.headers;
      }
      const client = await createMCPClient({ transport });

      sendEvent("log", { message: "Đang tải danh sách công cụ..." });
      cachedTools = await client.tools();
      cachedToolCount = Object.keys(cachedTools).length;
      sendEvent("log", { message: `Đã tải thành công ${cachedToolCount} công cụ.` });
    } else {
      sendEvent("log", { message: `Sử dụng ${cachedToolCount} công cụ từ bộ nhớ đệm (Cache).` });
    }

    sendEvent("log", { message: "Đang kích hoạt mô hình AI và thực thi tác vụ..." });

    const result = await streamText({
      model: anthropicModel("claude-sonnet-4-6"),
      prompt: prompt,
      tools: cachedTools,
    });

    for await (const chunk of result.fullStream) {
      if (chunk.type === "text-delta") {
        sendEvent("text", { content: chunk.text });
      } else if (chunk.type === "tool-call") {
        const args = (chunk as any).args !== undefined ? (chunk as any).args : ((chunk as any).input !== undefined ? (chunk as any).input : {});
        sendEvent("tool-call", {
          toolName: chunk.toolName,
          args: args,
        });
      } else if (chunk.type === "tool-result") {
        const resultVal = (chunk as any).result !== undefined ? (chunk as any).result : ((chunk as any).output !== undefined ? (chunk as any).output : {});
        sendEvent("tool-result", {
          toolName: chunk.toolName,
          result: resultVal,
        });
      }
    }

    sendEvent("done", { message: "Hoàn thành thực thi." });
  } catch (error: any) {
    console.error("Lỗi thực thi Agent:", error);
    sendEvent("error", { message: error.message || "Đã xảy ra lỗi hệ thống." });
  } finally {
    res.end();
  }
}
