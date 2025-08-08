document.addEventListener("DOMContentLoaded", function() {
  const buttons = document.querySelectorAll(".accordion-button");
  buttons.forEach(button => {
    button.addEventListener("click", function() {
      const content = this.nextElementSibling;
      const isOpen = content.classList.contains("show");
      document.querySelectorAll(".accordion-content").forEach(c => c.classList.remove("show"));
      if (!isOpen) content.classList.add("show");
    });
  });
  const navLinks = document.querySelectorAll("nav a");
  navLinks.forEach(link => {
    link.addEventListener("click", function(e) {
      e.preventDefault();
      document.body.style.opacity = "0";
      setTimeout(() => { window.location.href = this.href; }, 300);
    });
  });
  document.body.style.transition = "opacity 0.3s ease";
  document.body.style.opacity = "1";
});