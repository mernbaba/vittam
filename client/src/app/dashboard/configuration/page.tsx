"use client";

import { useState, useEffect } from "react";
import { Copy, Trash, Key, Webhook, Check, EyeOff, Palette, Settings, Code, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Textarea } from "@/components/ui/textarea";
import { toast } from "sonner";

export default function ConfigurationPage() {
  const [apiKey, setApiKey] = useState("nkd_wapI_LdM8iOH_*************");
  const [webhookUrl, setWebhookUrl] = useState("https://webhooks.vittam.growsoc.com/692bf271-71af-4854-b664-ffa7581a67c7");
  const [webhooksEnabled, setWebhooksEnabled] = useState(false);

  // Chatbot Customization State
  const [botName, setBotName] = useState("Vittam Assistant");
  const [welcomeMessage, setWelcomeMessage] = useState("Hello! How can I help you with your loan application today?");
  const [brandColor, setBrandColor] = useState("#0d9488"); // Default teal

  // Dynamic Script Generation
  const [installationCode, setInstallationCode] = useState("");

  useEffect(() => {
    const script = `<script>
  window.vittamConfig = {
    apiKey: "${apiKey}",
    botName: "${botName}",
    theme: "${brandColor}",
    welcomeMessage: "${welcomeMessage}"
  };
  (function(d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s); js.id = id;
    js.src = "https://cdn.vittam.ai/widget/loader.js";
    fjs.parentNode.insertBefore(js, fjs);
  }(document, 'script', 'vittam-widget'));
</script>`;
    setInstallationCode(script);
  }, [apiKey, botName, brandColor, welcomeMessage]);

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Copied to clipboard");
  };

  return (
    <div className="h-dvh flex flex-col bg-gray-50/50">
      <header className="bg-white h-16 flex items-center justify-between border-b border-gray-200 px-6 shrink-0 z-10 relative">
        <h1 className="text-xl font-bold flex items-center gap-2">
          <Settings className="h-5 w-5 text-gray-500" />
          Configuration
        </h1>
      </header>

      <div className="flex-1 overflow-y-auto p-6">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-[1600px] mx-auto">

          {/* LEFT COLUMN: Configuration (8 cols) */}
          <div className="lg:col-span-8 space-y-6">

            {/* Chatbot Customization Card */}
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="pb-3 border-b border-gray-100 bg-white rounded-t-lg">
                <div className="flex items-center gap-2">
                  <div className="p-2 bg-teal-50 rounded-lg">
                    <Palette className="h-5 w-5 text-teal-600" />
                  </div>
                  <div>
                    <CardTitle className="text-base font-semibold text-gray-900">Customize Assistant</CardTitle>
                    <CardDescription className="text-xs">Appearance & Behavior</CardDescription>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="p-6 grid gap-6 md:grid-cols-2">
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Bot Identity</Label>
                    <div className="space-y-3">
                      <div className="space-y-2">
                        <Label htmlFor="bot-name" className="text-sm font-medium">Name</Label>
                        <Input
                          id="bot-name"
                          value={botName}
                          onChange={(e) => setBotName(e.target.value)}
                          className="h-9"
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="brand-color" className="text-sm font-medium">Accent Color</Label>
                        <div className="flex gap-2">
                          <Input
                            id="brand-color"
                            type="color"
                            value={brandColor}
                            onChange={(e) => setBrandColor(e.target.value)}
                            className="w-12 h-9 p-1 cursor-pointer"
                          />
                          <Input
                            value={brandColor}
                            onChange={(e) => setBrandColor(e.target.value)}
                            className="font-mono uppercase h-9 flex-1"
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Messaging</Label>
                  <div className="space-y-2">
                    <Label htmlFor="welcome-msg" className="text-sm font-medium">Welcome Greeting</Label>
                    <Textarea
                      id="welcome-msg"
                      rows={5}
                      value={welcomeMessage}
                      onChange={(e) => setWelcomeMessage(e.target.value)}
                      className="resize-none text-sm leading-relaxed"
                    />
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Technical Settings Group */}
            <div className="grid gap-6 md:grid-cols-2">
              {/* API Keys Card */}
              <Card className="border-gray-200 shadow-sm h-full">
                <CardHeader className="pb-3 border-b border-gray-100">
                  <div className="flex items-center gap-2">
                    <Key className="h-4 w-4 text-gray-500" />
                    <CardTitle className="text-sm font-semibold">API Credentials</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="p-4 space-y-4">
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 relative group">
                    <p className="font-mono text-xs font-medium text-gray-800 break-all pr-8">{apiKey}</p>
                    <Button variant="ghost" size="icon" className="absolute top-1 right-1 h-6 w-6 text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity">
                      <Trash className="h-3 w-3" />
                    </Button>
                  </div>
                  <Button variant="outline" size="sm" className="w-full h-8 text-xs">
                    Roll Key
                  </Button>
                </CardContent>
              </Card>

              {/* Webhook Card */}
              <Card className="border-gray-200 shadow-sm h-full">
                <CardHeader className="pb-3 border-b border-gray-100 flex flex-row items-center justify-between space-y-0">
                  <div className="flex items-center gap-2">
                    <Webhook className="h-4 w-4 text-gray-500" />
                    <CardTitle className="text-sm font-semibold">Webhook</CardTitle>
                  </div>
                  <Switch checked={webhooksEnabled} onCheckedChange={setWebhooksEnabled} className="scale-75 origin-right" />
                </CardHeader>
                <CardContent className="p-4 space-y-3">
                  <div className="space-y-2">
                    <Label className="text-xs">Endpoint URL</Label>
                    <Input
                      value={webhookUrl}
                      onChange={(e) => setWebhookUrl(e.target.value)}
                      className="h-8 font-mono text-xs"
                    />
                  </div>
                  <Button size="sm" className="w-full h-8 text-xs bg-gray-900 text-white hover:bg-gray-800">
                    Update Configuration
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* RIGHT COLUMN: Installation & Preview (4 cols) */}
          <div className="lg:col-span-4 space-y-6">
            <div className="sticky top-6 space-y-6">
              <Card className="border-indigo-200 shadow-sm bg-indigo-50/30 overflow-hidden">
                <CardHeader className="bg-indigo-100/50 pb-3 border-b border-indigo-100">
                  <div className="flex items-center gap-2">
                    <Code className="h-4 w-4 text-indigo-600" />
                    <CardTitle className="text-sm font-semibold text-indigo-900">Install to Website</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="bg-gray-900 p-4 overflow-x-auto">
                    <pre className="text-[10px] leading-relaxed font-mono text-gray-300 whitespace-pre-wrap">{installationCode}</pre>
                  </div>
                </CardContent>
                <CardFooter className="p-3 bg-white border-t border-indigo-100">
                  <Button
                    size="sm"
                    className="w-full bg-indigo-600 hover:bg-indigo-700 text-white gap-2"
                    onClick={() => copyToClipboard(installationCode)}
                  >
                    <Copy className="h-3.5 w-3.5" /> Copy Script
                  </Button>
                </CardFooter>
              </Card>

              <div className="space-y-3">
                <Card className="border-green-100 shadow-sm bg-green-50/30">
                  <CardContent className="p-3 flex gap-3 items-start">
                    <div className="mt-0.5 bg-green-100 p-1 rounded-full h-5 w-5 flex items-center justify-center text-green-600 shrink-0">
                      <Check className="h-3 w-3" />
                    </div>
                    <div>
                      <p className="font-medium text-xs text-gray-900">Installation Status</p>
                      <p className="text-[10px] text-gray-600 mt-1 leading-tight">We haven't detected the script yet. Check back in ~5 mins.</p>
                      <Button variant="link" className="px-0 text-[10px] text-green-700 h-auto mt-1 p-0">Verify Now</Button>
                    </div>
                  </CardContent>
                </Card>

                <Card className="border-gray-200 shadow-sm">
                  <CardContent className="p-3 flex gap-3 items-start">
                    <div className="mt-0.5 bg-gray-100 p-1 rounded-full h-5 w-5 flex items-center justify-center text-gray-500 shrink-0">
                      <EyeOff className="h-3 w-3" />
                    </div>
                    <div>
                      <p className="font-medium text-xs text-gray-900">Privacy Mode</p>
                      <p className="text-[10px] text-gray-500 mt-1 leading-tight">Sensitive data is automatically masked.</p>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}

