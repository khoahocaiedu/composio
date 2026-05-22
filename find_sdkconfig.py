import os
import sys

site_packages = None
for path in sys.path:
    if "site-packages" in path:
        site_packages = path
        break

if site_packages:
    composio_path = os.path.join(site_packages, "composio")
    print("Searching in:", composio_path)
    for root, dirs, files in os.walk(composio_path):
        for f in files:
            if f.endswith(".py"):
                fp = os.path.join(root, f)
                try:
                    with open(fp, "r", encoding="utf-8") as file:
                        content = file.read()
                        if "class SDKConfig" in content or "SDKConfig = " in content:
                            print(f"Found SDKConfig in: {fp}")
                            # print the lines around it
                            lines = content.splitlines()
                            for i, line in enumerate(lines):
                                if "SDKConfig" in line:
                                    start = max(0, i - 2)
                                    end = min(len(lines), i + 15)
                                    print(f"--- lines {start} to {end} in {f} ---")
                                    for idx in range(start, end):
                                        print(f"{idx}: {lines[idx]}")
                except Exception:
                    pass
else:
    print("site-packages not found in path")
