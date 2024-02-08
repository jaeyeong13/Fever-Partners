function loadSubtags(id) {
    const tag_container = document.getElementById('detail-tag-container');
    fetch('../get_subtags/'+id)
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

const certRequired = document.getElementById("cert_required");
if (certRequired) {
    certRequired.addEventListener("change", function () {
        var certFields = document.getElementById("cert_fields");
        certFields.style.display = this.checked ? "block" : "none";
    });
}

function validateGroupForm() {
    const goalSelect = document.getElementById('goal');
    const titleInput = document.getElementById('title');
    const detailTextarea = document.getElementById('detail');
    const certRequiredCheckbox = document.getElementById('cert_required');
    const penaltyInput = document.getElementById('penalty');
    const certDetail = document.getElementById('cert_detail');

    const goalWarning = document.getElementById('goal-warning');
    const titleWarning = document.getElementById('title-warning');
    const detailWarning = document.getElementById('detail-warning');
    const penaltyWarning = document.getElementById('penalty-warning');
    const certDetailWarning = document.getElementById('cert-detail-warning');

    goalWarning.innerHTML = '';
    titleWarning.innerHTML = '';
    detailWarning.innerHTML = '';
    penaltyWarning.innerHTML = '';
    certDetailWarning.innerHTML = '';

    if (goalSelect.value === '') {
        goalWarning.innerHTML = '목표를 선택하세요.';
    }

    if (titleInput.value.trim() === '') {
        titleWarning.innerHTML = '방의 제목을 입력하세요.';
    }

    if (detailTextarea.value.trim() === '') {
        detailWarning.innerHTML = '세부사항을 입력하세요.';
    }

    // 토글 버튼이 On인 경우에만 추가 validation 수행
    if (certRequiredCheckbox.checked) {

        if (certDetail.value.trim() === ''){
            certDetailWarning.innerHTML = '인증 세부사항을 간단히 적어주세요!(인증주기, 인증시간 등)';
        }

        if (penaltyInput.value === '') {
            penaltyWarning.innerHTML = '벌금을 입력하세요.';
        }
    }

    // 유효성 검사 통과 여부 반환 : false이면 폼 제출X
    return goalWarning.innerHTML === '' &&
        titleWarning.innerHTML === '' &&
        detailWarning.innerHTML === '' &&
        penaltyWarning.innerHTML === '' &&
        certDetailWarning.innerHTML === '';
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Goal 삭제시 팝업되는 confirm창
function GoalDeletionConfirm(goal_id) {
    Swal.fire({
      title: "정말 삭제하시겠습니까?",
      text: "삭제한 목표는 복구할 수 없어요!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "삭제",
      cancelButtonText: "취소",
    }).then((result) => {
        if (result.isConfirmed) {
            fetch("../delete_goal/" + goal_id, {
                method: "DELETE",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
                .then((response) => {
                    if (response.ok) {
                        const goalContainer = document.getElementById(`goal-${goal_id}`);
                        goalContainer.remove();
                        return response.json();
                    } else {
                        Swal.fire({
                            title: "삭제 실패",
                            text: "목표 삭제 중 오류가 발생했습니다",
                            icon: "error",
                        });
                        throw new Error("삭제 과정에서 오류가 발생했습니다.");
                    }
                })
                .then((json_data) => {
                    Swal.fire({
                        title: "삭제 완료",
                        text: json_data.message,
                        icon: "success",
                    });
                })
                .catch(error => { console.log(error.message)})
      } else if (result.dismiss === Swal.DismissReason.cancel) {
        Swal.fire({
          title: "취소됨",
          text: "목표 삭제가 취소되었습니다.",
          icon: "error",
          confirmButtonText: "확인",
        });
      }
    });
}