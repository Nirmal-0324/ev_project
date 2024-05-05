function validateForm() {
    var email = document.forms[0]["email"].value;
    var password = document.forms[0]["psw"].value;
    if (email == "") {
      alert("Email must be filled out");
      return
    }}