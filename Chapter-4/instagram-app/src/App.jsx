import { useState } from 'react'
import './App.css'

function App() {
  // 피드 데이터 생성
  const posts = [
    { id: 1, username: 'travel_lover', profilePic: '/man.png', image: '/img01.png', likes: 1240, caption: 'Beautiful sunset! 🌅 #travel #sunset' },
    { id: 2, username: 'foodie_gram', profilePic: '/woman.png', image: '/img02.jpg', likes: 892, caption: 'Delicious brunch! 🥐 #food #brunch' },
    { id: 3, username: 'nature_photographer', profilePic: '/man.png', image: '/img03.jpg', likes: 2156, caption: 'Morning hike 🏔️ #nature #hiking' },
    { id: 4, username: 'city_explorer', profilePic: '/woman.png', image: '/img04.png', likes: 1534, caption: 'City lights ✨ #urban #night' },
    { id: 5, username: 'coffee_addict', profilePic: '/man.png', image: '/img05.jpg', likes: 678, caption: 'Perfect cup ☕ #coffee #morning' },
    { id: 6, username: 'art_lover', profilePic: '/woman.png', image: '/img06.jpg', likes: 987, caption: 'New artwork 🎨 #art #creative' },
    { id: 7, username: 'fitness_guru', profilePic: '/man.png', image: '/img07.jpg', likes: 1123, caption: 'Workout complete! 💪 #fitness #gym' },
    { id: 8, username: 'bookworm', profilePic: '/woman.png', image: '/img08.jpg', likes: 445, caption: 'Reading corner 📚 #books #reading' },
    { id: 9, username: 'pet_parent', profilePic: '/man.png', image: '/img09.jpg', likes: 2341, caption: 'My best friend 🐕 #pets #dog' },
    { id: 10, username: 'adventure_seeker', profilePic: '/woman.png', image: '/img10.jpg', likes: 1890, caption: 'New adventure awaits! 🗺️ #adventure #explore' },
  ]

  const [likedPosts, setLikedPosts] = useState(new Set())

  const toggleLike = (postId) => {
    const newLikedPosts = new Set(likedPosts)
    if (newLikedPosts.has(postId)) {
      newLikedPosts.delete(postId)
    } else {
      newLikedPosts.add(postId)
    }
    setLikedPosts(newLikedPosts)
  }

  return (
    <div className="app">
      {/* 헤더 */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <h1>Instagram</h1>
          </div>
          <div className="search-bar">
            <input type="text" placeholder="Search" />
          </div>
          <div className="header-icons">
            <span className="icon">🏠</span>
            <span className="icon">💬</span>
            <span className="icon">➕</span>
            <span className="icon">🔍</span>
            <span className="icon">❤️</span>
            <span className="icon">👤</span>
          </div>
        </div>
      </header>

      {/* 메인 컨텐츠 */}
      <main className="main-content">
        {/* 피드 섹션 */}
        <div className="feed">
          {posts.map(post => (
            <div key={post.id} className="post">
              {/* 포스트 헤더 */}
              <div className="post-header">
                <img 
                  src={post.profilePic} 
                  alt={post.username} 
                  className="profile-pic-small"
                />
                <span className="username">{post.username}</span>
                <span className="more-icon">⋯</span>
              </div>

              {/* 포스트 이미지 */}
              <div className="post-image-container">
                <img 
                  src={post.image} 
                  alt={post.caption} 
                  className="post-image"
                />
              </div>

              {/* 포스트 액션 */}
              <div className="post-actions">
                <button 
                  className={`like-btn ${likedPosts.has(post.id) ? 'liked' : ''}`}
                  onClick={() => toggleLike(post.id)}
                >
                  {likedPosts.has(post.id) ? '❤️' : '🤍'}
                </button>
                <button className="action-btn">💬</button>
                <button className="action-btn">📤</button>
                <button className="action-btn bookmark">🔖</button>
              </div>

              {/* 좋아요 수 */}
              <div className="post-likes">
                {likedPosts.has(post.id) ? post.likes + 1 : post.likes} likes
              </div>

              {/* 캡션 */}
              <div className="post-caption">
                <span className="caption-username">{post.username}</span>
                <span className="caption-text">{post.caption}</span>
              </div>

              {/* 댓글 보기 */}
              <div className="post-comments">
                <button className="view-comments">View all comments</button>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}

export default App
