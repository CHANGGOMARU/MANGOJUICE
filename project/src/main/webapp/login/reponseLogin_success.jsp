<%@ page language="java" contentType="text/html; charset=UTF-8"
    import="java.net.*,java.io.*,javax.servlet.http.*,
            java.util.Base64,
            java.nio.charset.StandardCharsets" %>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>로그인 성공</title>
<link rel = "stylesheet" href="./css/bootstrap.min.css">
<link rel = "stylesheet" href="./css/custom.css">
</head>
<body>


    <h2>웹사이트에 들어오신 것을 환영합니다!</h2>
    <hr>


    현재 날짜와 시각 :
   <%= request.getParameter("date")%>
   <br>
   
   <nav class = "navbar navbar-expand-lg navbar-light bg-light">
		<a class = "navbar-brand" href = "reponseLogin_success.jsp">일상생활 정보</a>
		<button class="navbar-toggler" type ="button" data-toggle = "collapse" data-target = "#navbar">
			<span class = "navbar-toggler-icon"></span>
		</button>
		<div id = "navbar" class = "collapse navbar-collapse">
			<ul class = "navbar-nav mr-auto">
				<li class = "nav-item active">
					<a class = "nav-link" href = "reponseLogin_success.jsp">메인</a>
				</li>
				<li class = "nav-item active">
					<a class = "nav-link" href = "#">그래프</a>
				</li>
				<li class = "nav-item active">
					<a class = "nav-link" href = "#">방문자</a>
				</li>
				<li class = "nav-item active">
					<a class = "nav-link" href = "#">알림 저장</a>
				</li>
				<li class = "nav-item dropdown">
					<a class = "nav-link dropdown-toggle" id = "dropdown" data-toggle = "dropdown">
						회원관리
					</a>
					<div class = "dropdown-menu" aria-labelledby = "dropdown">
						<a class = "dropdown-item" href = "#">로그인</a>  
						<a class = "dropdown-item" href = "#">회원가입</a>  
						<a class = "dropdown-item" href = "#">로그아웃</a>
                        <a class = "dropdown-item" href = "usermemory.jsp">회원관리</a>  
					</div>
				</li>
			</ul>
		</div>
	</nav>
   
   <!-- 제이커리 추가 -->
	<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js"></script>



   
   현재 날짜와 시각 :
   <%= request.getParameter("date")%>
   <br>
   <br>
   <br>
   <br>
   <br>
   <br>

<h2>Flask 서버에서 받은 JWT:</h2>

<%
    String jwtToken = "토큰을 불러올 수 없습니다.";
    String userId = "사용자 ID를 추출할 수 없습니다.";

    try {
        // 1) Cookie에서 JWT 가져오기
        Cookie[] cookies = request.getCookies();
        if (cookies != null) {
            for (Cookie cookie : cookies) {
                if ("jwt_token".equals(cookie.getName())) {
                    jwtToken = cookie.getValue();
                    break;
                }
            }
        }

        // 2) JWT payload 디코딩해서 id와 passwd 추출
        if (!"토큰을 불러올 수 없습니다.".equals(jwtToken)) {
            String[] parts = jwtToken.split("\\.");
            if (parts.length >= 2) {
                String payload = parts[1];
                // Base64 URL-safe padding 보정
                int mod = payload.length() % 4;
                if (mod != 0) {
                    payload += "====".substring(mod);
                }
                byte[] decoded = Base64.getUrlDecoder().decode(payload);
                String payloadJson = new String(decoded, "UTF-8");    // e.g. {"id":"Sparta",...}

                int idStart = payloadJson.indexOf("\"id\":\"") + 6;
                int idEnd   = payloadJson.indexOf("\"", idStart);
                userId = payloadJson.substring(idStart, idEnd);
                
                // 비밀번호 추출 (필요하다면)
                int pwStart = payloadJson.indexOf("\"passwd\":\"") + 10;
                int pwEnd   = payloadJson.indexOf("\"", pwStart);
                String userPw = payloadJson.substring(pwStart, pwEnd);
                
                
                Cookie idCookie = new Cookie("userId", userId);
                Cookie pwCookie = new Cookie("userPw", userPw);

                // 쿠키 설정 (예: 유효기간 1일, 경로 설정)
                idCookie.setMaxAge(60 * 60 * 24); // 1일
                pwCookie.setMaxAge(60 * 60 * 24);

                idCookie.setPath("/"); // 전체 경로에서 쿠키 사용 가능
                pwCookie.setPath("/");

                // 응답에 쿠키 추가
                response.addCookie(idCookie);
                response.addCookie(pwCookie);
                
                // 세션에 사용자 정보 저장 (필요에 따라 사용)
                session.setAttribute("userId", userId);
            }
        }

    } catch (Exception e) {
        jwtToken = "오류 발생: " + e.getMessage();
        userId = "파싱 실패";
    }
%>

<!-- JWT 전체 출력 -->
<p><strong>JWT Token:</strong></p>
<textarea rows="5" cols="100"><%= jwtToken %></textarea>

<!-- 추출된 사용자 ID 출력 -->
<p><strong>JWT에서 추출된 사용자 ID:</strong> <%= userId %></p>

<!-- JWT 정보 더 자세히 보기 -->
<%
    if (!"토큰을 불러올 수 없습니다.".equals(jwtToken)) {
        try {
            String[] parts = jwtToken.split("\\.");
            if (parts.length >= 2) {
                String payload = parts[1];
                // Base64 URL-safe padding 보정
                int mod = payload.length() % 4;
                if (mod != 0) {
                    payload += "====".substring(mod);
                }
                byte[] decoded = Base64.getUrlDecoder().decode(payload);
                String payloadJson = new String(decoded, "UTF-8");
%>
<p><strong>JWT Payload (decoded):</strong></p>
<textarea rows="5" cols="100"><%= payloadJson %></textarea>
<%
            }
        } catch (Exception e) {
            // 디코딩 오류 처리
        }
    }
%>

</body>
</html>