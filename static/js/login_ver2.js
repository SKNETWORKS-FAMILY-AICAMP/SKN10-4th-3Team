document.addEventListener('DOMContentLoaded', function() {
    // 쿠키에서 JWT 토큰 가져오기
    function getCookie(name) {
        let value = `; ${document.cookie}`;
        let parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // JWT 토큰 확인
    const refreshToken = getCookie('refresh_token');

    // 로그인 상태 확인
    if (refreshToken) {
        const currentPath = window.location.pathname;
        // 로그인 상태일 경우 로그인 페이지와 회원가입 페이지 접근 제한
        if (currentPath.includes('/login')) {
          alert('로그인상태')
            // 다른 페이지로 리다이렉트 (예: 메인 페이지)
            window.location.href = '/chatbot/';
        }
    }
});
