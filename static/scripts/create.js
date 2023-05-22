function openCreateModal() {
  modal.style.display = ""
  error.style.display = "none"
}

function closeError() {
  error.style.display = "none"
}

function closeModal() {
  modal.style.display = "none"
}

function createChat() {
  fetch("/create", {
    method: "POST",
    body: JSON.stringify({
      name: document.getElementById("name").value
    })
  })
    .then(response => response.json())
    .then(response => {
      if (response.success) {
        window.location.href = "/chats/"+response.id
      } else {
        errorText.innerHTML = response.message
        error.style.display = ""
      }
    })
}
