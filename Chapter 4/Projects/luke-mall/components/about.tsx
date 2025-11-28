"use client"

import Image from "next/image"

export default function About() {
  return (
    <section id="about" className="py-20 bg-background scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid md:grid-cols-2 gap-12 items-center">
          {/* Image */}
          <div className="bg-muted rounded-lg aspect-square overflow-hidden order-2 md:order-1 relative w-full">
            <Image
              src="https://images.unsplash.com/photo-1445205170230-053b83016050?w=800&h=800&fit=crop&q=80"
              alt="LUXE 브랜드 스토리"
              fill
              className="object-cover rounded-lg"
              sizes="(max-width: 768px) 100vw, 50vw"
              priority
            />
          </div>

          {/* Content */}
          <div className="space-y-6 order-1 md:order-2">
            <h2 className="font-serif text-4xl md:text-5xl font-bold text-primary text-balance">LUXE의 이야기</h2>

            <p className="text-lg text-muted-foreground leading-relaxed">
              2015년 설립된 LUXE는 작은 아틀리에에서 시작한 패션 브랜드입니다. 우리의 창립자들은 높은 수준의 장인 정신과
              현대적 감성이 만나는 옷을 만들고 싶었습니다.
            </p>

            <p className="text-lg text-muted-foreground leading-relaxed">
              매 시즌 우리는 영감을 찾기 위해 전 세계를 여행하며, 각 컬렉션에 문화와 예술, 그리고 사람들의 이야기를
              담아냅니다. LUXE의 옷을 입는 것은 단순한 의류 선택이 아닌, 라이프스타일과 가치관을 표현하는 것입니다.
            </p>

            <div className="pt-4 space-y-4">
              <div className="flex gap-4">
                <div className="text-primary text-2xl font-bold">→</div>
                <p className="text-foreground font-medium">50개 국가에서 사랑받는 브랜드</p>
              </div>
              <div className="flex gap-4">
                <div className="text-primary text-2xl font-bold">→</div>
                <p className="text-foreground font-medium">100% 윤리적 생산 체계</p>
              </div>
              <div className="flex gap-4">
                <div className="text-primary text-2xl font-bold">→</div>
                <p className="text-foreground font-medium">매년 250만 명 이상의 고객</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
