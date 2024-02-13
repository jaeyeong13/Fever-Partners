function displayRemainingTime(targetDate, authId) {
    const now = new Date();
    const endDate = new Date(targetDate);

    if (isNaN(endDate.getTime())) {
        // targetDate가 올바른 날짜가 아닌 경우 처리
        const timerElement = document.querySelector(`.auth-timer[data-auth-id="${authId}"]`);
        if (timerElement) {
            timerElement.textContent = '유효하지 않은 날짜';
        }
        return;
    }

    const timeRemaining = endDate - now;

    if (timeRemaining <= 0) {
        const timerElement = document.querySelector(`.auth-timer[data-auth-id="${authId}"]`);
        if (timerElement) {
            timerElement.textContent = '시간 초과';
        }
        return;
    }

    const hours = Math.floor((timeRemaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((timeRemaining % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((timeRemaining % (1000 * 60)) / 1000);

    // 시간, 분, 초가 10 미만일 경우 앞에 0 추가
    const formattedTime = `${hours < 10 ? '0' : ''}${hours}시간 ${minutes < 10 ? '0' : ''}${minutes}분 ${seconds < 10 ? '0' : ''}${seconds}초`;

    const timerElement = document.querySelector(`.auth-timer[data-auth-id="${authId}"]`);
    if (timerElement) {
        timerElement.textContent = formattedTime;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const authElements = document.querySelectorAll('.activate-auth');

    authElements.forEach(authElement => {
        const authId = authElement.getAttribute('data-auth-id');
        const targetDate = authElement.getAttribute('data-target-date');
        
        // 초기 표시
        displayRemainingTime(targetDate, authId);

        // 1초마다 업데이트
        setInterval(() => {
            displayRemainingTime(targetDate, authId);
        }, 1000);
    });
});