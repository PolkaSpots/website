document.addEventListener('DOMContentLoaded', function () {
  // Fade-in on scroll
  var els = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window) {
    var o = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('visible'); o.unobserve(e.target); }
      });
    }, { threshold: 0.1 });
    els.forEach(function (el) { o.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add('visible'); });
  }

  // Nav scroll state
  var nav = document.getElementById('nav');
  if (nav) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 40) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
    }, { passive: true });
  }

  // Hamburger toggle
  var toggle = document.querySelector('.nav-toggle');
  var links = document.querySelector('.nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open);
    });
  }
});
