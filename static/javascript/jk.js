//뒤로가기
function goBack() {
    window.history.back();
}

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

      // 모든 링크에서 selected-group-tab 클래스 제거
      var links = document.querySelectorAll('#group-select-activity-list a');
      links.forEach(function(link) {
        link.classList.remove('selected-group-tab');
      });
    
      // 클릭한 링크에 selected-group-tab 클래스 추가
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