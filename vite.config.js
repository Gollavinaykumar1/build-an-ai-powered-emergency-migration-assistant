import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/build-an-ai-powered-emergency-migration-assistant/",
  build: { outDir: "dist", assetsDir: "assets" },
  server: { port: 3000 },
});
