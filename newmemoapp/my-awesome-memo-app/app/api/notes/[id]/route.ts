import { NextRequest, NextResponse } from "next/server";
import { prisma } from "@/lib/prisma";
import { getCurrentUser } from "@/lib/auth";

// 메모 수정
export async function PUT(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const user = await getCurrentUser();
    const { id } = await params;
    
    if (!user) {
      return NextResponse.json(
        { error: "인증되지 않았습니다." },
        { status: 401 }
      );
    }

    const body = await request.json();
    const { title, content } = body;

    const note = await prisma.note.findUnique({
      where: { id },
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

    const updatedNote = await prisma.note.update({
      where: { id },
      data: { title, content },
    });

    return NextResponse.json(updatedNote);
  } catch (error) {
    console.error("Update note error:", error);
    return NextResponse.json(
      { error: "메모를 수정하는 중 오류가 발생했습니다." },
      { status: 500 }
    );
  }
}

// 메모 삭제
export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const user = await getCurrentUser();
    const { id } = await params;
    
    if (!user) {
      return NextResponse.json(
        { error: "인증되지 않았습니다." },
        { status: 401 }
      );
    }

    const note = await prisma.note.findUnique({
      where: { id },
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
      where: { id },
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
