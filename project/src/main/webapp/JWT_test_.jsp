<%@ page import="java.net.*, java.io.*, java.util.Base64" %>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>JWT Token Viewer</title>
</head>
<body>

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
                
                int nameStart = payloadJson.indexOf("\"name\":\"") + 10;
                int nameEnd   = payloadJson.indexOf("\"", nameStart);
                String username = payloadJson.substring(nameStart, nameEnd);

                int emialStart = payloadJson.indexOf("\"email\":\"") + 10;
                int emailEnd   = payloadJson.indexOf("\"", emailStart);
                String userPw = payloadJson.substring(emailStart, emailEnd);

                int pnStart = payloadJson.indexOf("\"phone_number\":\"") + 10;
                int pnEnd   = payloadJson.indexOf("\"", pnStart);
                String userPn = payloadJson.substring(pnStart, pnEnd);

                int ageStart = payloadJson.indexOf("\"age\":\"") + 10;
                int ageEnd   = payloadJson.indexOf("\"", emailStart);
                String userage = payloadJson.substring(ageStart, ageEnd);
                
                // 세션에 사용자 정보 저장 (필요에 따라 사용)
                session.setAttribute("userId", userId);
                session.setAttribute("userPw", userPw);
                session.setAttribute("username", username);
                session.setAttribute("userpn", userpn);
                session.setAttribute("userage", userage);

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
            out.println("<p style='color:red;'>오류: " + e.getMessage() + "</p>");
        }
    }
%>
<form name = 'submitform' action = 'http://127.0.0.1:5000/Generate' method = "post">
	<input type = "submit" value = "로그인"><br>	<br>
	
	</form>

</body>
</html>