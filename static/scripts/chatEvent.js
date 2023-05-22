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
