
window.onload = function() {
  // var user = "{{ user.username }}";
  var count = user.length;
  var element = document.querySelector('nav a:nth-child(1)'); // เลือกอิลิเมนต์ที่ต้องการ
  var element_2 = document.querySelector('nav a:nth-child(2)');
  var element_3 = document.querySelector('nav a:nth-child(3)');
  var element_4 = document.querySelector('nav a:nth-child(4)');
  var indicator = document.querySelector('#indicator');
   
  var buttonContainer = document.getElementById('buttonContainer');
  var links = buttonContainer.getElementsByTagName('a');
  var numLinks = links.length;

  if (count <= 5){
    element.style.width = '9rem';
    // console.log(numLinks);

    if (numLinks == 2) {
      element_2.addEventListener('mouseenter', function() {
        indicator.style.left = '9.7rem';
      });
      element_2.addEventListener('mouseleave', function() {
        // คืนค่า left และ background ไปยังค่าเริ่มต้นที่คุณต้องการ
        indicator.style.left = '';
      });
      console.log("แสดง 1 ปุ่ม");
      console.log("count user " + count);
      console.log(user);
    }
    else if (numLinks == 3) {
      element_2.addEventListener('mouseenter', function() {
        indicator.style.left = '9.7rem';
      });
      element_2.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });

      element_3.addEventListener('mouseenter', function() {
        indicator.style.left = '14.7rem';
      });
      element_3.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });
      console.log("แสดง 2 ปุ่ม");
      console.log("count user " + count);
      console.log(user);
    }
    else {
      element_2.addEventListener('mouseenter', function() {
        indicator.style.left = '9.7rem';
      });
      element_2.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });

      element_3.addEventListener('mouseenter', function() {
        indicator.style.left = '14.7rem';
      });
      element_3.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });

      element_4.addEventListener('mouseenter', function() {
        indicator.style.left = '21.7rem';
      });
      element_4.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });
      console.log("แสดง 3 ปุ่ม");
      console.log("count user" + count);
      console.log(user);
    }
  }

  else if (5 < count && count <= 10){
     
    console.log("count user " + count);
    console.log(user);
  }

  else {
    element.style.width = '14rem';

    if (numLinks == 2) {
      element_2.addEventListener('mouseenter', function() {
        indicator.style.left = '14.7rem';
      });
      element_2.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });
      console.log("แสดง 1 ปุ่ม");
      console.log("count user " + count);
      console.log(user);
    }
    else if (numLinks == 3) {
      element_2.addEventListener('mouseenter', function() {
        indicator.style.left = '14.7rem';
      });
      element_2.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });

      element_3.addEventListener('mouseenter', function() {
        indicator.style.left = '19.7rem';
      });
      element_3.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });
      console.log("แสดง 2 ปุ่ม");
      console.log("count user " + count);
      console.log(user);
    }
    else {
      element_2.addEventListener('mouseenter', function() {
        indicator.style.left = '14.7rem';
      });
      element_2.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });

      element_3.addEventListener('mouseenter', function() {
        indicator.style.left = '19.7rem';
      });
      element_3.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });

      element_4.addEventListener('mouseenter', function() {
        indicator.style.left = '26.7rem';
      });
      element_4.addEventListener('mouseleave', function() {
        indicator.style.left = '';
      });
      console.log("แสดง 3 ปุ่ม");
      console.log("count user " + count);
      console.log(user);
    }
    
  }
  };