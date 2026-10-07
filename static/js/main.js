document.addEventListener('DOMContentLoaded', () => {
  const navLinks = document.querySelectorAll('.navbar .nav-link');

  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      navLinks.forEach((item) => item.classList.remove('active'));
      link.classList.add('active');
    });
  });
});
