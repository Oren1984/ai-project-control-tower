// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const target = document.querySelector(link.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 64;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// Active nav highlighting on scroll
const sections = document.querySelectorAll('[data-section]');
const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');

const sectionObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('data-section');
      navLinks.forEach(link => {
        link.classList.toggle('active', link.getAttribute('href') === '#' + id);
      });
    }
  });
}, { rootMargin: '-20% 0px -65% 0px' });

sections.forEach(s => sectionObserver.observe(s));

// Animate score bars when they scroll into view
function initScoreBars() {
  const bars = document.querySelectorAll('.score-fill');
  bars.forEach(bar => {
    const targetWidth = bar.getAttribute('data-pct');
    bar.style.width = '0%';
    bar._targetWidth = targetWidth;
  });

  const scoreSection = document.querySelector('.score-bars');
  if (!scoreSection) return;

  const barObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.querySelectorAll('.score-fill').forEach(bar => {
          bar.style.width = bar._targetWidth + '%';
        });
        barObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.2 });

  document.querySelectorAll('.score-bars').forEach(el => barObserver.observe(el));
}

initScoreBars();
