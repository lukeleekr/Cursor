"use client"

import type React from "react"

import { useState } from "react"
import { Plus, X } from "lucide-react"

interface InputSectionProps {
  keyword: string
  setKeyword: (value: string) => void
  instructions: string
  setInstructions: (value: string) => void
  files: File[]
  setFiles: (files: File[]) => void
  style?: React.CSSProperties
}

export function InputSection({
  keyword,
  setKeyword,
  instructions,
  setInstructions,
  files,
  setFiles,
  style,
}: InputSectionProps) {
  const [dragActive, setDragActive] = useState(false)

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const newFiles = Array.from(e.dataTransfer.files)
      setFiles([...files, ...newFiles])
    }
  }

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files)
      setFiles([...files, ...newFiles])
    }
  }

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index))
  }

  return (
    <div className="flex-1 overflow-auto bg-background p-8 border-r border-border" style={style}>
      <div className="space-y-6 max-w-2xl">
        {/* Keyword Input */}
        <div>
          <label className="block text-sm font-semibold text-foreground mb-3">키워드 또는 주제</label>
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="칼럼의 주제나 키워드를 입력하세요..."
            className="w-full px-4 py-3 rounded-lg border border-border bg-card text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
          />
        </div>

        {/* Instructions Input */}
        <div>
          <label className="block text-sm font-semibold text-foreground mb-3">추가 지시사항</label>
          <textarea
            value={instructions}
            onChange={(e) => setInstructions(e.target.value)}
            placeholder="칼럼 작성에 필요한 추가 맥락이나 구체적인 지시사항을 입력하세요..."
            rows={4}
            className="w-full px-4 py-3 rounded-lg border border-border bg-card text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent resize-none"
          />
          <p className="text-xs text-muted-foreground mt-2">
            원하는 스타일, 톤, 또는 포함할 특정 내용을 설명해주세요
          </p>
        </div>

        {/* File Upload */}
        <div>
          <label className="block text-sm font-semibold text-foreground mb-3">첨부 파일 (선택사항)</label>
          <div
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-lg p-8 text-center transition-all ${
              dragActive ? "border-primary bg-primary/5" : "border-border bg-muted/30 hover:border-primary/50"
            }`}
          >
            <input type="file" id="file-upload" multiple onChange={handleFileSelect} className="hidden" />
            <label htmlFor="file-upload" className="cursor-pointer block">
              <div className="flex flex-col items-center gap-3">
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                  <Plus className="w-6 h-6 text-primary" />
                </div>
                <div>
                  <p className="font-medium text-foreground">파일을 여기에 드롭하거나 클릭하여 선택하세요</p>
                  <p className="text-sm text-muted-foreground mt-1">PDF, TXT, DOC 및 이미지 파일 지원</p>
                </div>
              </div>
            </label>
          </div>

          {/* File List */}
          {files.length > 0 && (
            <div className="mt-4 space-y-2">
              {files.map((file, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-muted rounded-lg">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-foreground">{file.name}</p>
                    <p className="text-xs text-muted-foreground">{(file.size / 1024).toFixed(2)} KB</p>
                  </div>
                  <button
                    onClick={() => removeFile(index)}
                    className="p-2 hover:bg-border rounded-lg transition-colors"
                  >
                    <X className="w-4 h-4 text-muted-foreground" />
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
