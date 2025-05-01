<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>세션 생성</title>
</head>
<body>
	Home > 세션 생성하기
	<hr>
	<%
		request.setCharacterEncoding("utf-8");	
	
		String u_id = request.getParameter("id");
		String u_pw = request.getParameter("passwd");
		
		if(u_id.equals("admin") && u_pw.equals("1234"))
		{
			response.sendRedirect("param.jsp");
		}
		else
		{
			response.sendRedirect("reponseLogin_failure.jsp");
		}
		
	%>

</body>
</html>