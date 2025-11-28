"use client"

import { useState } from "react"
import Image from "next/image"

export default function Collections() {
  const [selectedCollection, setSelectedCollection] = useState<string | null>(null)

  const collections = [
    {
      name: "봄 컬렉션 2025",
      category: "Spring",
      image: "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&h=600&fit=crop&q=80",
      description: "신선한 색감과 가벼운 소재의 봄 시즌 컬렉션",
      color: "from-green-200 to-blue-200",
      emoji: "🌸",
      details: "봄 컬렉션은 파스텔 톤의 부드러운 색감과 가벼운 소재로 제작되었습니다. 일상에서 특별한 날까지 다양한 스타일링이 가능한 아이템들로 구성되어 있습니다."
    },
    {
      name: "썸머 라인",
      category: "Summer",
      image: "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=600&h=600&fit=crop&q=80",
      description: "시원하고 우아한 여름 스타일",
      color: "from-yellow-200 to-orange-200",
      emoji: "☀️",
      details: "여름 컬렉션은 시원한 소재와 우아한 실루엣으로 제작되었습니다. 더운 날씨에도 편안하고 스타일리시하게 보일 수 있는 아이템들로 구성되어 있습니다."
    },
    {
      name: "가을 에센셜",
      category: "Autumn",
      image: "https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=600&h=600&fit=crop&q=80",
      description: "따뜻한 톤의 가을 명작 컬렉션",
      color: "from-orange-200 to-red-200",
      emoji: "🍂",
      details: "가을 컬렉션은 따뜻한 톤의 색감과 고급스러운 소재로 제작되었습니다. 계절의 변화를 느낄 수 있는 감각적인 디자인으로 구성되어 있습니다."
    },
    {
      name: "겨울 럭셔리",
      category: "Winter",
      image: "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600&h=600&fit=crop&q=80",
      description: "고급스러운 겨울 의류 모음",
      color: "from-blue-200 to-purple-200",
      emoji: "❄️",
      details: "겨울 컬렉션은 프리미엄 소재와 세련된 디자인으로 제작되었습니다. 보온성과 스타일을 모두 갖춘 럭셔리한 아이템들로 구성되어 있습니다."
    },
  ]

  const handleCollectionClick = (collectionName: string) => {
    setSelectedCollection(selectedCollection === collectionName ? null : collectionName)
  }

  return (
    <>
      <section id="collections" className="py-20 bg-secondary scroll-mt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl font-bold text-primary mb-4 text-balance">시즌 컬렉션</h2>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              매 시즌마다 새롭게 선보이는 LUXE의 정정성 있는 컬렉션
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {collections.map((collection) => (
              <div
                key={collection.name}
                className={`group cursor-pointer bg-background rounded-lg overflow-hidden border border-border transition-all ${
                  selectedCollection === collection.name ? 'border-primary shadow-lg scale-105' : 'hover:border-primary'
                }`}
                onClick={() => handleCollectionClick(collection.name)}
              >
                <div className="aspect-square overflow-hidden relative">
                  <Image
                    src={collection.image}
                    alt={collection.name}
                    fill
                    className="object-cover transition-transform duration-300 group-hover:scale-105"
                  />
                </div>
                <div className="p-6">
                  <p className="text-xs font-bold text-primary uppercase mb-2">{collection.category}</p>
                  <h3 className="font-serif text-lg font-bold mb-2 text-foreground">{collection.name}</h3>
                  <p className="text-sm text-muted-foreground mb-4">{collection.description}</p>
                  <button className="text-primary text-sm font-bold hover:text-primary/80 transition-colors">
                    {selectedCollection === collection.name ? '접기 ↑' : '컬렉션 보기 →'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Collection Details Modal */}
      {selectedCollection && (
        <div 
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 animate-in fade-in duration-200"
          onClick={() => setSelectedCollection(null)}
        >
          <div 
            className="bg-background rounded-lg max-w-2xl w-full p-8 max-h-[90vh] overflow-y-auto animate-in slide-in-from-bottom-4 duration-300"
            onClick={(e) => e.stopPropagation()}
          >
            {collections
              .filter(c => c.name === selectedCollection)
              .map((collection) => (
                <div key={collection.name}>
                  <div className="flex items-center justify-between mb-6">
                    <div>
                      <p className="text-xs font-bold text-primary uppercase mb-2">{collection.category}</p>
                      <h2 className="font-serif text-3xl font-bold text-primary">{collection.name}</h2>
                    </div>
                    <button
                      onClick={() => setSelectedCollection(null)}
                      className="text-muted-foreground hover:text-foreground transition-colors text-2xl"
                    >
                      ×
                    </button>
                  </div>
                  
                  <div className="aspect-video rounded-lg mb-6 overflow-hidden relative">
                    <Image
                      src={collection.image}
                      alt={collection.name}
                      fill
                      className="object-cover"
                    />
                  </div>

                  <div className="space-y-4">
                    <p className="text-lg text-muted-foreground leading-relaxed">{collection.details}</p>
                    <div className="pt-4 border-t border-border">
                      <h3 className="font-bold text-foreground mb-3">컬렉션 특징</h3>
                      <ul className="space-y-2 text-muted-foreground">
                        <li className="flex items-start gap-2">
                          <span className="text-primary">→</span>
                          <span>프리미엄 소재 사용</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-primary">→</span>
                          <span>수공예 제작</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-primary">→</span>
                          <span>지속 가능한 패션</span>
                        </li>
                        <li className="flex items-start gap-2">
                          <span className="text-primary">→</span>
                          <span>시간초월적 디자인</span>
                        </li>
                      </ul>
                    </div>
                    <button className="w-full mt-6 px-6 py-3 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition-colors">
                      컬렉션 구매하기
                    </button>
                  </div>
                </div>
              ))}
          </div>
        </div>
      )}
    </>
  )
}
