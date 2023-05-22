function openModal(type) {
  modal.style.display = ""
  error.style.display = "none"
  username.value = ""
  password.value = ""
  password.type = "password"
  passwordToggle.innerHTML = "Show password"
  if (type == 0) {
    modalTitle.innerHTML = "Login"
    actionToggle.innerHTML = "Login"
    actionToggle.onclick = function() {actionEvent("login")}
  } else {
    modalTitle.innerHTML = "Signup"
    actionToggle.innerHTML = "Signup"
    actionToggle.onclick = function() {actionEvent("signup")}
  }
}

function togglePassword() {
  if (passwordToggle.innerHTML == "Show password") {
    password.type = "text"
    passwordToggle.innerHTML = "Hide password"
  } else {
    password.type = "password"
    passwordToggle.innerHTML = "Show password"
  }
}

function closeError() {
  error.style.display = "none"
}

function actionEvent(type) {
  fetch(`/${type}`, {
    method: "POST",
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  })
    .then(data => data.json())
    .then(data => {
      if (data.success) {
        window.location.href = `/callback?token=`+data.token
      } else {
        if (type == "login") {
          errorText.innerHTML = "Username or password is incorrect"
          error.style.display = ""
        } else {
          errorText.innerHTML = data.message
          error.style.display = ""
        }
      }
    })
}

function closeModal() {
  modal.style.display = "none"
}



var modalTitle
var modal
var username
var password
var actionToggle
var error
var errorText
var passwordToggle

window.onload = function() {
  passwordToggle = document.getElementById("passwordToggle")
  errorText = document.getElementById("errorText")
  error = document.getElementsByClassName("error")[0]
  actionToggle = document.getElementById("actionToggle")
  username = document.getElementById("username")
  password = document.getElementById("password")
  modal = document.getElementById("modal")
  modalTitle = document.getElementById("modalTitle")
}
