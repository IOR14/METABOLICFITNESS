(function () {
  var grid = document.getElementById('blog-posts-grid');
  if (!grid) return;

  fetch('data/blog-posts.json?v=' + Date.now())
    .then(function (response) {
      if (!response.ok) throw new Error('No se pudo cargar el indice del blog');
      return response.json();
    })
    .then(function (posts) {
      // Solo papers con articulo real (slug + imagen o pdf)
      posts = (posts || []).filter(function (post) {
        return post && post.slug && (post.image || post.pdf);
      });
      if (!posts.length) {
        grid.innerHTML =
          '<p class="col-span-full text-center font-body text-metabolic-charcoal/70">Aun no hay articulos publicados.</p>';
        return;
      }

      grid.innerHTML = posts.map(renderCard).join('');
    })
    .catch(function () {
      grid.innerHTML =
        '<p class="col-span-full text-center font-body text-metabolic-charcoal/70">No se pudieron cargar los articulos del blog.</p>';
    });

  function renderCard(post) {
    var color = post.category_color || 'metabolic-green';
    var href = 'blog/' + encodeURIComponent(post.slug) + '.html';
    var date = post.published_at ? formatDate(post.published_at) : '';
    var image = post.image ? escapeHtml(post.image) : '';
    var hero = image
      ? '<img src="' + image + '?v=2" alt="' + escapeHtml(post.title) + '" class="w-full h-full object-cover">'
      : '<div class="w-full h-full bg-gradient-to-br from-metabolic-green/20 to-metabolic-cyan/20 flex items-center justify-center">' +
          '<svg class="w-16 h-16 text-' + color + '" fill="none" stroke="currentColor" viewBox="0 0 24 24">' +
            '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>' +
          '</svg>' +
        '</div>';

    var pdfLink = post.pdf
      ? '<a href="' + escapeHtml(post.pdf) + '" download class="inline-flex items-center px-3 py-1.5 rounded-lg text-white text-xs font-heading font-semibold" style="background:#460877;">Descargar PDF</a>'
      : '';

    var rating = typeof post.rating === 'number' ? post.rating : null;
    var stars = '';
    if (rating != null) {
      var full = Math.floor(rating);
      var half = rating - full >= 0.5 ? 1 : 0;
      var empty = 5 - full - half;
      stars = '<div class="flex items-center gap-1 mb-2" title="Evaluacion ' + rating.toFixed(1) + '/5">';
      for (var i = 0; i < full; i++) stars += '<span style="color:#F5B301;">★</span>';
      if (half) stars += '<span style="color:#F5B301;opacity:0.55;">★</span>';
      for (var j = 0; j < empty; j++) stars += '<span style="color:#D1D5DB;">★</span>';
      stars += '<span class="text-xs font-body text-metabolic-charcoal/50 ml-1">' + rating.toFixed(1) + '</span></div>';
    }

    return (
      '<article class="bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all border border-gray-100">' +
        '<div class="h-52 overflow-hidden">' + hero + '</div>' +
        '<div class="p-6">' +
          '<div class="flex items-center justify-between gap-3 mb-2">' +
            '<span class="text-xs font-heading font-semibold text-' + color + ' uppercase">' + escapeHtml(post.category) + '</span>' +
            (date ? '<span class="text-xs font-body text-metabolic-charcoal/50">' + date + '</span>' : '') +
          '</div>' +
          stars +
          '<h3 class="font-heading font-bold text-xl text-metabolic-charcoal mt-2 mb-3 line-clamp-2">' + escapeHtml(post.title) + '</h3>' +
          '<p class="font-body text-metabolic-charcoal/70 text-sm mb-4 line-clamp-3">' + escapeHtml(post.excerpt) + '</p>' +
          '<div class="flex items-center justify-between gap-3">' +
            '<a href="' + href + '" class="text-metabolic-green font-body font-semibold text-sm hover:underline">Leer articulo →</a>' +
            pdfLink +
          '</div>' +
        '</div>' +
      '</article>'
    );
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
