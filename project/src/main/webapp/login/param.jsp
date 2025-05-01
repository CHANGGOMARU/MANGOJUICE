<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8" %>
<%@ page import = "java.util.Date" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>param 액션태그</title>
</head>
<body>
   <%
      Date nowTime = new Date();
   %>
   <jsp:forward page = "reponseLogin_success.jsp">
      <jsp:param name = "date"
      value = "<%= nowTime.toLocaleString() %>" />
   </jsp:forward>
   
</body>
</html>