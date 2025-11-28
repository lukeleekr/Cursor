"use client"

import Image from "next/image"

export default function Hero() {
  const handleSmoothScroll = (targetId: string) => {
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
  }

  return (
    <section className="pt-32 pb-20 bg-gradient-to-b from-secondary to-background">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <div className="space-y-6">
            <h1 className="font-serif text-5xl md:text-6xl font-bold text-primary text-balance leading-tight">
              당신의 스타일, 우리의 철학
            </h1>
            <p className="text-lg text-muted-foreground leading-relaxed">
              LUXE는 현대적 감성과 고전적 우아함을 결합한 프리미엄 패션 브랜드입니다. 매 시즌 정교하게 제작된 컬렉션으로
              당신의 개성을 표현하세요.
            </p>
            <div className="flex gap-4 pt-4">
              <button 
                onClick={() => handleSmoothScroll("collections")}
                className="px-8 py-3 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition-colors cursor-pointer"
              >
                새로운 컬렉션 보기
              </button>
              <button 
                onClick={() => handleSmoothScroll("about")}
                className="px-8 py-3 border-2 border-primary text-primary font-medium rounded-lg hover:bg-primary hover:text-primary-foreground transition-colors cursor-pointer"
              >
                더 알아보기
              </button>
            </div>
          </div>

          {/* Hero Image */}
          <div className="bg-muted rounded-lg aspect-square overflow-hidden relative">
            <Image
              src="https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=800&h=800&fit=crop"
              alt="LUXE 컬렉션 전시"
              fill
              className="object-cover"
              priority
              sizes="(max-width: 768px) 100vw, 50vw"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
