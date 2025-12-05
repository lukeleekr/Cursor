import { type NextRequest, NextResponse } from "next/server"
import OpenAI from "openai"

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
})

export async function POST(request: NextRequest) {
  try {
    const { keyword, instructions, model } = await request.json()

    if (!keyword || keyword.trim() === "") {
      return NextResponse.json({ error: "키워드를 입력해주세요." }, { status: 400 })
    }

    if (!process.env.OPENAI_API_KEY) {
      return NextResponse.json({ error: "OpenAI API 키가 설정되지 않았습니다." }, { status: 500 })
    }

    const systemPrompt = `당신은 10년 경력의 전문 칼럼니스트입니다. 
복잡한 주제를 일반 독자들이 이해하기 쉽게 설명하는 능력이 뛰어납니다.

칼럼 작성 시 다음 원칙을 따르세요:

1. **구조**: 
   - 흥미로운 도입부로 시작
   - 본론에서 핵심 내용을 3-4개 섹션으로 나누어 분석
   - 통찰력 있는 결론으로 마무리

2. **톤앤매너**:
   - 전문적이면서도 친근한 어조
   - 독자와 대화하듯이 작성
   - 지나치게 딱딱하거나 학술적이지 않게

3. **전문 용어 처리**:
   - 전문 용어가 나오면 반드시 쉬운 말로 풀어서 설명
   - 일상적인 비유나 예시를 들어 이해를 도움
   - 예: "인플레이션(물가상승률) - 쉽게 말해, 작년에 1000원이던 라면이 올해 1100원이 되는 현상입니다"

4. **분석적 관점**:
   - 단순 정보 나열이 아닌, '왜?'와 '어떻게?'에 초점
   - 다양한 시각에서 주제를 조명
   - 현실적인 사례와 데이터 활용
   - 독자가 생각해볼 만한 질문 제시

5. **길이**: 
   - 약 1500-2000자 분량
   - 각 섹션에 소제목 포함`

    const userPrompt = `다음 키워드에 대한 분석적 칼럼을 작성해주세요.

키워드: ${keyword}

${instructions ? `추가 지시사항:\n${instructions}\n\n` : ""}요청사항:
- 이 키워드와 관련된 핵심 이슈나 트렌드를 분석해주세요
- 일반 독자가 이해할 수 있도록 전문 용어는 쉽게 풀어서 설명해주세요
- 구체적인 예시나 사례를 포함해주세요
- 독자에게 새로운 통찰을 줄 수 있는 관점을 제시해주세요`

    // 모델 선택 (gpt-5-nano는 reasoning 모델이므로 developer 역할 사용)
    const isReasoningModel = model === "gpt-5-nano"
    const messages = isReasoningModel
      ? [
          { role: "developer" as const, content: systemPrompt },
          { role: "user" as const, content: userPrompt },
        ]
      : [
          { role: "system" as const, content: systemPrompt },
          { role: "user" as const, content: userPrompt },
        ]

    const response = await openai.chat.completions.create({
      model: model || "gpt-4o",
      messages,
      max_completion_tokens: 16000,
    })

    const content = response.choices[0]?.message?.content

    if (!content || content.trim() === "") {
      return NextResponse.json(
        { error: "API 응답이 비어있습니다." },
        { status: 500 }
      )
    }

    return NextResponse.json({ content })
  } catch (error) {
    console.error("Error generating article:", error)
    const errorMessage = error instanceof Error ? error.message : "알 수 없는 오류가 발생했습니다."
    return NextResponse.json({ error: `칼럼 생성 중 오류가 발생했습니다: ${errorMessage}` }, { status: 500 })
  }
}
