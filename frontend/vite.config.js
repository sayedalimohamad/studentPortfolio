import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";
import { execSync } from "child_process";

function getLocalIPv4() {
  const output = execSync("ipconfig").toString();
  const lines = output.split("\n");
  for (let line of lines) {
    if (line.includes("IPv4 Address")) {
      return line.split(":")[1].trim();
    }
  }
  return null;
}

const localIPv4 = getLocalIPv4();


export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    host: true,
    proxy: {
      "/api": {
        target: `http://${localIPv4}:5000`, // Flask backend URL
        changeOrigin: true,
        secure: false,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
  },
});

