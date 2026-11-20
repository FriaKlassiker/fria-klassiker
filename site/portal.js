/* Progressive enhancements: catalogue search and comfortable reading. */
(() => {
  'use strict';
  const catalog = document.querySelector('#bok-katalog');
  if (catalog) {
    const cards = [...catalog.querySelectorAll('.book-card')];
    const input = document.querySelector('#search-books');
    const buttons = [...document.querySelectorAll('.filter')];
    const counter = document.querySelector('#catalog-count');
    let current = 'alla';
    function update() {
      const q = (input?.value || '').trim().toLocaleLowerCase('sv-SE');
      let visible = 0;
      for (const card of cards) {
        const cats = (card.dataset.category || '').split(' ');
        const matchesGroup = current === 'alla' || cats.includes(current);
        const matchesText = (card.dataset.search || '').includes(q);
        card.hidden = !(matchesGroup && matchesText);
        if (!card.hidden) visible++;
      }
      if (counter) counter.textContent = `${visible} av ${cards.length} utgåvor`;
    }
    buttons.forEach(button => button.addEventListener('click', () => {
      current = button.dataset.filter || 'alla';
      buttons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
      update();
    }));
    input?.addEventListener('input', update);
    update();
  }
  const main = document.querySelector('.reader-main');
  if (main) {
    let scale = 1.09;
    document.querySelector('[data-reader-action="smaller"]')?.addEventListener('click', () => {
      scale = Math.max(.88, scale - .09); main.style.setProperty('--reader-font-size', `${scale.toFixed(2)}rem`);
    });
    document.querySelector('[data-reader-action="larger"]')?.addEventListener('click', () => {
      scale = Math.min(1.6, scale + .09); main.style.setProperty('--reader-font-size', `${scale.toFixed(2)}rem`);
    });
    const nightButton = document.querySelector('[data-reader-action="night"]');
    nightButton?.addEventListener('click', () => {
      const enabled = document.body.classList.toggle('reading-night');
      nightButton.setAttribute('aria-pressed', String(enabled));
      nightButton.textContent = enabled ? 'Ljust läsläge' : 'Mörkt läsläge';
    });
  }
})();
