"use client"

import type React from "react"

import { useState } from "react"
import { X } from "lucide-react"

const COLORS = [
  { name: "blue", bg: "bg-blue-100", border: "border-blue-300" },
  { name: "pink", bg: "bg-pink-100", border: "border-pink-300" },
  { name: "yellow", bg: "bg-yellow-100", border: "border-yellow-300" },
  { name: "green", bg: "bg-green-100", border: "border-green-300" },
  { name: "purple", bg: "bg-purple-100", border: "border-purple-300" },
  { name: "orange", bg: "bg-orange-100", border: "border-orange-300" },
]

interface NoteFormProps {
  onSubmit: (title: string, content: string, color: string) => void
  onCancel: () => void
}

export function NoteForm({ onSubmit, onCancel }: NoteFormProps) {
  const [title, setTitle] = useState("")
  const [content, setContent] = useState("")
  const [selectedColor, setSelectedColor] = useState("bg-blue-100")

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (title.trim() || content.trim()) {
      onSubmit(title || "제목 없음", content, selectedColor)
      setTitle("")
      setContent("")
      setSelectedColor("bg-blue-100")
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden">
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-slate-900">새 메모</h2>
          <button
            onClick={onCancel}
            className="p-2 hover:bg-slate-100 rounded-lg text-slate-500 hover:text-slate-700 transition-colors"
            aria-label="Close form"
          >
            <X size={20} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            type="text"
            placeholder="제목을 입력하세요..."
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
          />

          <textarea
            placeholder="내용을 입력하세요..."
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={4}
            className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all resize-none"
          />

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-3">색상 선택</label>
            <div className="grid grid-cols-6 gap-2">
              {COLORS.map((color) => (
                <button
                  key={color.name}
                  type="button"
                  onClick={() => setSelectedColor(color.bg)}
                  className={`h-10 rounded-lg border-2 transition-all ${
                    selectedColor === color.bg
                      ? `${color.bg} ${color.border} border-2`
                      : `${color.bg} border-transparent hover:border-slate-300`
                  }`}
                  aria-label={`Select ${color.name} color`}
                />
              ))}
            </div>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={onCancel}
              className="flex-1 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-900 font-semibold rounded-lg transition-colors"
            >
              취소
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transition-all"
            >
              저장
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
