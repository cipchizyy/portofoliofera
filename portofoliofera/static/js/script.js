// ── Scroll reveal
const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.12 });
reveals.forEach(el => observer.observe(el));

// ── Animated skill bars on scroll
const bars = document.querySelectorAll('.bar-fill');
const barObserver = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.width = e.target.dataset.width + '%';
      barObserver.unobserve(e.target);
    }
  });
}, { threshold: 0.3 });
bars.forEach(b => barObserver.observe(b));

// ── Contact form — kirim ke Flask API
async function sendMessage() {
  const name    = document.getElementById('contact-name').value.trim();
  const email   = document.getElementById('contact-email').value.trim();
  const message = document.getElementById('contact-message').value.trim();
  const feedback = document.getElementById('contact-feedback');
  const btn = document.querySelector('.send-btn');

  if (!name || !email || !message) {
    feedback.style.color = '#ef4444';
    feedback.textContent = '⚠️ Nama, email, dan pesan wajib diisi.';
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Mengirim...';
  feedback.textContent = '';

  try {
    const res = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, message })
    });
    const data = await res.json();

    if (data.success) {
      feedback.style.color = '#16a34a';
      feedback.textContent = '✓ Pesan berhasil dikirim!';
      btn.textContent = 'Terkirim ✓';
      btn.style.background = '#16a34a';
      document.getElementById('contact-name').value = '';
      document.getElementById('contact-email').value = '';
      document.getElementById('contact-message').value = '';
      setTimeout(() => {
        btn.innerHTML = 'Send Message <span class="btn-dot" style="display:inline-block;width:18px;height:18px;background:var(--yellow);border-radius:50%;"></span>';
        btn.style.background = '';
        btn.disabled = false;
        feedback.textContent = '';
      }, 3000);
    } else {
      throw new Error(data.error || 'Gagal mengirim pesan.');
    }
  } catch (err) {
    feedback.style.color = '#ef4444';
    feedback.textContent = '✗ ' + err.message;
    btn.innerHTML = 'Send Message <span class="btn-dot" style="display:inline-block;width:18px;height:18px;background:var(--yellow);border-radius:50%;"></span>';
    btn.disabled = false;
  }
}