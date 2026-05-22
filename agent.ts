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
      headers: {
        "HTTP-Referer": "https://github.com/khoahocaiedu/composio",
        "X-Title": "Composio Agent Console",
      }
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
    system: "Bạn là một AI Agent đàm thoại chạy trực tiếp bằng mô hình 'openrouter/auto' và được tích hợp với các công cụ của Composio thông qua giao thức MCP. Hiện tại bạn đang kết nối trực tiếp với Composio và đã tải các công cụ thành công. Khi người dùng hỏi 'Làm sao tôi biết bạn đã kết nối đến composio' hoặc các câu hỏi tương tự về kết nối, bạn hãy trả lời xác nhận ngay rằng bạn đã kết nối thành công và sẵn sàng hoạt động (vì bạn đang có sẵn danh sách công cụ được tải trực tiếp từ Composio). Bạn KHÔNG CẦN gọi bất kỳ công cụ tìm kiếm hay công cụ kiểm tra kết nối nào của Composio để xác thực lại, hãy trả lời thẳng câu hỏi của người dùng và liệt kê ngắn gọn các ứng dụng bạn đang kết nối (ví dụ: GitHub, Google Drive, Facebook Page, Gmail). Nếu người dùng yêu cầu thực hiện một tác vụ cụ thể mà cần dùng công cụ, hãy gọi công cụ tương ứng, nhận kết quả, sau đó đưa ra câu trả lời hoàn chỉnh dựa trên kết quả đó.",
    prompt: "Star the composiohq/composio repo on GitHub",
    maxSteps: 10,
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
