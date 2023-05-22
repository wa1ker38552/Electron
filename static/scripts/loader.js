function getCookie(name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

async function fetchUserChats() {
  const username = getCookie("Authorization").split(".")[0]
  const a = await fetch(`/${username}/chats`)
  const b = await a.json()
  return b
}

function renderUserChats(data, id=null) {
  var p = document.getElementsByClassName("tabs-container")[0]
  for (chat of data) {
    var parent = document.createElement("div")
    var name = document.createElement("div")
    var sub = document.createElement("name")
    
    if (id == chat.id) {
      parent.style.background = "var(--accent-light)"
    }
    
    parent.className = "chat-container"
    name.className = "chat-name"
    sub.className = "chat-sub"
    
    if (chat.name.length > 11) {
      name.innerHTML = chat.name.slice(0, 11)+"..."
    } else {name.innerHTML = chat.name}
    
    if (chat.members.length == 0) {
      sub.innerHTML = "1 Member"
    } else {''
      sub.innerHTML = chat.members.length+1+" Members"
    }
    parent.id = chat.id
    parent.onclick = function() {window.location.href = "/chats/"+this.id}
    parent.append(name, sub)
    p.append(parent)
  }
}

async function fetchChatMeta(id) {
  const a = await fetch(`/chats/${id}/details`)
  const b = await a.json()
  return b
}

function renderChatMembers(members, avatars) {
  var p = document.getElementById("contentPanelMembers")
  var i = 0
  for (member of members) {
    var e = document.createElement("div")
    var avatar = document.createElement("div")
    var avatarIcon = document.createElement("img")
    var username = document.createElement("span")
    e.className = "content-panel-user centered-vertically"
    avatar.className = "panel-author-avatar"
    if (avatars[i]) {
      avatarIcon.src = avatars[i]
    } else {
      avatarIcon.src = "/static/assets/default.png"
    }
    username.innerHTML = member
    avatar.append(avatarIcon)
    e.append(avatar, username)
    p.append(e)
  }
}

function fetchUserAvatars(members) {
  response = fetch("/avatars/batch", {
    method: "POST",
    body: JSON.stringify({
      "members": members
    })
  })
  return response
}
