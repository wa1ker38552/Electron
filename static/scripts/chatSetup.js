window.onload = function() {
  modal = document.getElementById("modal")
  error = document.getElementsByClassName("error")[0]
  errorText = document.getElementById("errorText")
  shareModal = document.getElementById("shareModal")
  shareLink = document.getElementById("shareLink")
  shareButton = document.getElementById("shareButton")
  leaveChatButton = document.getElementById("leaveChatButton")
  leaveModal = document.getElementById("leaveModal")
  input = document.getElementById("input")
  var username = getCookie("Authorization").split(".")[0]
  
  shareLink.innerHTML = window.location.origin+"/invite/"+id
  input.addEventListener("keyup", function(e) {
    if (e.key == "Enter") {
      e.preventDefault()
      sendMessage(id, input.value)
      input.value = ''
    }
  })

  fetchUserChats()
    .then(data => renderUserChats(data, id))

  fetchChatMeta(id)
    .then(data => {
      document.title = 'Electric | '+data.name
      document.getElementById("chatHeader").innerHTML = data.name
      document.getElementById("input").placeholder = "Message "+data.name
      if (username == data.owner) {
        var button = document.createElement("button")
        button.className = "button selection-button chat-option"
        button.innerHTML = "⚙️"
        document.getElementsByClassName("chat-options-container")[0].append(button)
        leaveChatButton.onclick = function() {openLeaveModal()}
      } else {
        leaveChatButton.onclick = function() {leaveChat(id)}
      }

      var avatar = document.createElement("div")
      var avatarIcon = document.createElement("img")
      var username = document.createElement("span")
      avatar.className = "panel-author-avatar"

      var members = [data.owner]
      members.push(...data.members)
      fetchUserAvatars(members)
        .then(avatars => avatars.json())
        .then(avatars => {
          if (avatars.data[data.owner]) {
            avatarIcon.src = avatars.data[data.owner]
          } else {
            avatarIcon.src = "/static/assets/default.png"
          }
          renderChatMembers(data.members, avatars.data)
        })
      
      username.innerHTML = data.owner
      avatar.append(avatarIcon)
      document.getElementById("chatOwner").append(avatar, username)
    })
  
  fetchChatHistory(id)
    .then(history => {
      renderChatHistory(history.data)
    })

  // stream handling
  setupSreamManager(2000, id)
}
