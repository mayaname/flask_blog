// Display modal profile window

document.addEventListener("DOMContentLoaded", function () {
let modal = document.getElementById("profileModal");
let profileContent = document.getElementById("profileContent");
let closeBtn = document.querySelector(".close");

document.querySelectorAll(".profile-link").forEach(link => {
    link.addEventListener("click", function (event) {
    event.preventDefault();
    let username = this.getAttribute("data-username");

    fetch(`/profile_popup/${username}`)
        .then(response => response.text())
        .then(data => {
        profileContent.innerHTML = data;
        modal.style.display = "block";
        });
    });
});

// Close modal when clicking the close button
closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
});

// Close modal when clicking outside the modal content
window.addEventListener("click", function (event) {
    if (event.target === modal) {
    modal.style.display = "none";
    }
});
});

