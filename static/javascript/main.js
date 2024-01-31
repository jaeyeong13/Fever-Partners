function loadSubtags(id) {
    const tag_container = document.getElementById('detail-tag-container');
    fetch('goal/get_subtags/'+id)
    .then(response => response.json())
    .then(json => {
        tag_container.innerHTML = json.result;
    });
}

function validateForm() {
    const activityCheckboxes = document.getElementsByName('activity-type[]');
    const tagRadios = document.getElementsByName('selected_tag');
    const goalTitle = document.getElementById('goal-title');
    const goalDetails = document.getElementById('goal-details');
    const offlineRadio = document.getElementById('offline-radio');
    const onlineRadio = document.getElementById('online-radio');
    
    const activityTypeWarning = document.getElementById('activity-type-warning');
    const goalTitleWarning = document.getElementById('goal-title-warning');
    const goalDetailsWarning = document.getElementById('goal-details-warning');
    const meetingPreferenceWarning = document.getElementById('meeting-preference-warning');
    const tagSelectionWarning = document.getElementById('tag-selection-warning');

    // 모든 경고 메시지 초기화
    tagSelectionWarning.innerHTML = '';
    activityTypeWarning.innerHTML = '';
    goalTitleWarning.innerHTML = '';
    goalDetailsWarning.innerHTML = '';
    meetingPreferenceWarning.innerHTML = '';

    const atLeastOneTagSelected = Array.from(tagRadios).some(function(radio) {
        return radio.checked;
    });

    if (!atLeastOneTagSelected) {
        tagSelectionWarning.innerHTML = '적어도 하나의 메인 태그를 선택해야 해요.';
    }

    // 스터디, 챌린지 중 하나는 반드시 선택
    const atLeastOneChecked = Array.from(activityCheckboxes).some((checkbox) => {
        return checkbox.checked;
    });

    if (!atLeastOneChecked) {
        activityTypeWarning.innerHTML = '적어도 하나는 선택해야 해요';
    }

    // 공백 허용 X
    if (goalTitle.value.trim() === '') {
        goalTitleWarning.innerHTML = '제목을 입력해주세요';
    }

    // 공백 허용 X
    if (goalDetails.value.trim() === '') {
        goalDetailsWarning.innerHTML = '세부사항을 입력해주세요';
    }

    // 대면/비대면 활동 중 하나는 선택되어야 함
    if (!offlineRadio.checked && !onlineRadio.checked) {
        meetingPreferenceWarning.innerHTML = '하나를 선택해주세요';
    }

    // 유효성 검사 통과 여부 반환 : false이면 폼 제출X
    return tagSelectionWarning.innerHTML === '' &&
        activityTypeWarning.innerHTML === '' &&
        goalTitleWarning.innerHTML === '' &&
        goalDetailsWarning.innerHTML === '' &&
        meetingPreferenceWarning.innerHTML === '';
}