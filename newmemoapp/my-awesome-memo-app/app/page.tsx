"use client"

import { useState, useEffect } from "react"
import { useRouter } from "next/navigation"
import { Plus, Search, LogOut, User } from "lucide-react"
import { NoteCard } from "@/components/note-card"
import { NoteForm } from "@/components/note-form"

interface Note {
  id: string
  title: string
  content: string
  color: string
  createdAt: string
}

interface User {
  id: string
  email: string
  name: string | null
}

export default function Page() {
  const router = useRouter()
  const [notes, setNotes] = useState<Note[]>([])
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [showForm, setShowForm] = useState(false)

  useEffect(() => {
    checkAuth()
    loadNotes()
  }, [])

  const checkAuth = async () => {
    try {
      const response = await fetch("/api/auth/me")
      if (response.ok) {
        const data = await response.json()
        setUser(data.user)
      } else {
        router.push("/login")
      }
    } catch (error) {
      router.push("/login")
    } finally {
      setLoading(false)
    }
  }

  const loadNotes = async () => {
    try {
      const response = await fetch("/api/notes")
      if (response.ok) {
        const data = await response.json()
        setNotes(data.notes)
      }
    } catch (error) {
      console.error("Failed to load notes:", error)
    }
  }

  const handleAddNote = async (title: string, content: string, color: string) => {
    try {
      const response = await fetch("/api/notes", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, content, color }),
      })

      if (response.ok) {
        const data = await response.json()
        setNotes([data.note, ...notes])
        setShowForm(false)
      }
    } catch (error) {
      console.error("Failed to add note:", error)
    }
  }

  const handleDeleteNote = async (id: string) => {
    try {
      const response = await fetch(`/api/notes/${id}`, {
        method: "DELETE",
      })

      if (response.ok) {
        setNotes(notes.filter((note) => note.id !== id))
      }
    } catch (error) {
      console.error("Failed to delete note:", error)
    }
  }

  const handleLogout = async () => {
    try {
      await fetch("/api/auth/logout", { method: "POST" })
      router.push("/login")
      router.refresh()
    } catch (error) {
      console.error("Failed to logout:", error)
    }
  }

  const filteredNotes = notes.filter(
    (note) =>
      note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      note.content.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 flex items-center justify-center">
        <div className="text-slate-500">로딩 중...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-sm border-b border-slate-200/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-slate-900">메모</h1>
              <p className="text-sm text-slate-500 mt-1">{notes.length}개의 메모가 있습니다</p>
            </div>
            <div className="flex items-center gap-3">
              {user && (
                <div className="flex items-center gap-2 text-slate-600">
                  <User size={18} />
                  <span className="text-sm">{user.name || user.email}</span>
                </div>
              )}
              <button
                onClick={() => setShowForm(true)}
                className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white px-6 py-3 rounded-lg font-semibold shadow-md hover:shadow-lg transition-all duration-200"
              >
                <Plus size={20} />새 메모
              </button>
              <button
                onClick={handleLogout}
                className="inline-flex items-center gap-2 bg-slate-100 hover:bg-slate-200 text-slate-700 px-4 py-3 rounded-lg font-semibold transition-all duration-200"
              >
                <LogOut size={18} />로그아웃
              </button>
            </div>
          </div>

          {/* Search Bar */}
          <div className="mt-6 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
            <input
              type="text"
              placeholder="메모 검색..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white transition-all"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {showForm && (
          <div className="mb-8">
            <NoteForm onSubmit={handleAddNote} onCancel={() => setShowForm(false)} />
          </div>
        )}

        {/* Notes Grid */}
        {filteredNotes.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredNotes.map((note) => (
              <NoteCard key={note.id} note={note} onDelete={() => handleDeleteNote(note.id)} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-slate-300 mb-4 text-5xl">📝</div>
            <p className="text-slate-500 text-lg">{searchQuery ? "검색 결과가 없습니다" : "메모를 추가해주세요"}</p>
          </div>
        )}
      </main>
    </div>
  )
}
