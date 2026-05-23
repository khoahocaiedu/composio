import dotenv from "dotenv";
dotenv.config();

import { createAnthropic } from "@ai-sdk/anthropic";
import { createOpenAI } from "@ai-sdk/openai";
import { Composio } from "@composio/core";
import { streamText, stepCountIs } from "ai";
import { experimental_createMCPClient as createMCPClient } from "@ai-sdk/mcp";

// Cấu hình Vercel Serverless
export const config = {
  maxDuration: 60, // Hỗ trợ chạy tối đa 60 giây trên Vercel
};

// Hàm lấy model AI, kiểm tra biến môi trường động
function getAiModel() {
  const useAnthropic = !!process.env.ANTHROPIC_API_KEY;

  if (useAnthropic) {
    const anthropicProvider = createAnthropic({ apiKey: process.env.ANTHROPIC_API_KEY as string });
    return anthropicProvider("claude-3-5-sonnet-latest");
  } else {
    const openrouterKey = process.env.OPENROUTER_API_KEY;
    if (!openrouterKey) {
      throw new Error(
        "Thiếu biến môi trường OPENROUTER_API_KEY. Vui lòng thêm OPENROUTER_API_KEY trong Cấu hình Biến môi trường (Environment Variables) trên Vercel Dashboard của bạn, sau đó thực hiện Redeploy dự án để áp dụng."
      );
    }
    
    const openrouterProvider = createOpenAI({
      baseURL: "https://openrouter.ai/api/v1",
      apiKey: openrouterKey,
      headers: {
        "HTTP-Referer": "https://github.com/khoahocaiedu/composio",
        "X-Title": "Composio Agent Console",
      }
    });
    
    // Sử dụng model tự động định tuyến của OpenRouter
    return openrouterProvider.chat("openrouter/auto");
  }
}


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
    // Kiểm tra các biến môi trường trước khi thực thi
    if (!process.env.COMPOSIO_API_KEY) {
      throw new Error(
        "Thiếu biến môi trường COMPOSIO_API_KEY. Vui lòng thêm COMPOSIO_API_KEY trong Cấu hình Biến môi trường (Environment Variables) trên Vercel Dashboard của bạn, sau đó thực hiện Redeploy dự án để áp dụng."
      );
    }
    const useAnthropic = !!process.env.ANTHROPIC_API_KEY;
    if (!useAnthropic && !process.env.OPENROUTER_API_KEY) {
      throw new Error(
        "Thiếu biến môi trường OPENROUTER_API_KEY. Vui lòng thêm OPENROUTER_API_KEY trong Cấu hình Biến môi trường (Environment Variables) trên Vercel Dashboard của bạn, sau đó thực hiện Redeploy dự án để áp dụng."
      );
    }

    if (!cachedTools) {
      sendEvent("log", { message: "Khởi tạo session Composio Cloud..." });
      const composio = new Composio();
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
      model: getAiModel(),
      system: `Bạn là một AI Agent thông minh được tích hợp Composio qua MCP. Bạn có 6 meta-tools:
- COMPOSIO_SEARCH_TOOLS: Tìm tool phù hợp với tác vụ
- COMPOSIO_GET_TOOL_SCHEMAS: Lấy schema chi tiết của tool
- COMPOSIO_MULTI_EXECUTE_TOOL: Thực thi tool (đây là tool QUAN TRỌNG NHẤT)
- COMPOSIO_MANAGE_CONNECTIONS: Quản lý kết nối apps
- COMPOSIO_REMOTE_BASH_TOOL: Chạy lệnh bash
- COMPOSIO_REMOTE_WORKBENCH: IDE workspace

CÁC ỨNG DỤNG ĐÃ KẾT NỐI: GitHub, Google Drive, Facebook Page, Gmail.

QUY TRÌNH BẮT BUỘC khi người dùng yêu cầu tác vụ (ví dụ đọc email, post Facebook, star repo):
1. Gọi COMPOSIO_SEARCH_TOOLS để tìm tool slug phù hợp
2. Dùng kết quả trả về, NGAY LẬP TỨC gọi COMPOSIO_MULTI_EXECUTE_TOOL với tool slug và arguments đúng
3. Đọc kết quả và trả lời người dùng bằng tiếng Việt

LƯU Ý QUAN TRỌNG:
- KHÔNG BAO GIỜ dừng lại sau bước tìm kiếm. Luôn thực thi tool sau khi tìm được.
- Khi lấy nội dung email chi tiết (ví dụ dùng GMAIL_FETCH_MESSAGE_BY_MESSAGE_ID), luôn truyền tham số format: "metadata" (chỉ lấy subject, snippet và headers) để tránh làm tràn giới hạn token của context.
- Khi hỏi về kết nối Composio, trả lời ngay rằng đã kết nối thành công với GitHub, Google Drive, Facebook, Gmail.
- Luôn trả lời bằng tiếng Việt.
- Nếu tool trả về lỗi, giải thích rõ ràng cho người dùng.`,
      prompt: prompt,
      tools: cachedTools,
      maxSteps: 15,
      stopWhen: stepCountIs(15),
    } as any);

    for await (const chunk of result.fullStream) {
      console.log(`[AGENT CHUNK] type=${chunk.type}`, chunk.type === "text-delta" ? chunk.text : (chunk.type === "tool-call" || chunk.type === "tool-result" ? JSON.stringify(chunk) : ""));
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
