// 게임 설정
const ROWS = 8;
const COLS = 8;
const TARGET_SUM = 10;

// 게임 상태
let apples = [];
let selectedApples = new Set();
let isDragging = false;
let dragStart = null;
let score = 0;
let combo = 0;
let removedApplesCount = 0;

// 게임 보드 초기화
function initGame() {
    const gameBoard = document.getElementById('gameBoard');
    gameBoard.innerHTML = '';
    apples = [];
    selectedApples.clear();
    score = 0;
    combo = 0;
    removedApplesCount = 0;

    // 1부터 9까지 숫자가 적힌 사과 생성
    for (let row = 0; row < ROWS; row++) {
        for (let col = 0; col < COLS; col++) {
            const number = Math.floor(Math.random() * 9) + 1; // 1~9 랜덤
            const apple = {
                id: row * COLS + col,
                row: row,
                col: col,
                number: number,
                element: null
            };
            apples.push(apple);

            // DOM 요소 생성
            const appleElement = document.createElement('div');
            appleElement.className = 'apple';
            // appleElement.textContent = number; // 기존: 숫자 직접 삽입
            appleElement.innerHTML = `<span class="number">${number}</span>`; // 변경: span으로 감쌈
            appleElement.dataset.id = apple.id;
            apple.element = appleElement;

            gameBoard.appendChild(appleElement);
        }
    }

    updateUI();
}

// 마우스 이벤트 처리
let gameBoard = null;

function setupEventListeners() {
    gameBoard = document.getElementById('gameBoard');

    // 게임보드에서 드래그 시작
    gameBoard.addEventListener('mousedown', handleMouseDown);

    // 전역 마우스 이동 및 업 이벤트 (게임보드 밖에서도 작동)
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
}

function handleMouseDown(e) {
    e.preventDefault();
    const rect = gameBoard.getBoundingClientRect();

    // 게임보드 내부에서만 드래그 시작
    if (e.clientX >= rect.left && e.clientX <= rect.right &&
        e.clientY >= rect.top && e.clientY <= rect.bottom) {
        isDragging = true;
        dragStart = {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top,
            appleId: null
        };

        // 클릭한 사과 찾기 (blank가 아닌 사과만)
        const clickedApple = e.target.closest('.apple');
        if (clickedApple && !clickedApple.classList.contains('blank')) {
            dragStart.appleId = parseInt(clickedApple.dataset.id);
            selectedApples.clear();
            selectApple(dragStart.appleId);
        } else {
            selectedApples.clear();
        }

        updateSelection();
    }
}

function handleMouseMove(e) {
    if (!isDragging || !gameBoard) return;

    e.preventDefault();
    const rect = gameBoard.getBoundingClientRect();
    const currentX = e.clientX - rect.left;
    const currentY = e.clientY - rect.top;

    // 드래그 범위 계산
    const minX = Math.min(dragStart.x, currentX);
    const maxX = Math.max(dragStart.x, currentX);
    const minY = Math.min(dragStart.y, currentY);
    const maxY = Math.max(dragStart.y, currentY);

    selectedApples.clear();

    // 각 사과가 드래그 범위 내에 있는지 확인
    apples.forEach(apple => {
        if (apple.removed || !apple.element || apple.element.classList.contains('blank')) return;

        const appleRect = apple.element.getBoundingClientRect();
        const appleCenterX = appleRect.left + appleRect.width / 2 - rect.left;
        const appleCenterY = appleRect.top + appleRect.height / 2 - rect.top;

        // 사과의 중심점이 드래그 범위 내에 있으면 선택
        if (appleCenterX >= minX && appleCenterX <= maxX &&
            appleCenterY >= minY && appleCenterY <= maxY) {
            selectedApples.add(apple.id);
        }
    });

    updateSelection();

    // 선택 박스는 게임보드 내부에서만 표시
    if (currentX >= 0 && currentX <= rect.width &&
        currentY >= 0 && currentY <= rect.height) {
        drawSelectionBox(dragStart.x, dragStart.y, currentX, currentY);
    }
}

function handleMouseUp(e) {
    if (isDragging) {
        isDragging = false;
        removeSelectionBox();
        checkAndRemoveApples();
    }
}

// 사과 선택
function selectApple(appleId) {
    const apple = apples.find(a => a.id === appleId && !a.removed && a.element && !a.element.classList.contains('blank'));
    if (apple) {
        selectedApples.add(appleId);
    }
}

// 선택 상태 업데이트
function updateSelection() {
    apples.forEach(apple => {
        if (apple.removed || !apple.element || apple.element.classList.contains('blank')) return;
        if (selectedApples.has(apple.id)) {
            apple.element.classList.add('selected');
        } else {
            apple.element.classList.remove('selected');
        }
    });

    updateSelectedSum();
}

// 선택한 사과들의 합 계산
function updateSelectedSum() {
    let sum = 0;
    selectedApples.forEach(appleId => {
        const apple = apples.find(a => a.id === appleId && !a.removed && a.element && !a.element.classList.contains('blank'));
        if (apple) {
            sum += apple.number;
        }
    });
    document.getElementById('selectedSum').textContent = sum;
}

// 선택 박스 그리기
let selectionBoxElement = null;

function drawSelectionBox(x1, y1, x2, y2) {
    removeSelectionBox();

    const rect = gameBoard.getBoundingClientRect();
    const left = Math.min(x1, x2);
    const top = Math.min(y1, y2);
    const width = Math.abs(x2 - x1);
    const height = Math.abs(y2 - y1);

    selectionBoxElement = document.createElement('div');
    selectionBoxElement.className = 'selection-box';
    selectionBoxElement.style.left = left + 'px';
    selectionBoxElement.style.top = top + 'px';
    selectionBoxElement.style.width = width + 'px';
    selectionBoxElement.style.height = height + 'px';

    gameBoard.appendChild(selectionBoxElement);
}

function removeSelectionBox() {
    if (selectionBoxElement) {
        selectionBoxElement.remove();
        selectionBoxElement = null;
    }
}

// 선택한 사과들의 합이 10인지 확인하고 제거
function checkAndRemoveApples() {
    let sum = 0;
    const selectedAppleObjects = [];

    selectedApples.forEach(appleId => {
        const apple = apples.find(a => a.id === appleId && !a.removed && a.element && !a.element.classList.contains('blank'));
        if (apple) {
            sum += apple.number;
            selectedAppleObjects.push(apple);
        }
    });

    if (sum === TARGET_SUM && selectedAppleObjects.length > 0) {
        // 합이 10이면 사과 제거 (빈 공간으로 표시)
        selectedAppleObjects.forEach(apple => {
            apple.removed = true;
            apple.element.classList.add('removing');
            removedApplesCount++;

            setTimeout(() => {
                // 사과를 빈 공간으로 표시 (제거하지 않고 빈 공간 스타일 적용)
                apple.element.classList.remove('apple', 'removing', 'selected');
                apple.element.classList.add('blank');
                apple.element.innerHTML = ''; // 내부 내용(숫자 span) 제거
                apple.element.style.pointerEvents = 'none';
            }, 300);
        });

        // 점수 계산
        const baseScore = selectedAppleObjects.length * 10;
        const comboBonus = combo > 0 ? combo * 5 : 0;
        score += baseScore + comboBonus;
        combo++;

        // 사운드 효과
        playSuccessSound();

        // 게임 종료 확인
        setTimeout(() => {
            checkGameOver();
        }, 350);
    } else {
        combo = 0;
    }

    selectedApples.clear();
    updateSelection();
    updateUI();
}

// UI 업데이트
function updateUI() {
    document.getElementById('score').textContent = score;
    document.getElementById('combo').textContent = combo;

    const remaining = apples.filter(a => !a.removed && a.element && !a.element.classList.contains('blank')).length;
    document.getElementById('remaining').textContent = remaining;
}

// 게임 오버 확인
function checkGameOver() {
    const remaining = apples.filter(a => !a.removed && a.element && !a.element.classList.contains('blank'));

    // 남은 사과들 중에서 합이 10이 되는 조합이 있는지 확인
    const canMakeTen = canMakeSum(remaining, TARGET_SUM);

    if (!canMakeTen || remaining.length === 0) {
        gameOver();
    }
}

// 합이 10이 되는 조합이 있는지 확인 (간단한 체크)
function canMakeSum(remainingApples, target) {
    if (remainingApples.length === 0) return false;

    // 간단한 체크: 1과 9, 2와 8 등의 조합이 있는지 확인
    const numbers = remainingApples.map(a => a.number).sort((a, b) => a - b);

    // 두 개의 사과로 10 만들기
    for (let i = 0; i < numbers.length; i++) {
        for (let j = i + 1; j < numbers.length; j++) {
            if (numbers[i] + numbers[j] === target) {
                return true;
            }
        }
    }

    // 세 개 이상의 사과로 10 만들기 (간단한 체크)
    // 1+2+7, 1+3+6, 1+4+5, 2+3+5, 3+3+4 등
    for (let i = 0; i < numbers.length; i++) {
        for (let j = i + 1; j < numbers.length; j++) {
            for (let k = j + 1; k < numbers.length; k++) {
                if (numbers[i] + numbers[j] + numbers[k] === target) {
                    return true;
                }
            }
        }
    }

    // 더 많은 조합도 가능하지만 성능을 위해 제한
    return false;
}

// 게임 오버
function gameOver() {
    document.getElementById('finalScore').textContent = score;
    document.getElementById('removedApples').textContent = removedApplesCount;
    document.getElementById('gameOver').style.display = 'block';
}

// 게임 재시작
function restartGame() {
    document.getElementById('gameOver').style.display = 'none';
    initGame();
}

// 성공 사운드
function playSuccessSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();

    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);

    oscillator.frequency.value = 600;
    oscillator.type = 'sine';

    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.2);

    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.2);
}

// 게임 시작
window.addEventListener('load', () => {
    initGame();
    setupEventListeners();
});

// 전역 함수로 노출
window.restartGame = restartGame;
