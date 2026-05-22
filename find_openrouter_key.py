import json
import re

transcript_path = r"C:\Users\Windows\.gemini\antigravity\brain\1c57d74e-24ed-4701-b775-c051cc646a3b\.system_generated\logs\transcript.jsonl"

print("Searching transcript for OpenRouter API Key...")
pattern = re.compile(r"sk-or-v1-[a-zA-Z0-9_\-]+")

with open(transcript_path, "r", encoding="utf-8") as f:
    for line_num, line in enumerate(f, 1):
        try:
            data = json.loads(line)
            content = data.get("content", "")
            if not content and "tool_calls" in data:
                content = str(data["tool_calls"])
            
            matches = pattern.findall(str(content))
            if matches:
                print(f"Line {line_num} (Source: {data.get('source')}): {matches}")
        except Exception as e:
            pass
