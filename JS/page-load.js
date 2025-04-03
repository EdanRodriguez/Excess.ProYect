// Wait for the page to load and add the loaded class to fade in
window.addEventListener("load", () => {
  document.body.classList.add("loaded");
});

// Handle page transitions on navbar links
document.querySelectorAll("nav a").forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault();

    // Add fade-out class to body immediately when the link is clicked
    document.body.classList.add("fade-out");

    // Navigate to the new page immediately after starting the fade-out
    window.location.href = e.target.href;
  });
});
