<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page import = "java.util.Date" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>로그인 폼 생성</title>
</head>
<body>
	Home > 로그인 폼 화면
	<hr>
	<img src = "per.jpg" width = "100" height = "150">
	<br>
	
	<form name = 'loginForm' action = 'http://127.0.0.1:5000/login' method = "post">
	아이디: <br>
	<input type = "text" name = "id"> <br><br>
	비밀번호: <br> 
	<input type = "password" name = "passwd"> <br><br>
	<input type = "submit" value = "로그인"><br>	<br>
	
	</form>
	
	<form name = 'signup' action = 'reponse_singup.jsp' method = "post">
	<input type = "submit" value = "회원가입">	
	</form>
	<script>
    // 페이지 로드되면 바로 POST
    document.getElementById('loginForm').submit();
  </script>
</body>
</html>