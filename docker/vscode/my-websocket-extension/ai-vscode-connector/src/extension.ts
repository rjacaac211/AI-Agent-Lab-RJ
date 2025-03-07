import * as vscode from 'vscode';
import { WebSocketServer, WebSocket } from 'ws';

export function activate(context: vscode.ExtensionContext) {
    const port = 8765;
    const wss = new WebSocketServer({ port });
    
    wss.on('connection', (ws: WebSocket) => {
        ws.on('message', async (message: string) => {
            try {
                const cmd = JSON.parse(message);
                if (cmd.operation === 'create') {
                    const uri = vscode.Uri.file(cmd.filepath);
                    const content = Buffer.from(cmd.content);
                    await vscode.workspace.fs.writeFile(uri, content);
                    ws.send(JSON.stringify({ status: 'success', message: `File ${cmd.filepath} created.` }));
                } else if (cmd.operation === 'delete') {
                    const uri = vscode.Uri.file(cmd.filepath);
                    await vscode.workspace.fs.delete(uri, { recursive: false, useTrash: false });
                    ws.send(JSON.stringify({ status: 'success', message: `File ${cmd.filepath} deleted.` }));
                } else {
                    ws.send(JSON.stringify({ status: 'error', message: 'Invalid operation.' }));
                }
            } catch (err: any) {
                ws.send(JSON.stringify({ status: 'error', message: err.message }));
            }
        });
    });
    
    vscode.window.showInformationMessage(`WebSocket server started on port ${port}`);
}

export function deactivate() {
    // Clean up resources if needed
}
