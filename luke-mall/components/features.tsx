export default function Features() {
  const features = [
    {
      number: "01",
      title: "프리미엄 소재",
      description: "세계 최고의 공급처에서 엄선한 고급 원단만을 사용합니다.",
      icon: "✨",
    },
    {
      number: "02",
      title: "수공예 제작",
      description: "숙련된 장인의 손길로 정성들여 만들어진 제품입니다.",
      icon: "🧵",
    },
    {
      number: "03",
      title: "지속 가능성",
      description: "환경을 생각하는 지속 가능한 패션을 실천합니다.",
      icon: "🌿",
    },
    {
      number: "04",
      title: "시간초월적 디자인",
      description: "트렌드를 넘어 오랫동안 사랑받을 디자인입니다.",
      icon: "⏳",
    },
  ]

  return (
    <section id="features" className="py-20 bg-background scroll-mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="font-serif text-4xl md:text-5xl font-bold text-primary mb-4 text-balance">우리의 가치</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            LUXE가 추구하는 네 가지 핵심 가치로 최고의 패션 경험을 제공합니다.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => (
            <div
              key={feature.number}
              className="bg-secondary rounded-lg p-8 border border-border hover:border-primary transition-colors cursor-pointer"
            >
              <div className="text-4xl mb-4">{feature.icon}</div>
              <div className="text-sm font-bold text-primary mb-2">{feature.number}</div>
              <h3 className="font-serif text-xl font-bold mb-3 text-foreground">{feature.title}</h3>
              <p className="text-muted-foreground text-sm leading-relaxed">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
