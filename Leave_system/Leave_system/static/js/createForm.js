function checkInput() {
  var inputs = document.getElementsByTagName("input");
  var hasError = false;

  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].value === "") {
      inputs[i].classList.add("error-input");
      hasError = true;
    } else {
      inputs[i].classList.remove("error-input");
    }
  }

  if (hasError) {
    return false; // หยุดการส่งฟอร์มหากมีข้อผิดพลาด
  }

  var form = document.getElementById("register_form");
  form.submit(); // ส่งฟอร์มเมื่อไม่มีข้อผิดพลาด
}