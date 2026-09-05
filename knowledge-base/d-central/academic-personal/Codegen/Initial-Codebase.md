---
source_project: Codegen
source_project_uuid: 6b12c781-6b8b-4b85-a073-f5f3ed19c1c9
doc_uuid: 0475c048-7b6f-494e-8dbb-bb7da3c5d189
original_filename: Initial Codebase
created_at: 2025-03-24T22:19:00.978425+00:00
content_hash: ab136175edc4
---

I'll create a complete folder structure for you to run the program locally without CORS issues. This approach uses a simple Node.js server to host the application and proxy the API requests to Claude.

Now I'll create all the necessary files for this folder structure:

I've created a complete folder structure with all the files you need to run the Claude Project Generator locally. This solution addresses the loading error by using a server that handles API requests to Claude.

### What's Included:

1. **A Node.js Express server** that:
   - Serves the static HTML/CSS/JS files
   - Proxies API requests to Claude to avoid CORS issues
   - Provides a clean separation between frontend and backend

2. **Complete frontend:**
   - Modern responsive interface
   - Syntax highlighting for code
   - File tree navigation
   - Support for different Claude models

3. **Security features:**
   - Your API key is sent directly from the server to Claude
   - Option to save API key in browser localStorage for convenience

### How to Run:

1. **Create a folder** named `claude-project-generator`
2. **Save all the files** in their respective locations as shown in the folder structure
3. **Open a terminal/command prompt** and navigate to the folder
4. **Install dependencies:**
   ```
   npm install
   ```
5. **Start the application:**
   ```
   npm start
   ```
6. **Open your browser** and go to:
   ```
   http://localhost:3000
   ```

### Requirements:

- Node.js and npm installed on your computer
- A valid Claude API key

This setup is production-ready and can be run locally on your laptop without any CORS or security issues. The server handles all communication with the Claude API, making it much more reliable than a purely client-side solution.