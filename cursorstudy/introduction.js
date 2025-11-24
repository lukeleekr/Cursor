// 모바일 햄버거 메뉴 토글
const hamburger = document.querySelector('.hamburger');
const mobileNavMenu = document.querySelector('.mobile-nav-menu');
const sidebar = document.querySelector('.sidebar');

if (hamburger && mobileNavMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        mobileNavMenu.classList.toggle('active');
        
        // 모바일에서 사이드바도 토글
        if (window.innerWidth <= 768 && sidebar) {
            sidebar.classList.toggle('active');
        }
    });

    // 모바일 메뉴 링크 클릭 시 메뉴 닫기
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            mobileNavMenu.classList.remove('active');
            if (sidebar) {
                sidebar.classList.remove('active');
            }
        });
    });
}

// 부드러운 스크롤
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        const offsetTop = section.offsetTop - 20;
        window.scrollTo({
            top: offsetTop,
            behavior: 'smooth'
        });
    }
}

// 네비게이션 링크 클릭 시 부드러운 스크롤
document.querySelectorAll('.nav-link, .mobile-nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        const href = link.getAttribute('href');
        if (href && href.startsWith('#')) {
            const targetId = href.substring(1);
            scrollToSection(targetId);
        }
    });
});

// 스크롤 애니메이션
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// 애니메이션 적용할 요소들
document.addEventListener('DOMContentLoaded', () => {
    const animateElements = document.querySelectorAll(
        '.content-box, .strengths-box, .weakness-box, .philosophy-box, .experience-card, .timeline-item'
    );
    
    animateElements.forEach(el => {
        el.classList.add('fade-in');
        observer.observe(el);
    });
});

// 현재 섹션 하이라이트
let currentSection = '';

function updateActiveNav() {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
    
    let newCurrent = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        const scrollPosition = window.scrollY + 150;
        
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            newCurrent = section.getAttribute('id');
        }
    });
    
    if (newCurrent !== currentSection) {
        currentSection = newCurrent;
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            const href = link.getAttribute('href');
            if (href === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }
}

window.addEventListener('scroll', updateActiveNav);
window.addEventListener('load', updateActiveNav);

// 페이지 로드 시 애니메이션
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    setTimeout(() => {
        document.body.style.transition = 'opacity 0.5s ease';
        document.body.style.opacity = '1';
    }, 100);
});

// 리사이즈 시 사이드바 처리
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        if (sidebar) {
            sidebar.classList.remove('active');
        }
        if (mobileNavMenu) {
            mobileNavMenu.classList.remove('active');
        }
        if (hamburger) {
            hamburger.classList.remove('active');
        }
    }
});

// 키보드 접근성 개선
document.addEventListener('keydown', (e) => {
    // ESC 키로 모바일 메뉴 닫기
    if (e.key === 'Escape') {
        if (mobileNavMenu && mobileNavMenu.classList.contains('active')) {
            mobileNavMenu.classList.remove('active');
            if (hamburger) {
                hamburger.classList.remove('active');
            }
            if (sidebar && window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        }
    }
});
