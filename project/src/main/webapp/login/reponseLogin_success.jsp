<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>로그인 성공</title>
</head>
<body>
    <h2>웹사이트에 들어오신 것을 한영합니다!</h2>
    <hr>
   
   현재 날짜와 시각 :
   <%= request.getParameter("date")%>
   <br>
   
   
   <a href = "usermemory.jsp" target = "_blank">
      <img src = "button.png">
   </a><br>
   
</body>
</html>