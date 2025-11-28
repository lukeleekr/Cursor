import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [memos, setMemos] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [newMemoTitle, setNewMemoTitle] = useState('');
  const [newMemoContent, setNewMemoContent] = useState('');

  // 로컬 스토리지에서 메모 불러오기
  useEffect(() => {
    const savedMemos = localStorage.getItem('memos');
    if (savedMemos) {
      setMemos(JSON.parse(savedMemos));
    }
  }, []);

  // 메모가 변경될 때마다 로컬 스토리지에 저장
  useEffect(() => {
    localStorage.setItem('memos', JSON.stringify(memos));
  }, [memos]);

  // 새 메모 생성
  const handleNewMemo = () => {
    const newMemo = {
      id: Date.now(),
      title: '',
      content: '',
      createdAt: new Date().toISOString(),
    };
    setMemos([newMemo, ...memos]);
    setEditingId(newMemo.id);
    setNewMemoTitle('');
    setNewMemoContent('');
  };

  // 메모 수정 모드로 전환
  const handleEdit = (id) => {
    setEditingId(id);
    const memo = memos.find(m => m.id === id);
    if (memo) {
      setNewMemoTitle(memo.title);
      setNewMemoContent(memo.content);
    }
  };

  // 메모 저장
  const handleSave = (id) => {
    setMemos(memos.map(memo => {
      if (memo.id === id) {
        return {
          ...memo,
          title: newMemoTitle.trim() || '제목 없음',
          content: newMemoContent.trim(),
          updatedAt: new Date().toISOString(),
        };
      }
      return memo;
    }));
    setEditingId(null);
    setNewMemoTitle('');
    setNewMemoContent('');
  };

  // 메모 삭제
  const handleDelete = (id) => {
    if (window.confirm('정말 이 메모를 삭제하시겠습니까?')) {
      setMemos(memos.filter(memo => memo.id !== id));
      if (editingId === id) {
        setEditingId(null);
        setNewMemoTitle('');
        setNewMemoContent('');
      }
    }
  };

  // 검색 필터링
  const filteredMemos = memos.filter(memo => {
    const query = searchQuery.toLowerCase();
    return (
      memo.title.toLowerCase().includes(query) ||
      memo.content.toLowerCase().includes(query)
    );
  });

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-700 py-8 px-4">
      <div className="w-full max-w-7xl mx-auto">
        {/* TailwindCSS 테스트 배지 - 나중에 제거 가능 */}
        <div className="fixed top-4 right-4 bg-green-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 text-sm font-bold">
          ✅ TailwindCSS Active
        </div>

        {/* 헤더 */}
        <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-xl mb-6 p-6 border border-white/20">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-4xl font-bold text-purple-600 mb-2 flex items-center gap-2">
                <span>📝</span>
                메모 앱
              </h1>
              <span className="inline-block px-3 py-1 bg-gray-200 text-gray-700 rounded-full text-sm font-medium">
                {memos.length}개의 메모
              </span>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 flex-1 md:flex-initial md:max-w-md">
              <div className="relative flex-1">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <span className="text-gray-400">🔍</span>
                </div>
                <input
                  type="text"
                  placeholder="메모 검색..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-3 border-2 border-purple-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                />
              </div>
              <button
                onClick={handleNewMemo}
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 whitespace-nowrap"
              >
                ✏️ 새 메모
              </button>
            </div>
          </div>
        </div>

        {/* 메모 리스트 */}
        {filteredMemos.length === 0 ? (
          <div className="bg-white/95 backdrop-blur-sm rounded-2xl shadow-xl p-12 text-center border border-white/20">
            <div className="text-6xl mb-4">
              {searchQuery ? '🔍' : '📝'}
            </div>
            <h2 className="text-2xl font-bold text-gray-700 mb-2">
              {searchQuery ? '검색 결과가 없습니다' : '메모가 없습니다'}
            </h2>
            <p className="text-gray-500">
              {searchQuery 
                ? '다른 검색어를 시도해보세요.' 
                : '새 메모를 만들어보세요!'}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredMemos.map(memo => (
              <div
                key={memo.id}
                className={`bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 flex flex-col h-full ${
                  editingId === memo.id 
                    ? 'ring-4 ring-purple-500 ring-opacity-50 border-2 border-purple-500' 
                    : ''
                }`}
              >
                {editingId === memo.id ? (
                  // 수정 모드
                  <div className="p-6 flex flex-col h-full">
                    <input
                      type="text"
                      placeholder="제목을 입력하세요"
                      value={newMemoTitle}
                      onChange={(e) => setNewMemoTitle(e.target.value)}
                      className="text-xl font-bold mb-4 px-4 py-2 border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      autoFocus
                    />
                    <textarea
                      placeholder="내용을 입력하세요"
                      value={newMemoContent}
                      onChange={(e) => setNewMemoContent(e.target.value)}
                      className="flex-1 min-h-[200px] px-4 py-3 border-2 border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                    />
                    <div className="mt-4 flex flex-col gap-2">
                      <button
                        onClick={() => handleSave(memo.id)}
                        className="w-full px-4 py-3 bg-green-500 hover:bg-green-600 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                      >
                        💾 저장
                      </button>
                      <button
                        onClick={() => {
                          setEditingId(null);
                          setNewMemoTitle('');
                          setNewMemoContent('');
                        }}
                        className="w-full px-4 py-3 bg-gray-200 hover:bg-gray-300 text-gray-700 font-semibold rounded-lg transition-all duration-200"
                      >
                        취소
                      </button>
                    </div>
                  </div>
                ) : (
                  // 보기 모드
                  <div className="p-6 flex flex-col h-full">
                    <div className="mb-4">
                      <h3 className="text-xl font-bold text-gray-800 mb-2">
                        {memo.title || <span className="text-gray-400">제목 없음</span>}
                      </h3>
                      <div className="flex items-center gap-2 text-sm text-gray-500">
                        <span className="px-2 py-1 bg-gray-100 rounded-md">📅</span>
                        <span>
                          {new Date(memo.createdAt).toLocaleDateString('ko-KR', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </span>
                      </div>
                    </div>
                    <div className="flex-1 mb-4 text-gray-600 whitespace-pre-wrap break-words">
                      {memo.content || <em className="text-gray-400">내용이 없습니다.</em>}
                    </div>
                    <div className="flex flex-col gap-2 pt-4 border-t border-gray-200">
                      <button
                        onClick={() => handleEdit(memo.id)}
                        className="w-full px-4 py-3 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                      >
                        ✏️ 수정
                      </button>
                      <button
                        onClick={() => handleDelete(memo.id)}
                        className="w-full px-4 py-3 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-lg shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all duration-200"
                      >
                        🗑️ 삭제
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
