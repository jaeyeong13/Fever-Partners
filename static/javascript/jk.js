//group_activity에서 ajax 처리
function loadContent(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(data => {
            document.getElementById('group-activity-content').innerHTML = data;
        })
        .catch(error => {
            console.error('Error during fetch operation:', error);
        });
  }

  function changeTab(tab, event, room_id) {
      event.preventDefault();

      // 모든 링크에서 selected 클래스 제거
      var links = document.querySelectorAll('#group-select-activity-list a');
      links.forEach(function(link) {
        link.classList.remove('selected-group-tab');
      });
    
      // 클릭한 링크에 selected 클래스 추가
      var selectedLink = event.currentTarget;
      selectedLink.classList.add('selected-group-tab');


      var url = '';
      switch (tab) {
        case 'member':
            url = '../member_list/'+room_id;
            break;
        case 'activate':
            url = '../activate/'+room_id;
            break;
        case 'show_log':
            url = '../show_log/'+room_id;
            break;
      }
      loadContent(url);
  }


//타이머 관련 코드.. 문제 많음
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