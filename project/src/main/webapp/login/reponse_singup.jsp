<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>회원가입</title>
  <script>
    function validateForm() {
      const pw = document.getElementById("password").value;
      const pwCheck = document.getElementById("passwordCheck").value;

      if (pw !== pwCheck) {
        alert("비밀번호가 일치하지 않습니다.");
        return false; // 폼 제출 방지
      }

      // 모든 필수 입력 항목이 비어 있지 않은지 확인
      const requiredFields = ["userId", "name", "password", "passwordCheck", "phone", "guardianName", "guardianPhone"];
      for (let field of requiredFields) {
        if (document.getElementById(field).value.trim() === "") {
          alert("모든 항목을 입력해주세요.");
          return false;
        }
      }

      alert("회원가입이 완료되었습니다.");
      return true; // 폼 제출 허용
    }
  </script>
</head>
<body>
  <h2>회원가입</h2>
  <form method="post" action="sessionCreate.jsp" onsubmit="return validateForm();">
    <label>아이디: <input type="text" id="userId" name="userId"></label><br><br>
    <label>이름: <input type="text" id="name" name="name"></label><br><br>
    <label>비밀번호: <input type="password" id="password" name="password"></label><br><br>
    <label>비밀번호 확인: <input type="password" id="passwordCheck" name="passwordCheck"></label><br><br>
    <label>전화번호: <input type="text" id="phone" name="phone"></label><br><br>
    <label>보호자 이름: <input type="text" id="guardianName" name="guardianName"></label><br><br>
    <label>보호자 전화번호: <input type="text" id="guardianPhone" name="guardianPhone"></label><br><br>

    <input type="submit" value="회원가입">

  </form>
</body>
</html>