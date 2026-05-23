import dotenv from "dotenv";
dotenv.config({ override: true });

import { createAnthropic } from "@ai-sdk/anthropic";
import { createOpenAI } from "@ai-sdk/openai";
import { Composio } from "@composio/core";
import { stepCountIs, streamText } from "ai";
import { experimental_createMCPClient as createMCPClient } from "@ai-sdk/mcp";

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
        "Thiếu biến môi trường OPENROUTER_API_KEY. Vui lòng thêm OPENROUTER_API_KEY trong file .env."
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

const composio = new Composio();

async function main() {
  console.log("Khởi tạo session Composio...");
  // Create a tool router session
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
    prompt: "Star the composiohq/composio repo on GitHub",
    maxSteps: 15,
    stopWhen: stepCountIs(15),
    tools,
  } as any);

  for await (const textPart of stream.textStream) {
    process.stdout.write(textPart);
  }
  console.log("\n[Hoàn thành thực thi]");
}

main().catch((err) => {
  console.error("Lỗi khi thực thi agent:", err);
});
