(function () {
  var btn = document.getElementById('mf-burger');
  var panel = document.getElementById('mf-mobile');
  if (btn && panel) {
    btn.addEventListener('click', function () {
      var open = panel.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      var openIcon = btn.querySelector('[data-icon=open]');
      var closeIcon = btn.querySelector('[data-icon=close]');
      if (openIcon && closeIcon) {
        openIcon.classList.toggle('hidden', open);
        closeIcon.classList.toggle('hidden', !open);
      }
    });
  }
  document.querySelectorAll('.mf-mobile-acc').forEach(function (acc) {
    acc.addEventListener('click', function () {
      var sub = acc.parentElement.querySelector('.mf-mobile-sub');
      if (!sub) return;
      var open = sub.classList.toggle('is-open');
      acc.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  });
})();
