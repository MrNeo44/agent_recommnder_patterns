/// <reference types="vscode" />
import * as vscode from 'vscode';
import { spawn } from 'child_process';
import * as path from 'path';

export function activate(context: vscode.ExtensionContext) {
  console.log('✅ BDI-LLM Extension activated');

  const disposable = vscode.workspace.onDidSaveTextDocument(async (doc: vscode.TextDocument) => {
    // 🔔 DEBUG: confirmar que el listener atrapa el evento
    vscode.window.showInformationMessage('🔔 Save event detected for: ' + doc.uri.fsPath);
    console.log('🔔 onDidSaveTextDocument fired for:', doc.uri.fsPath);

    if (doc.languageId !== 'python') {
      console.log('🛑 No es un archivo Python, se ignora');
      return;
    }

    const code = doc.getText();
    console.log('📄 Código Python capturado, longitud:', code.length);

    // Rutas absolutas: cambia según tu entorno
    const pythonPath = 'C:/Users/DiegoGaticaPizarro/PycharmProjects/PythonProject/.venv/Scripts/python.exe';
    const scriptPath = 'C:/Users/DiegoGaticaPizarro/OneDrive - Dprime/repositorios-mia/agent_recommnder_patterns/main.py';

    console.log('🐍 Invocando Python:', pythonPath, scriptPath);

    // Lanzar el proceso Python
    const py = spawn(pythonPath, [scriptPath], { shell: false });

    let output = '';
    let errorOutput = '';

    py.stdout.on('data', (data) => {
      console.log('📥 stdout chunk:', data.toString());
      output += data.toString();
    });

    py.stderr.on('data', (data) => {
      console.error('📤 stderr chunk:', data.toString());
      errorOutput += data.toString();
    });

    py.on('error', (err) => {
      console.error('⚠️ Spawn error:', err);
      vscode.window.showErrorMessage(`Error lanzando Python: ${err.message}`);
    });

    py.on('close', (codeExit) => {
      console.log(`🔚 Python process closed with code ${codeExit}`);
      if (errorOutput) {
        vscode.window.showErrorMessage(`Error agente: ${errorOutput}`);
      } else {
        const pattern = output.trim();
        console.log('✅ Patrón recibido:', pattern);
        vscode.window.showInformationMessage(`Patrón sugerido: ${pattern}`);
      }
    });

    // Enviar el código por stdin
    py.stdin.write(code);
    py.stdin.end();
  });

  context.subscriptions.push(disposable);
}

export function deactivate() {
  console.log('🛑 BDI-LLM Extension deactivated');
}
