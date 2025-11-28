"use client"

import { useState } from "react"

export default function Contact() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: ""
  })
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // 실제로는 여기서 API 호출을 하겠지만, 데모용으로는 상태만 변경
    setSubmitted(true)
    setTimeout(() => {
      setSubmitted(false)
      setFormData({ name: "", email: "", message: "" })
    }, 3000)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  return (
    <section id="contact" className="py-20 bg-secondary scroll-mt-20">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="font-serif text-4xl md:text-5xl font-bold text-primary mb-4 text-balance">연락처</h2>
          <p className="text-lg text-muted-foreground">
            궁금한 점이 있으시면 언제든지 연락주세요. 빠르게 답변드리겠습니다.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-12">
          {/* Contact Info */}
          <div className="space-y-6">
            <div>
              <h3 className="font-bold text-foreground mb-4">연락처 정보</h3>
              <div className="space-y-4">
                <div className="flex gap-3">
                  <div className="text-primary text-xl">📧</div>
                  <div>
                    <p className="font-medium text-foreground">이메일</p>
                    <p className="text-muted-foreground">contact@luxe.com</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="text-primary text-xl">📞</div>
                  <div>
                    <p className="font-medium text-foreground">전화</p>
                    <p className="text-muted-foreground">02-1234-5678</p>
                  </div>
                </div>
                <div className="flex gap-3">
                  <div className="text-primary text-xl">📍</div>
                  <div>
                    <p className="font-medium text-foreground">주소</p>
                    <p className="text-muted-foreground">서울특별시 강남구 테헤란로 123</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-6 border-t border-border">
              <h3 className="font-bold text-foreground mb-4">운영 시간</h3>
              <div className="space-y-2 text-muted-foreground">
                <p>월-금: 09:00 - 18:00</p>
                <p>토요일: 10:00 - 17:00</p>
                <p>일요일: 휴무</p>
              </div>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-foreground mb-2">
                  이름
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-border rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="이름을 입력하세요"
                />
              </div>
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-foreground mb-2">
                  이메일
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-border rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary"
                  placeholder="이메일을 입력하세요"
                />
              </div>
              <div>
                <label htmlFor="message" className="block text-sm font-medium text-foreground mb-2">
                  메시지
                </label>
                <textarea
                  id="message"
                  name="message"
                  value={formData.message}
                  onChange={handleChange}
                  required
                  rows={5}
                  className="w-full px-4 py-2 border border-border rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-primary resize-none"
                  placeholder="메시지를 입력하세요"
                />
              </div>
              <button
                type="submit"
                className="w-full px-6 py-3 bg-primary text-primary-foreground font-medium rounded-lg hover:bg-primary/90 transition-colors"
              >
                {submitted ? "전송 완료! ✓" : "메시지 보내기"}
              </button>
            </form>
          </div>
        </div>
      </div>
    </section>
  )
}

