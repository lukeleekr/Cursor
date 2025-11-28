"use client"

import { useState, useEffect } from "react"
import Link from "next/link"

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
    }
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  const handleSmoothScroll = (e: React.MouseEvent<HTMLAnchorElement>, targetId: string) => {
    e.preventDefault()
    const element = document.getElementById(targetId)
    if (element) {
      const headerOffset = 80
      const elementPosition = element.getBoundingClientRect().top
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset

      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth"
      })
    }
    setMenuOpen(false)
  }

  return (
    <header className={`fixed top-0 w-full bg-background border-b border-border z-50 transition-all ${scrolled ? 'shadow-md' : ''}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2" onClick={(e) => {
            e.preventDefault()
            window.scrollTo({ top: 0, behavior: "smooth" })
          }}>
            <div className="w-8 h-8 bg-primary rounded-sm"></div>
            <span className="font-serif text-xl font-bold text-primary">LUXE</span>
          </Link>

          {/* Navigation */}
          <nav className="hidden md:flex items-center gap-8">
            <a 
              href="#collections" 
              onClick={(e) => handleSmoothScroll(e, "collections")}
              className="text-sm font-medium hover:text-primary transition-colors cursor-pointer"
            >
              컬렉션
            </a>
            <a 
              href="#about" 
              onClick={(e) => handleSmoothScroll(e, "about")}
              className="text-sm font-medium hover:text-primary transition-colors cursor-pointer"
            >
              소개
            </a>
            <a 
              href="#contact" 
              onClick={(e) => handleSmoothScroll(e, "contact")}
              className="text-sm font-medium hover:text-primary transition-colors cursor-pointer"
            >
              연락처
            </a>
          </nav>

          {/* CTA Button */}
          <div className="hidden md:flex items-center gap-4">
            <button 
              onClick={(e) => handleSmoothScroll(e as any, "collections")}
              className="px-6 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-lg hover:bg-primary/90 transition-colors cursor-pointer"
            >
              구매하기
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button onClick={() => setMenuOpen(!menuOpen)} className="md:hidden p-2">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {menuOpen && (
          <div className="md:hidden pb-4 space-y-2">
            <a 
              href="#collections" 
              onClick={(e) => handleSmoothScroll(e, "collections")}
              className="block px-4 py-2 hover:bg-secondary rounded cursor-pointer"
            >
              컬렉션
            </a>
            <a 
              href="#about" 
              onClick={(e) => handleSmoothScroll(e, "about")}
              className="block px-4 py-2 hover:bg-secondary rounded cursor-pointer"
            >
              소개
            </a>
            <a 
              href="#contact" 
              onClick={(e) => handleSmoothScroll(e, "contact")}
              className="block px-4 py-2 hover:bg-secondary rounded cursor-pointer"
            >
              연락처
            </a>
            <button 
              onClick={(e) => handleSmoothScroll(e as any, "collections")}
              className="w-full mt-2 px-4 py-2 bg-primary text-primary-foreground rounded cursor-pointer"
            >
              구매하기
            </button>
          </div>
        )}
      </div>
    </header>
  )
}
