(function () {
  var grid = document.getElementById('blog-posts-grid');
  var featured = document.getElementById('blog-featured');
  if (!grid) return;

  fetch('data/blog-posts.json?v=' + Date.now())
    .then(function (response) {
      if (!response.ok) throw new Error('No se pudo cargar el indice del blog');
      return response.json();
    })
    .then(function (posts) {
      posts = (posts || []).filter(function (post) {
        return post && post.slug && (post.image || post.pdf);
      });
      if (!posts.length) {
        grid.innerHTML =
          '<p class="col-span-full text-center font-body text-metabolic-charcoal/70">Aun no hay articulos publicados.</p>';
        return;
      }

      posts.sort(function (a, b) {
        return String(b.published_at || '').localeCompare(String(a.published_at || ''));
      });

      var latest = posts[0];
      var rest = posts.slice(1);

      if (featured) {
        featured.innerHTML = renderFeatured(latest);
      }
      grid.innerHTML = rest.map(renderCard).join('');
    })
    .catch(function () {
      grid.innerHTML =
        '<p class="col-span-full text-center font-body text-metabolic-charcoal/70">No se pudieron cargar los articulos del blog.</p>';
    });

  function renderFeatured(post) {
    var href = 'blog/' + encodeURIComponent(post.slug) + '.html';
    var image = post.image ? escapeHtml(post.image) + '?v=11' : '';
    var date = post.published_at ? formatDate(post.published_at) : '';
    var stars = renderStars(post.rating);
    var pdf = post.pdf
      ? '<a class="pdf" href="' + escapeHtml(post.pdf) + '" download>Descargar PDF</a>'
      : '';
    return (
      '<article class="mf-paper-featured">' +
        (image
          ? '<a href="' + href + '"><img src="' + image + '" alt="' + escapeHtml(post.title) + '"></a>'
          : '<div></div>') +
        '<div class="mf-paper-featured-body">' +
          '<div class="mf-paper-meta"><span class="mf-paper-cat">' +
            escapeHtml(post.category || 'Clinica') +
          '</span>' +
          (date ? '<span>' + date + '</span>' : '') +
          '<span>Mas reciente</span></div>' +
          stars +
          '<h2 class="mf-paper-title" style="font-size:1.45rem;margin-top:0.35rem;">' +
            escapeHtml(post.title) +
          '</h2>' +
          '<p class="mf-paper-excerpt">' + escapeHtml(post.excerpt || '') + '</p>' +
          '<div class="mf-paper-actions">' +
            '<a class="read" href="' + href + '">Leer articulo →</a>' +
            pdf +
          '</div>' +
        '</div>' +
      '</article>'
    );
  }

  function renderCard(post) {
    var href = 'blog/' + encodeURIComponent(post.slug) + '.html';
    var date = post.published_at ? formatDate(post.published_at) : '';
    var image = post.image ? escapeHtml(post.image) + '?v=11' : '';
    var stars = renderStars(post.rating);
    var pdf = post.pdf
      ? '<a class="pdf" href="' + escapeHtml(post.pdf) + '" download>Descargar PDF</a>'
      : '';
    var hero = image
      ? '<a href="' + href + '"><img src="' + image + '" alt="' + escapeHtml(post.title) + '"></a>'
      : '<div style="height:11.5rem;background:#f7f5f9;"></div>';

    return (
      '<article class="mf-paper-card">' +
        hero +
        '<div class="mf-paper-card-body">' +
          '<div class="mf-paper-meta"><span class="mf-paper-cat">' +
            escapeHtml(post.category || 'Clinica') +
          '</span>' +
          (date ? '<span>' + date + '</span>' : '') +
          '</div>' +
          stars +
          '<h3 class="mf-paper-title">' + escapeHtml(post.title) + '</h3>' +
          '<p class="mf-paper-excerpt">' + truncate(escapeHtml(post.excerpt || ''), 160) + '</p>' +
          '<div class="mf-paper-actions">' +
            '<a class="read" href="' + href + '">Leer articulo →</a>' +
            pdf +
          '</div>' +
        '</div>' +
      '</article>'
    );
  }

  function renderStars(rating) {
    if (typeof rating !== 'number') return '';
    var full = Math.floor(rating);
    var half = rating - full >= 0.5 ? 1 : 0;
    var empty = 5 - full - half;
    var html = '<div class="mf-paper-meta" style="margin-bottom:0.35rem;" title="Evaluacion ' + rating.toFixed(1) + '/5">';
    var i;
    for (i = 0; i < full; i++) html += '<span style="color:#F5B301;">★</span>';
    if (half) html += '<span style="color:#F5B301;opacity:0.55;">★</span>';
    for (i = 0; i < empty; i++) html += '<span style="color:#D1D5DB;">★</span>';
    html += '<span style="margin-left:0.25rem;">' + rating.toFixed(1) + '</span></div>';
    return html;
  }

  function truncate(text, max) {
    if (!text || text.length <= max) return text;
    return text.slice(0, max - 1).replace(/\s+\S*$/, '') + '…';
  }

  function formatDate(isoDate) {
    var parts = isoDate.split('-');
    if (parts.length !== 3) return isoDate;
    return parts[2] + '/' + parts[1] + '/' + parts[0];
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }
})();
