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
    <div className="App">
      <div className="memo-container">
        <header className="memo-header">
          <h1>📝 메모 앱</h1>
          <div className="header-actions">
            <input
              type="text"
              className="search-input"
              placeholder="메모 검색..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button className="btn btn-primary" onClick={handleNewMemo}>
              ✏️ 새 메모
            </button>
          </div>
        </header>

        <div className="memo-list">
          {filteredMemos.length === 0 ? (
            <div className="empty-state">
              {searchQuery ? '검색 결과가 없습니다.' : '메모가 없습니다. 새 메모를 만들어보세요!'}
            </div>
          ) : (
            filteredMemos.map(memo => (
              <div key={memo.id} className={`memo-card ${editingId === memo.id ? 'editing' : ''}`}>
                {editingId === memo.id ? (
                  // 수정 모드
                  <div className="memo-edit">
                    <input
                      type="text"
                      className="memo-title-input"
                      placeholder="제목을 입력하세요"
                      value={newMemoTitle}
                      onChange={(e) => setNewMemoTitle(e.target.value)}
                      autoFocus
                    />
                    <textarea
                      className="memo-content-input"
                      placeholder="내용을 입력하세요"
                      value={newMemoContent}
                      onChange={(e) => setNewMemoContent(e.target.value)}
                    />
                    <div className="memo-actions">
                      <button
                        className="btn btn-save"
                        onClick={() => handleSave(memo.id)}
                      >
                        💾 저장
                      </button>
                      <button
                        className="btn btn-cancel"
                        onClick={() => {
                          setEditingId(null);
                          setNewMemoTitle('');
                          setNewMemoContent('');
                        }}
                      >
                        취소
                      </button>
                    </div>
                  </div>
                ) : (
                  // 보기 모드
                  <div className="memo-view">
                    <div className="memo-header-view">
                      <h3 className="memo-title">
                        {memo.title || '제목 없음'}
                      </h3>
                      <div className="memo-date">
                        {new Date(memo.createdAt).toLocaleDateString('ko-KR', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </div>
                    </div>
                    <div className="memo-content">
                      {memo.content || <em className="empty-content">내용이 없습니다.</em>}
                    </div>
                    <div className="memo-actions">
                      <button
                        className="btn btn-edit"
                        onClick={() => handleEdit(memo.id)}
                      >
                        ✏️ 수정
                      </button>
                      <button
                        className="btn btn-delete"
                        onClick={() => handleDelete(memo.id)}
                      >
                        🗑️ 삭제
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
