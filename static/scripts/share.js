function showShareModal() {
  shareModal.style.display = ""
}

function closeShareModal() {
  shareModal.style.display = "none"
  shareButton.classList.remove("success")
}

function copyLink() {
  navigator.clipboard.writeText(shareLink.innerHTML);
  shareButton.classList.add("success")
}
