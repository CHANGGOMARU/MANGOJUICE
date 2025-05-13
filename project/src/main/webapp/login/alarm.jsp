<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
<link rel = "stylesheet" href="./css/bootstrap.min.css">
   <link rel = "stylesheet" href="./css/custom.css">
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


<div class = "modal-body">
               <h2 class="text-center">약 정보 입력</h2>

<form action="evaluationRegisterAction.jsp" method="post" class="p-3">

  <div class="form-group">
    <label>약 이름</label>
    <input type="text" name="lectureName" class="form-control" maxlength="20">
  </div>

  <div class="form-group">
    <label>약 설명</label>
    <input type="text" name="directorName" class="form-control" maxlength="20">
  </div>

  <div class="form-group">
    <label>감상 시간 선택</label>
    <div class="d-flex">
      <!-- 시 선택 -->
      <select name="hour" class="form-control me-2" style="width: 100px;">
        <% for (int i = 0; i < 24; i++) { %>
          <option value="<%= i %>"><%= i %>시</option>
        <% } %>
      </select>

      <!-- 분 선택 -->
      <select name="minute" class="form-control me-2" style="width: 100px;">
        <% for (int i = 0; i < 60; i++) { %>
          <option value="<%= i %>"><%= i %>분</option>
        <% } %>
      </select>
    </div>
  </div>

  <button type="submit" class="btn btn-primary mt-4">등록하기</button>

</form>
            </div>
      
   
   <!-- 제이커리 추가 -->
   <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js"></script>
   <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.min.js"></script>
   
</body>
</html>