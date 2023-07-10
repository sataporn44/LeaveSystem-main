form.addEventListener('submit',function(e){
  e.preventDefault();
  if (username.value==='') {
    showerror(username,"Please insert Username");
  }
  else{
    showsuccess();
  }
})

function showerror(input,messege){
  const formBold = input.parentElement ;  //ส่งไปตัวเเม่
  formold.className='formbold error'
}

function showsuccess(){
}

function detecNull(user,first,last,nick,phone,email,team,position,leader,level,password){
  if(user == ""){
    window.alert("Please insert Username");
    return false ;
  } else if (first == "") {
    window.alert("Please insert Firstname");
    return false ;
  } else if (last == "") {
    window.alert("Please insert Lastname");
    return false ;
  } else if (nick == "") {
    window.alert("Please insert Nickname");
    return false ;
  } else if (phone == "") {
    window.alert("Please insert Phone number");
    return false ;
  } else if (email == "") {
    window.alert("Please insert Email");
    return false ;
  } else if (team == "") {
    window.alert("Please insert Team");
    return false ;
  } else if (position == "") {
    window.alert("Please insert Position");
    return false ;
  } else if (leader == "") {
    window.alert("Please insert Leader");
    return false ;
  } else if (level == "") {
    window.alert("Please insert Level");
    return false ;
  } else if (password == "") {
    window.alert("Please insert Password");
    return false ;
  }
}

function checkInput(){
  var username = document.getElementById("username").value
  var firstname = document.getElementById("first_name").value
  var lastname = document.getElementById("last_name").value
  var nickname = document.getElementById("nickname").value
  var phone = document.getElementById("phone").value
  var email = document.getElementById("email").value
  var team = document.getElementById("team").value            
  var position = document.getElementById("position").value
  var leader = document.getElementById("leader").value
  var level = document.getElementById("level").value            
  var password = document.getElementById("password").value

  detecNull(username,firstname,lastname,nickname,phone,email,team,position,leader,level,password)
}