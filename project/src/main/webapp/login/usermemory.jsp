<%@ page language="java" contentType="text/html; charset=UTF-8"
    import="java.net.*,java.io.*,javax.servlet.http.*,
            java.util.Base64,
            java.nio.charset.StandardCharsets" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>회원 등록</title>
    <link rel = "stylesheet" href="./css/bootstrap.min.css">
   <link rel = "stylesheet" href="./css/custom.css">
    <script>
        function validateForm() {
            var password = document.forms["regForm"]["password"].value;
            var confirmPassword = document.forms["regForm"]["confirmPassword"].value;
            if (password !== confirmPassword) {
                alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>
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
               <a class = "nav-link" href = "aram.jsp">알림 저장</a>
            </li>
            <li class = "nav-item dropdown">
               <a class = "nav-link dropdown-toggle" id = "dropdown" data-toggle = "dropdown">
                  회원관리
               </a>
               <div class = "dropdown-menu" aria-labelledby = "dropdown">
                  <a class = "dropdown-item" href = "sessionCreate_success.jsp">로그인</a>  
                  <a class = "dropdown-item" href = "#">회원가입</a>
                   <a class = "dropdown-item" href = "usermemory.jsp">회원관리</a>   
                  <a class = "dropdown-item" href = "#">로그아웃</a>  
               </div>
            </li>
         </ul>
      </div>
   </nav>
   
   <!-- 제이커리 추가 -->
   <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js"></script>


    <%@ page contentType="text/html; charset=UTF-8" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>회원 등록</title>
    <script>
        function validateForm() {
            var password = document.forms["regForm"]["password"].value;
            var confirmPassword = document.forms["regForm"]["confirmPassword"].value;
            if (password !== confirmPassword) {
                alert("비밀번호와 비밀번호 확인이 일치하지 않습니다.");
                return false;
            }
            return true;
        }
    </script>
</head>
<body>

<%
Cookie[] cookies = request.getCookies();
String userId = null;
String userPw = null;

if (cookies != null) {
    for (Cookie cookie : cookies) {
        if ("userId".equals(cookie.getName())) {
            userId = cookie.getValue();
        } else if ("userPw".equals(cookie.getName())) {
            userPw = cookie.getValue();
        }
    }
}
%>

    <h2>회원 등록</h2>
<form name="regForm" action="RegisterServlet" method="post" onsubmit="return validateForm();">
    <label>아이디: 
        <input type="text" name="userId" value=<%= userId %> disabled>
    </label><br>

    <label>이름: 
        <input type="text" name="name" required>
    </label><br>

    <label>나이: 
        <input type="number" name="age" required>
    </label><br>

    <label>비밀번호: 
        <input type="password" name="password" 
               value=<%= userPw %> " 
               required>
    </label><br>

    <label>비밀번호 확인: 
        <input type="password" name="confirmPassword" required>
    </label><br>

    <label>전화번호: 
        <input type="text" name="phone" required>
    </label><br>

    <hr>
    <h3>보호자 정보</h3>
    <label>이름: 
        <input type="text" name="guardianName" required>
    </label><br>

    <label>전화번호: 
        <input type="text" name="guardianPhone" required>
    </label><br>

    <input type="submit" value="등록">
</form>
    
    
</body>
</html>

    
    
</body>
</html>
