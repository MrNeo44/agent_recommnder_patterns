"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
/// <reference types="vscode" />
const vscode = __importStar(require("vscode"));
const child_process_1 = require("child_process");
function activate(context) {
    console.log('✅ BDI-LLM Extension activated');
    const disposable = vscode.workspace.onDidSaveTextDocument((doc) => __awaiter(this, void 0, void 0, function* () {
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
        const py = (0, child_process_1.spawn)(pythonPath, [scriptPath], { shell: false });
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
            }
            else {
                const pattern = output.trim();
                console.log('✅ Patrón recibido:', pattern);
                vscode.window.showInformationMessage(`Patrón sugerido: ${pattern}`);
            }
        });
        // Enviar el código por stdin
        py.stdin.write(code);
        py.stdin.end();
    }));
    context.subscriptions.push(disposable);
}
exports.activate = activate;
function deactivate() {
    console.log('🛑 BDI-LLM Extension deactivated');
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map