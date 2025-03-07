# AI-VSCode-Connector

**AI-VSCode-Connector** is a Visual Studio Code extension that exposes a WebSocket interface for file management. It allows an AI agent to create and delete files within the VS Code environment by sending simple JSON commands. The extension leverages VS Code's native file system API for seamless integration.

## Features

- **WebSocket Interface for File Management:**  
  Accepts JSON commands to create or delete files on the fly.
- **Real-Time Communication:**  
  Uses WebSockets for low-latency, bidirectional communication.
- **Seamless Integration:**  
  Leverages VS Code's native `workspace.fs` API to perform file operations.

## Requirements

- [Visual Studio Code](https://code.visualstudio.com/) or [code‑server](https://coder.com/docs/code-server/latest)
- Node.js (v18 or later recommended)
- This extension should be installed in an environment where your AI agent can connect via WebSockets.

## Usage

Once the extension is activated, it starts a WebSocket server on port **8765**. You can connect to this server using any WebSocket client and send commands in the following JSON formats:

- **Create a file:**

```
{
  "operation": "create",
  "filepath": "path/to/your/file.txt",
  "content": "your file content here"
}
```

- **Delete a file:**

```
{
  "operation": "delete",
  "filepath": "path/to/your/file.txt"
}
```

The extension will respond with a JSON message indicating the status of the operation.

## Extension Settings

This extension does not contribute any additional VS Code settings. All configuration is handled via the extension's source code and environment settings.

## Known Issues

- No known issues at this time.

## Release Notes

### 1.0.0

- Initial release of AI-VSCode-Connector.
- Added WebSocket interface for file creation and deletion.
- Integrated with VS Code’s native file system API.

---

For more information on developing VS Code extensions, please refer to the [VS Code Extension API documentation](https://code.visualstudio.com/api).

**Enjoy using AI-VSCode-Connector!**
