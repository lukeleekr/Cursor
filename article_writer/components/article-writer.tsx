"use client"

import { useState } from "react"
import { Sidebar } from "./sidebar"
import { MainContent } from "./main-content"

export function ArticleWriter() {
  const [selectedModel, setSelectedModel] = useState("gpt-5-nano")
  const [isGenerating, setIsGenerating] = useState(false)
  const [output, setOutput] = useState("")

  const handleGenerate = async (input: {
    keyword: string
    instructions: string
    files: File[]
  }) => {
    setIsGenerating(true)
    try {
      // API call will be implemented here
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          keyword: input.keyword,
          instructions: input.instructions,
          model: selectedModel,
        }),
      })
      const data = await response.json()
      if (data.error) {
        setOutput(`오류: ${data.error}`)
      } else {
        setOutput(data.content || "생성된 내용이 없습니다.")
      }
    } catch (error) {
      console.error("Error generating article:", error)
      setOutput("칼럼 생성 중 오류가 발생했습니다. 다시 시도해주세요.")
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="flex h-screen">
      <Sidebar selectedModel={selectedModel} onModelChange={setSelectedModel} />
      <MainContent onGenerate={handleGenerate} isGenerating={isGenerating} output={output} />
    </div>
  )
}
