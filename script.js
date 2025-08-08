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
});