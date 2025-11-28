"use client"

import { useState } from "react"

export default function Footer() {
  const [activeModal, setActiveModal] = useState<string | null>(null)

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

  const shoppingContent = {
    women: {
      title: "여성 컬렉션",
      description: "우아하고 세련된 여성 의류 컬렉션",
      items: [
        { name: "드레스", price: "₩299,000", category: "정장" },
        { name: "블라우스", price: "₩149,000", category: "캐주얼" },
        { name: "팬츠", price: "₩199,000", category: "하의" },
        { name: "아우터", price: "₩399,000", category: "외투" },
      ]
    },
    men: {
      title: "남성 컬렉션",
      description: "클래식하고 모던한 남성 의류 컬렉션",
      items: [
        { name: "정장", price: "₩599,000", category: "정장" },
        { name: "셔츠", price: "₩129,000", category: "상의" },
        { name: "바지", price: "₩179,000", category: "하의" },
        { name: "코트", price: "₩449,000", category: "외투" },
      ]
    },
    new: {
      title: "신상품",
      description: "최신 트렌드를 반영한 새로운 컬렉션",
      items: [
        { name: "2025 봄 신상", badge: "NEW", price: "₩249,000" },
        { name: "리미티드 에디션", badge: "LIMITED", price: "₩399,000" },
        { name: "콜라보레이션", badge: "COLLAB", price: "₩349,000" },
      ]
    },
    sale: {
      title: "세일",
      description: "특별 할인 상품",
      items: [
        { name: "시즌 오프 세일", discount: "최대 50%", originalPrice: "₩299,000", salePrice: "₩149,500" },
        { name: "클리어런스", discount: "최대 70%", originalPrice: "₩199,000", salePrice: "₩59,700" },
        { name: "플래시 세일", discount: "한정 시간", originalPrice: "₩399,000", salePrice: "₩199,500" },
      ]
    }
  }

  const companyContent = {
    about: {
      title: "회사 소개",
      content: "LUXE는 2015년 설립된 프리미엄 패션 브랜드로, 현대적 감성과 고전적 우아함을 결합한 의류를 제작합니다. 우리는 세계 최고의 소재와 수공예 기술로 고객에게 최고의 패션 경험을 제공합니다."
    },
    sustainability: {
      title: "지속 가능성",
      content: "LUXE는 환경을 생각하는 지속 가능한 패션을 실천합니다. 재생 가능한 소재 사용, 윤리적 생산 공정, 그리고 친환경 포장을 통해 지구를 보호하는 데 기여하고 있습니다."
    },
    careers: {
      title: "채용 정보",
      content: "LUXE와 함께 성장할 인재를 찾고 있습니다. 패션 디자이너, 마케팅 전문가, 고객 서비스 담당자 등 다양한 포지션에서 열정적인 분들의 지원을 기다립니다.",
      positions: ["패션 디자이너", "마케팅 매니저", "고객 서비스", "재고 관리"]
    },
    news: {
      title: "뉴스 & 이벤트",
      content: "LUXE의 최신 소식과 이벤트를 확인하세요.",
      news: [
        { date: "2025.01.15", title: "2025 봄 컬렉션 런칭", category: "컬렉션" },
        { date: "2025.01.10", title: "신규 매장 오픈", category: "매장" },
        { date: "2025.01.05", title: "지속 가능성 리포트 발표", category: "지속가능성" },
      ]
    }
  }

  const supportContent = {
    service: {
      title: "고객 서비스",
      content: "LUXE 고객 서비스 팀이 항상 도와드리겠습니다.",
      services: [
        { icon: "💬", name: "실시간 채팅", time: "평일 09:00-18:00" },
        { icon: "📞", name: "전화 상담", phone: "02-1234-5678" },
        { icon: "📧", name: "이메일 문의", email: "service@luxe.com" },
        { icon: "💡", name: "FAQ", link: "자주 묻는 질문" },
      ]
    },
    shipping: {
      title: "배송 정보",
      content: "빠르고 안전한 배송 서비스를 제공합니다.",
      info: [
        { type: "일반 배송", time: "3-5일", price: "₩3,000", free: "50,000원 이상 무료" },
        { type: "익일 배송", time: "다음날", price: "₩10,000", free: "100,000원 이상 무료" },
        { type: "당일 배송", time: "당일", price: "₩15,000", free: "서울 지역 한정" },
      ]
    },
    returns: {
      title: "반품 정책",
      content: "구매 후 7일 이내에 반품 가능합니다.",
      policy: [
        "구매일로부터 7일 이내 반품 가능",
        "상품 미착용 및 태그 부착 상태 유지",
        "배송비는 고객 부담 (단, 상품 불량 시 무료)",
        "환불은 영업일 기준 3-5일 소요",
      ]
    },
    contact: {
      title: "연락처",
      content: "언제든지 연락주세요."
    }
  }

  const renderModal = () => {
    if (!activeModal) return null

    const [category, item] = activeModal.split("-")

    return (
      <div 
        className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 animate-in fade-in duration-200"
        onClick={() => setActiveModal(null)}
      >
        <div 
          className="bg-background rounded-lg max-w-3xl w-full p-8 max-h-[90vh] overflow-y-auto animate-in slide-in-from-bottom-4 duration-300"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Shopping Modals */}
          {category === "shopping" && shoppingContent[item as keyof typeof shoppingContent] && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="font-serif text-3xl font-bold text-primary">
                    {shoppingContent[item as keyof typeof shoppingContent].title}
                  </h2>
                  <p className="text-muted-foreground mt-2">
                    {shoppingContent[item as keyof typeof shoppingContent].description}
                  </p>
                </div>
                <button
                  onClick={() => setActiveModal(null)}
                  className="text-muted-foreground hover:text-foreground transition-colors text-2xl"
                >
                  ×
                </button>
              </div>
              
              <div className="grid md:grid-cols-2 gap-4">
                {shoppingContent[item as keyof typeof shoppingContent].items.map((product: any, idx: number) => (
                  <div key={idx} className="border border-border rounded-lg p-4 hover:border-primary transition-colors">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="font-bold text-foreground">{product.name}</h3>
                        {product.category && (
                          <p className="text-xs text-muted-foreground">{product.category}</p>
                        )}
                        {product.badge && (
                          <span className="inline-block px-2 py-1 bg-primary text-primary-foreground text-xs rounded mt-1">
                            {product.badge}
                          </span>
                        )}
                      </div>
                    </div>
                    <div className="mt-4">
                      {product.discount ? (
                        <div>
                          <p className="text-xs text-muted-foreground line-through">{product.originalPrice}</p>
                          <p className="text-lg font-bold text-primary">{product.salePrice}</p>
                          <p className="text-xs text-red-500 font-bold">{product.discount}</p>
                        </div>
                      ) : (
                        <p className="text-lg font-bold text-primary">{product.price}</p>
                      )}
                    </div>
                    <button className="w-full mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors text-sm">
                      구매하기
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Company Modals */}
          {category === "company" && companyContent[item as keyof typeof companyContent] && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-serif text-3xl font-bold text-primary">
                  {companyContent[item as keyof typeof companyContent].title}
                </h2>
                <button
                  onClick={() => setActiveModal(null)}
                  className="text-muted-foreground hover:text-foreground transition-colors text-2xl"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-4">
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {companyContent[item as keyof typeof companyContent].content}
                </p>
                
                {item === "careers" && companyContent.careers.positions && (
                  <div className="pt-4 border-t border-border">
                    <h3 className="font-bold text-foreground mb-3">채용 포지션</h3>
                    <div className="grid md:grid-cols-2 gap-3">
                      {companyContent.careers.positions.map((position, idx) => (
                        <div key={idx} className="p-3 bg-secondary rounded-lg border border-border">
                          <p className="font-medium text-foreground">{position}</p>
                          <button className="text-sm text-primary mt-2 hover:underline">
                            지원하기 →
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {item === "news" && companyContent.news.news && (
                  <div className="pt-4 border-t border-border">
                    <h3 className="font-bold text-foreground mb-3">최신 뉴스</h3>
                    <div className="space-y-3">
                      {companyContent.news.news.map((item, idx) => (
                        <div key={idx} className="p-4 bg-secondary rounded-lg border border-border hover:border-primary transition-colors">
                          <div className="flex items-start justify-between">
                            <div>
                              <span className="text-xs text-primary font-bold">{item.category}</span>
                              <h4 className="font-bold text-foreground mt-1">{item.title}</h4>
                              <p className="text-sm text-muted-foreground mt-1">{item.date}</p>
                            </div>
                            <button className="text-primary text-sm hover:underline">
                              자세히 보기 →
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Support Modals */}
          {category === "support" && supportContent[item as keyof typeof supportContent] && (
            <div>
              <div className="flex items-center justify-between mb-6">
                <h2 className="font-serif text-3xl font-bold text-primary">
                  {supportContent[item as keyof typeof supportContent].title}
                </h2>
                <button
                  onClick={() => setActiveModal(null)}
                  className="text-muted-foreground hover:text-foreground transition-colors text-2xl"
                >
                  ×
                </button>
              </div>
              
              <div className="space-y-4">
                <p className="text-lg text-muted-foreground leading-relaxed">
                  {supportContent[item as keyof typeof supportContent].content}
                </p>
                
                {item === "service" && supportContent.service.services && (
                  <div className="pt-4 border-t border-border">
                    <div className="grid md:grid-cols-2 gap-4">
                      {supportContent.service.services.map((service, idx) => (
                        <div key={idx} className="p-4 bg-secondary rounded-lg border border-border">
                          <div className="text-2xl mb-2">{service.icon}</div>
                          <h3 className="font-bold text-foreground mb-1">{service.name}</h3>
                          {service.time && <p className="text-sm text-muted-foreground">{service.time}</p>}
                          {service.phone && <p className="text-sm text-primary">{service.phone}</p>}
                          {service.email && <p className="text-sm text-primary">{service.email}</p>}
                          {service.link && (
                            <button className="text-sm text-primary mt-2 hover:underline">
                              {service.link} →
                            </button>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {item === "shipping" && supportContent.shipping.info && (
                  <div className="pt-4 border-t border-border">
                    <div className="space-y-3">
                      {supportContent.shipping.info.map((info, idx) => (
                        <div key={idx} className="p-4 bg-secondary rounded-lg border border-border">
                          <div className="flex items-start justify-between">
                            <div>
                              <h3 className="font-bold text-foreground">{info.type}</h3>
                              <p className="text-sm text-muted-foreground mt-1">배송 시간: {info.time}</p>
                              <p className="text-sm text-muted-foreground">배송비: {info.price}</p>
                              <p className="text-xs text-primary mt-1">{info.free}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {item === "returns" && supportContent.returns.policy && (
                  <div className="pt-4 border-t border-border">
                    <ul className="space-y-3">
                      {supportContent.returns.policy.map((policy, idx) => (
                        <li key={idx} className="flex items-start gap-3">
                          <span className="text-primary">→</span>
                          <span className="text-muted-foreground">{policy}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {item === "contact" && (
                  <div className="pt-4 border-t border-border">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="p-4 bg-secondary rounded-lg">
                        <h3 className="font-bold text-foreground mb-2">이메일</h3>
                        <p className="text-primary">contact@luxe.com</p>
                      </div>
                      <div className="p-4 bg-secondary rounded-lg">
                        <h3 className="font-bold text-foreground mb-2">전화</h3>
                        <p className="text-primary">02-1234-5678</p>
                      </div>
                      <div className="p-4 bg-secondary rounded-lg">
                        <h3 className="font-bold text-foreground mb-2">주소</h3>
                        <p className="text-muted-foreground text-sm">서울특별시 강남구 테헤란로 123</p>
                      </div>
                      <div className="p-4 bg-secondary rounded-lg">
                        <h3 className="font-bold text-foreground mb-2">운영 시간</h3>
                        <p className="text-muted-foreground text-sm">월-금: 09:00 - 18:00</p>
                      </div>
                    </div>
                    <button 
                      onClick={() => {
                        setActiveModal(null)
                        setTimeout(() => handleSmoothScroll("contact"), 300)
                      }}
                      className="w-full mt-4 px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
                    >
                      문의 폼 작성하기
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    )
  }

  return (
    <>
      <footer className="bg-primary text-primary-foreground pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
            {/* Brand */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 bg-primary-foreground rounded-sm"></div>
                <span className="font-serif text-xl font-bold">LUXE</span>
              </div>
              <p className="text-sm text-primary-foreground/80">
                현대적 감성과 고전적 우아함을 담은 프리미엄 패션 브랜드
              </p>
            </div>

            {/* Shop */}
            <div>
              <h4 className="font-bold mb-4">쇼핑</h4>
              <ul className="space-y-2 text-sm text-primary-foreground/80">
                <li>
                  <button 
                    onClick={() => setActiveModal("shopping-women")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    여성
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("shopping-men")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    남성
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("shopping-new")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    신상품
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("shopping-sale")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    세일
                  </button>
                </li>
              </ul>
            </div>

            {/* Company */}
            <div>
              <h4 className="font-bold mb-4">회사</h4>
              <ul className="space-y-2 text-sm text-primary-foreground/80">
                <li>
                  <button 
                    onClick={() => {
                      setActiveModal("company-about")
                    }}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    소개
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("company-sustainability")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    지속 가능성
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("company-careers")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    채용 정보
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("company-news")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    뉴스
                  </button>
                </li>
              </ul>
            </div>

            {/* Support */}
            <div>
              <h4 className="font-bold mb-4">지원</h4>
              <ul className="space-y-2 text-sm text-primary-foreground/80">
                <li>
                  <button 
                    onClick={() => setActiveModal("support-service")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    고객 서비스
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("support-shipping")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    배송 정보
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("support-returns")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    반품 정책
                  </button>
                </li>
                <li>
                  <button 
                    onClick={() => setActiveModal("support-contact")}
                    className="hover:text-primary-foreground transition-colors cursor-pointer text-left"
                  >
                    연락처
                  </button>
                </li>
              </ul>
            </div>
          </div>

          <div className="border-t border-primary-foreground/20 pt-8">
            <div className="flex flex-col md:flex-row items-center justify-between">
              <p className="text-sm text-primary-foreground/80">© 2025 LUXE. All rights reserved.</p>
              <div className="flex gap-6 mt-4 md:mt-0">
                <button className="text-sm text-primary-foreground/80 hover:text-primary-foreground transition-colors cursor-pointer">
                  개인정보처리방침
                </button>
                <button className="text-sm text-primary-foreground/80 hover:text-primary-foreground transition-colors cursor-pointer">
                  이용약관
                </button>
                <button className="text-sm text-primary-foreground/80 hover:text-primary-foreground transition-colors cursor-pointer">
                  쿠키 설정
                </button>
              </div>
            </div>
          </div>
        </div>
      </footer>
      {renderModal()}
    </>
  )
}
