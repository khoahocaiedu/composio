import dotenv from "dotenv";
dotenv.config();

import { createAnthropic } from "@ai-sdk/anthropic";
import { createOpenAI } from "@ai-sdk/openai";
import { Composio } from "@composio/core";
import { streamText } from "ai";
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
    
    // Sử dụng model tự động định tuyến miễn phí của OpenRouter
    return openrouterProvider.chat("openrouter/free");
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
      model: getAiModel(),
      system: "Bạn là một AI Agent đàm thoại chạy trực tiếp bằng mô hình 'openrouter/auto' và được tích hợp với các công cụ của Composio thông qua giao thức MCP. Hiện tại bạn đang kết nối trực tiếp với Composio và đã tải các công cụ thành công. Khi người dùng hỏi 'Làm sao tôi biết bạn đã kết nối đến composio' hoặc các câu hỏi tương tự về kết nối, bạn hãy trả lời xác nhận ngay rằng bạn đã kết nối thành công và sẵn sàng hoạt động (vì bạn đang có sẵn danh sách công cụ được tải trực tiếp từ Composio). Bạn KHÔNG CẦN gọi bất kỳ công cụ tìm kiếm hay công cụ kiểm tra kết nối nào của Composio để xác thực lại, hãy trả lời thẳng câu hỏi của người dùng và liệt kê ngắn gọn các ứng dụng bạn đang kết nối (ví dụ: GitHub, Google Drive, Facebook Page, Gmail). Nếu người dùng yêu cầu thực hiện một tác vụ cụ thể mà cần dùng công cụ, hãy gọi công cụ tương ứng, nhận kết quả, sau đó đưa ra câu trả lời hoàn chỉnh dựa trên kết quả đó.",
      prompt: prompt,
      tools: cachedTools,
      maxSteps: 10,
    } as any);

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
