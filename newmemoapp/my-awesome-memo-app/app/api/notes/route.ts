import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCurrentUser } from "@/lib/auth";

// 메모 목록 조회
export async function GET() {
  try {
    const user = await getCurrentUser();
    
    if (!user) {
      return NextResponse.json(
        { error: "인증되지 않았습니다." },
        { status: 401 }
      );
    }

    const notes = await prisma.note.findMany({
      where: { userId: user.id },
      orderBy: { createdAt: "desc" },
    });

    return NextResponse.json({ notes });
  } catch (error) {
    console.error("Get notes error:", error);
    return NextResponse.json(
      { error: "메모를 가져오는 중 오류가 발생했습니다." },
      { status: 500 }
    );
  }
}

// 새 메모 생성
export async function POST(request: NextRequest) {
  try {
    const user = await getCurrentUser();
    
    if (!user) {
      return NextResponse.json(
        { error: "인증되지 않았습니다." },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { title, content, color } = body;

    if (!title && !content) {
      return NextResponse.json(
        { error: "제목 또는 내용을 입력해주세요." },
        { status: 400 }
      );
    }

    const note = await prisma.note.create({
      data: {
        title: title || "제목 없음",
        content: content || "",
        color: color || "bg-blue-100",
        userId: user.id,
      },
    });

    return NextResponse.json({ note }, { status: 201 });
  } catch (error) {
    console.error("Create note error:", error);
    return NextResponse.json(
      { error: "메모를 생성하는 중 오류가 발생했습니다." },
      { status: 500 }
    );
  }
}

