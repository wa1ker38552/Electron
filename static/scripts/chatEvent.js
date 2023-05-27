async function leaveChat(id) {
  const a = await fetch(`/chats/${id}/leave`)
  const b = await a.json()
  if (b.success) {
    window.location.href = "/"
  }
}

function openLeaveModal() {
  leaveModal.style.display = ""
}

function closeLeaveModal() {
  leaveModal.style.display = "none"
}

function sendMessage(id, message) {
  fetch(`/chats/${id}/message`, {
    method : "POST",
    body: JSON.stringify({content: message})
  })
    .then(response => response.json())
    .then(response => {
      console.log(response)
    })
}

function setupSreamManager(millis, id) {
  setInterval(async function() {
    const p = document.getElementsByClassName("chat-content")[0]
    const a = await fetch("/stream/"+id)
    const b = await a.json()

    if (b.data.length > 0) {
      for (message of b.data) {
        p.append(createMessage(message))
      }
    }
  }, millis)
}
