"use client"

import { useState } from "react"
import { Loader2, Copy, Download, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { InputSection } from "./input-section"

interface MainContentProps {
  onGenerate: (input: { keyword: string; instructions: string; files: File[] }) => void
  isGenerating: boolean
  output: string
}

export function MainContent({ onGenerate, isGenerating, output }: MainContentProps) {
  const [keyword, setKeyword] = useState("")
  const [instructions, setInstructions] = useState("")
  const [files, setFiles] = useState<File[]>([])
  const [dividerPos, setDividerPos] = useState(50)
  const [isDragging, setIsDragging] = useState(false)

  const handleGenerate = () => {
    onGenerate({ keyword, instructions, files })
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(output)
  }

  const handleDownload = () => {
    const element = document.createElement("a")
    element.setAttribute("href", "data:text/markdown;charset=utf-8," + encodeURIComponent(output))
    element.setAttribute("download", `article_${Date.now()}.md`)
    element.style.display = "none"
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <div className="flex-1 flex flex-col">
      {/* Header */}
      <header className="border-b border-border bg-card px-8 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-3xl font-bold text-foreground mb-2">칼럼 생성</h2>
            <p className="text-muted-foreground">AI 기반 분석 칼럼 작성</p>
          </div>
          <Button onClick={handleGenerate} disabled={!keyword || isGenerating} className="gap-2">
            {isGenerating ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                생성 중...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                생성하기
              </>
            )}
          </Button>
        </div>
      </header>

      {/* Main Content Area */}
      <div className="flex-1 flex overflow-hidden">
        <InputSection
          keyword={keyword}
          setKeyword={setKeyword}
          instructions={instructions}
          setInstructions={setInstructions}
          files={files}
          setFiles={setFiles}
          style={{ width: `${dividerPos}%` }}
        />

        {/* Divider */}
        <div
          onMouseDown={() => setIsDragging(true)}
          onMouseUp={() => setIsDragging(false)}
          onMouseMove={(e) => {
            if (!isDragging) return
            const container = e.currentTarget.parentElement
            if (container) {
              const newPos = (e.clientX / container.clientWidth) * 100
              if (newPos > 30 && newPos < 70) {
                setDividerPos(newPos)
              }
            }
          }}
          className={`w-1 bg-border hover:bg-primary cursor-col-resize transition-colors ${
            isDragging ? "bg-primary" : ""
          }`}
        />

        {/* Output Section */}
        <div className="flex-1 flex flex-col overflow-hidden" style={{ width: `${100 - dividerPos}%` }}>
          <div className="border-b border-border px-8 py-4 flex items-center justify-between">
            <h3 className="font-semibold text-foreground">생성된 칼럼</h3>
            {output && (
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={handleCopy} className="gap-2 bg-transparent">
                  <Copy className="w-4 h-4" />
                  복사
                </Button>
                <Button variant="outline" size="sm" onClick={handleDownload} className="gap-2 bg-transparent">
                  <Download className="w-4 h-4" />
                  다운로드
                </Button>
              </div>
            )}
          </div>

          <div className="flex-1 overflow-auto p-8">
            {output ? (
              <div className="prose prose-sm max-w-none">
                <pre className="bg-muted p-6 rounded-lg overflow-auto text-sm leading-relaxed whitespace-pre-wrap break-words">
                  {output}
                </pre>
              </div>
            ) : (
              <div className="h-full flex items-center justify-center text-center">
                <div>
                  <div className="w-16 h-16 rounded-full bg-muted mx-auto mb-4 flex items-center justify-center">
                    <Sparkles className="w-8 h-8 text-muted-foreground" />
                  </div>
                  <p className="text-muted-foreground">칼럼을 생성하면 결과가 여기에 표시됩니다</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
