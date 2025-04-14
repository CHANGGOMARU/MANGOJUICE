<%@ page import="com.mongodb.client.*" %>
<%@ page import="org.bson.Document" %>
<%@ page import="com.mongodb.MongoClientSettings" %>
<%@ page import="com.mongodb.client.model.Filters" %>
<%@ page import="java.util.*" %>
<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>로그인 성공</title>
</head>
<body>
    <h2>로그인 성공</h2>
    <hr>
<%
    String loginId = (String)session.getAttribute("loginId");

    if (loginId == null) {
        out.println("<p>세션이 만료되었습니다. 다시 로그인 해주세요.</p>");
    } else {
        try {
            // 1. MongoDB 연결
            MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017");
            MongoDatabase database = mongoClient.getDatabase("yourDatabase"); // DB 이름
            MongoCollection<Document> collection = database.getCollection("users");

            // 2. 로그인한 사용자의 정보 가져오기
            Document user = collection.find(Filters.eq("id", loginId)).first();

            if (user != null) {
                String name = user.getString("name");
                String imageUrl = user.getString("imageUrl"); // 예: "images/user1.jpg"

%>
                <p><strong>아이디:</strong> <%= loginId %></p>
                <p><strong>이름:</strong> <%= name %></p>
                <p><img src="<%= imageUrl %>" alt="사용자 사진" width="150" height="200"></p>
<%
            } else {
                out.println("<p>해당하는 사용자 정보를 찾을 수 없습니다.</p>");
            }

            mongoClient.close();

        } catch (Exception e) {
            out.println("<p>데이터베이스 오류: " + e.getMessage() + "</p>");
        }
    }
%>
</body>
</html>