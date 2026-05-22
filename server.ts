import dotenv from "dotenv";
dotenv.config({ override: true });

import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import handler from "./api/agent.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());

// Phục vụ giao diện tĩnh index.html ở thư mục gốc
app.use(express.static(__dirname));

// Route API chuyển tiếp cuộc gọi đến Vercel Serverless Handler
app.post("/api/agent", async (req, res) => {
  try {
    await handler(req, res);
  } catch (error) {
    console.error("Lỗi khi xử lý API qua Express:", error);
    if (!res.headersSent) {
      res.status(500).json({ error: "Internal Server Error" });
    }
  }
});

app.listen(port, () => {
  console.log(`\n🚀 Server đang chạy tại: http://localhost:${port}`);
  console.log(`💡 Mẹo: Bạn có thể truy cập địa chỉ này để chạy Agent không bị giới hạn 10 giây!\n`);
});
