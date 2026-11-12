import * as vscode from "vscode";
import { createGatewayClient } from "./gateway";
import { LintenChatProvider } from "./provider";

export const VENDOR = "linten";
export const REFRESH_COMMAND = "linten.refreshModels";

export function activate(context: vscode.ExtensionContext): void {
  const provider = new LintenChatProvider(createGatewayClient());
  context.subscriptions.push(
    provider,
    vscode.lm.registerLanguageModelChatProvider(VENDOR, provider),
    vscode.commands.registerCommand(REFRESH_COMMAND, () => provider.refresh()),
  );
}

export function deactivate(): void {}
