import dotenv from "dotenv";
dotenv.config();

import * as composioCore from "@composio/core";

const allExports = Object.keys(composioCore);
console.log("Composio core all exports count:", allExports.length);

// Search for any tool related class or function
const toolExports = allExports.filter(k => k.toLowerCase().includes("tool"));
console.log("Tool related exports:", toolExports);

const comp = new composioCore.Composio();
console.log("\nComposio class methods:", Object.getOwnPropertyNames(Object.getPrototypeOf(comp)));
console.log("Composio instance properties:", Object.keys(comp));

// Try to print functions of Composio instance
for (const key of Object.keys(comp)) {
  const val = (comp as any)[key];
  if (val && typeof val === 'object') {
    console.log(`\nProperty: ${key} | methods:`, Object.getOwnPropertyNames(Object.getPrototypeOf(val)));
  }
}
