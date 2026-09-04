(function () {
  var box = document.getElementById('mf-paper-rating');
  if (!box) return;

  var slug = box.getAttribute('data-slug') || '';
  var editorial = parseFloat(box.getAttribute('data-editorial-rating') || '0') || 0;
  var storageKey = 'mf-paper-rating:' + slug;
  var voterKey = 'mf-paper-voter-id';
  var apiBase = (window.MF_API_BASE || 'https://metabolicfitness.vercel.app').replace(/\/$/, '');
  var stars = Array.prototype.slice.call(box.querySelectorAll('.mf-stars-input .mf-star'));
  var avgEl = document.getElementById('mf-avg-score');
  var countEl = document.getElementById('mf-vote-count');
  var statusEl = document.getElementById('mf-rating-status');
  var clearBtn = document.getElementById('mf-rating-clear');
  var remote = { sum: 0, count: 0, editorial: editorial };
  var saving = false;

  if (clearBtn) clearBtn.style.display = 'none';

  function voterId() {
    var id = localStorage.getItem(voterKey);
    if (!id) {
      id = 'v_' + Math.random().toString(36).slice(2) + Date.now().toString(36);
      localStorage.setItem(voterKey, id);
    }
    return id;
  }

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
    if (isNaN(n) || n < 1 || n > 5) return null;
    return n;
  }

  function writeLocal(value) {
    // Nunca borrar: solo guardar 1..5
    if (value >= 1 && value <= 5) {
      localStorage.setItem(storageKey, String(value));
    }
  }

  function updateSummary() {
    var sum = remote.sum || 0;
    var count = remote.count || 0;
    if (count > 0) {
      avgEl.textContent = (sum / count).toFixed(1);
      countEl.textContent = String(count);
    } else {
      var local = readLocal();
      if (local) {
        avgEl.textContent = local.toFixed(1);
        countEl.textContent = '1';
      } else {
        avgEl.textContent = '—';
        countEl.textContent = '0';
      }
    }
  }

  function setStatus(msg) {
    if (!statusEl) return;
    var base =
      'Promedio lectores: <span id="mf-avg-score">' +
      (avgEl ? avgEl.textContent : '—') +
      '</span> · <span id="mf-vote-count">' +
      (countEl ? countEl.textContent : '0') +
      '</span> votos';
    statusEl.innerHTML = base + (msg ? ' <span class="text-metabolic-green">' + msg + '</span>' : '');
    avgEl = document.getElementById('mf-avg-score');
    countEl = document.getElementById('mf-vote-count');
  }

  function applyRemote(data) {
    if (!data) return;
    remote.sum = Number(data.sum || 0);
    remote.count = Number(data.count || 0);
    if (data.editorial != null) remote.editorial = Number(data.editorial) || editorial;
    updateSummary();
  }

  function loadRemote() {
    // 1) API viva
    return fetch(apiBase + '/api/blog-rating?slug=' + encodeURIComponent(slug), {
      method: 'GET',
      headers: { Accept: 'application/json' },
    })
      .then(function (r) {
        if (!r.ok) throw new Error('api');
        return r.json();
      })
      .then(applyRemote)
      .catch(function () {
        // 2) fallback JSON estatico del sitio
        return fetch('../data/blog-ratings.json?v=' + Date.now())
          .then(function (r) {
            return r.ok ? r.json() : {};
          })
          .then(function (data) {
            if (data && data[slug]) applyRemote(data[slug]);
            else updateSummary();
          })
          .catch(function () {
            updateSummary();
          });
      });
  }

  function saveVote(score) {
    if (saving) return;
    saving = true;
    writeLocal(score);
    paint(score);
    updateSummary();
    setStatus('· guardando…');

    fetch(apiBase + '/api/blog-rating', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        slug: slug,
        score: score,
        voter_id: voterId(),
        editorial: editorial,
      }),
    })
      .then(function (r) {
        return r.json().then(function (data) {
          if (!r.ok) throw new Error(data.error || 'fail');
          return data;
        });
      })
      .then(function (data) {
        applyRemote(data);
        setStatus('· voto guardado');
      })
      .catch(function () {
        // Queda guardado localmente aunque falle la red
        setStatus('· guardado en este dispositivo');
      })
      .finally(function () {
        saving = false;
      });
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
      // No se borra al volver a marcar: solo actualiza 1..5
      if (value >= 1 && value <= 5) saveVote(value);
    });
  });

  var local = readLocal();
  paint(local || 0);
  updateSummary();
  loadRemote().then(function () {
    paint(readLocal() || 0);
  });
})();
