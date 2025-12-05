"use client"

import { Sparkles, Settings } from "lucide-react"

interface SidebarProps {
  selectedModel: string
  onModelChange: (model: string) => void
}

export function Sidebar({ selectedModel, onModelChange }: SidebarProps) {
  const models = [
    { id: "gpt-5-nano", label: "GPT-5 Nano" },
    { id: "gpt-5-mini", label: "GPT-5 Mini" },
    { id: "gpt-5", label: "GPT-5" },
    { id: "gpt-4o", label: "GPT-4o" },
  ]

  return (
    <aside className="w-64 bg-card border-r border-border flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-10 h-10 rounded-lg bg-primary text-primary-foreground flex items-center justify-center">
            <Sparkles className="w-6 h-6" />
          </div>
          <h1 className="text-xl font-bold text-foreground">칼럼 작성기</h1>
        </div>
        <p className="text-sm text-muted-foreground">AI 기반 분석 칼럼 생성</p>
      </div>

      {/* Model Selection */}
      <div className="flex-1 overflow-y-auto p-6">
        <div className="mb-8">
          <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-4">모델</h3>
          <div className="space-y-2">
            {models.map((model) => (
              <button
                key={model.id}
                onClick={() => onModelChange(model.id)}
                className={`w-full text-left px-4 py-3 rounded-lg font-medium text-sm transition-all ${
                  selectedModel === model.id
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-foreground hover:bg-secondary hover:text-secondary-foreground"
                }`}
              >
                {model.label}
              </button>
            ))}
          </div>
        </div>

        {/* Settings */}
        <div className="border-t border-border pt-6">
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-all">
            <Settings className="w-5 h-5" />
            <span className="font-medium text-sm">설정</span>
          </button>
        </div>
      </div>

      {/* Footer */}
      <div className="p-6 border-t border-border">
        <p className="text-xs text-muted-foreground text-center">OpenAI 기반</p>
      </div>
    </aside>
  )
}
