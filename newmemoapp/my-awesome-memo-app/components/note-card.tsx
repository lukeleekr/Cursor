"use client"

import { Trash2, Calendar } from "lucide-react"

interface NoteCardProps {
  note: {
    id: string
    title: string
    content: string
    color: string
    createdAt: string | Date
  }
  onDelete: () => void
}

export function NoteCard({ note, onDelete }: NoteCardProps) {
  const formatDate = (date: string | Date) => {
    const dateObj = typeof date === "string" ? new Date(date) : date
    return dateObj.toLocaleDateString("ko-KR", {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  return (
    <div
      className={`${note.color} rounded-xl p-6 shadow-sm hover:shadow-md transition-all duration-200 group border border-white/50`}
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <h3 className="text-lg font-semibold text-slate-900 flex-1 line-clamp-2">{note.title}</h3>
        <button
          onClick={onDelete}
          className="p-2 text-slate-400 hover:text-red-500 hover:bg-white/60 rounded-lg opacity-0 group-hover:opacity-100 transition-all duration-200"
          aria-label="Delete note"
        >
          <Trash2 size={18} />
        </button>
      </div>

      <p className="text-slate-700 text-sm line-clamp-4 mb-4">{note.content}</p>

      <div className="flex items-center gap-2 text-xs text-slate-500">
        <Calendar size={14} />
        <time>{formatDate(note.createdAt)}</time>
      </div>
    </div>
  )
}
