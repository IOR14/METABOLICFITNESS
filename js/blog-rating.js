(function () {
  var box = document.getElementById('mf-paper-rating');
  if (!box) return;

  var slug = box.getAttribute('data-slug') || '';
  var editorial = parseFloat(box.getAttribute('data-editorial-rating') || '0') || 0;
  var storageKey = 'mf-paper-rating:' + slug;
  var stars = Array.prototype.slice.call(box.querySelectorAll('.mf-stars-input .mf-star'));
  var avgEl = document.getElementById('mf-avg-score');
  var countEl = document.getElementById('mf-vote-count');
  var clearBtn = document.getElementById('mf-rating-clear');
  var remote = { sum: 0, count: 0, editorial: editorial };

  function paint(value, hoverValue) {
    var active = hoverValue != null ? hoverValue : value;
    stars.forEach(function (star) {
      var v = parseInt(star.getAttribute('data-value'), 10);
      star.classList.toggle('mf-active', v <= active && active > 0);
      star.classList.toggle('mf-hover', hoverValue != null && v <= hoverValue);
    });
  }

  function readLocal() {
    var raw = localStorage.getItem(storageKey);
    if (raw == null || raw === '') return null;
    var n = parseInt(raw, 10);
    if (isNaN(n) || n < 0 || n > 5) return null;
    return n;
  }

  function writeLocal(value) {
    if (value == null || value === 0) localStorage.removeItem(storageKey);
    else localStorage.setItem(storageKey, String(value));
  }

  function updateSummary(userVote) {
    var sum = remote.sum || 0;
    var count = remote.count || 0;
    var local = userVote;
    // Si el usuario voto y aun no hay backend, refleja su voto en el promedio local.
    if (local != null && local > 0 && count === 0) {
      sum = local;
      count = 1;
    } else if (local != null && local > 0 && count > 0) {
      // no duplicar: mostramos remoto + nota de tu voto aparte
    }
    if (count > 0) {
      avgEl.textContent = (sum / count).toFixed(1);
      countEl.textContent = String(count);
    } else if (local != null && local > 0) {
      avgEl.textContent = local.toFixed(1);
      countEl.textContent = '1';
    } else {
      avgEl.textContent = '—';
      countEl.textContent = '0';
    }
  }

  function setVote(value) {
    writeLocal(value);
    paint(value || 0);
    updateSummary(value);
  }

  stars.forEach(function (star) {
    star.addEventListener('mouseenter', function () {
      paint(readLocal() || 0, parseInt(star.getAttribute('data-value'), 10));
    });
    star.addEventListener('mouseleave', function () {
      paint(readLocal() || 0);
    });
    star.addEventListener('click', function () {
      var value = parseInt(star.getAttribute('data-value'), 10);
      var current = readLocal();
      // segundo click en la misma estrella => 0
      if (current === value) setVote(0);
      else setVote(value);
    });
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      setVote(0);
    });
  }

  fetch('../data/blog-ratings.json?v=' + Date.now())
    .then(function (r) { return r.ok ? r.json() : {}; })
    .then(function (data) {
      if (data && data[slug]) remote = data[slug];
      var local = readLocal();
      paint(local || 0);
      updateSummary(local);
    })
    .catch(function () {
      var local = readLocal();
      paint(local || 0);
      updateSummary(local);
    });
})();
