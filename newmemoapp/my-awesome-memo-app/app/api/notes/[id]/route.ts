import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCurrentUser } from "@/lib/auth";

// 메모 삭제
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const user = await getCurrentUser();
    
    if (!user) {
      return NextResponse.json(
        { error: "인증되지 않았습니다." },
        { status: 401 }
      );
    }

    const note = await prisma.note.findUnique({
      where: { id: params.id },
    });

    if (!note) {
      return NextResponse.json(
        { error: "메모를 찾을 수 없습니다." },
        { status: 404 }
      );
    }

    if (note.userId !== user.id) {
      return NextResponse.json(
        { error: "권한이 없습니다." },
        { status: 403 }
      );
    }

    await prisma.note.delete({
      where: { id: params.id },
    });

    return NextResponse.json({ message: "메모가 삭제되었습니다." });
  } catch (error) {
    console.error("Delete note error:", error);
    return NextResponse.json(
      { error: "메모를 삭제하는 중 오류가 발생했습니다." },
      { status: 500 }
    );
  }
}

