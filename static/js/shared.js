/* ============================================================
   IVORY IMMO — Shared JS: Navbar, Modal, Chatbot, Favorites
   ============================================================ */

// ============================================================
// NAVBAR SCROLL + HAMBURGER
// ============================================================
(function () {
  const nav = document.getElementById('navbar');
  if (!nav) return;

  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 60);
  });

  const burger = document.getElementById('burger');
  const links  = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', () => {
      links.classList.toggle('open');
      // Animate hamburger to X
      const spans = burger.querySelectorAll('span');
      if (links.classList.contains('open')) {
        spans[0].style.transform = 'translateY(7px) rotate(45deg)';
        spans[1].style.opacity   = '0';
        spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
      } else {
        spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
      }
    });
    // Close on link click
    links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      links.classList.remove('open');
      burger.querySelectorAll('span').forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    }));
  }

  // Mark active nav link based on current page
  const page = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(a => {
    const href = a.getAttribute('href') || '';
    if (href.includes(page)) a.classList.add('active');
  });
})();

// ============================================================
// MODAL (shared)
// ============================================================
function openModal(prop) {
  const bd = document.getElementById('modal-backdrop');
  if (!bd) return;

  document.getElementById('m-img').src     = prop.image;
  document.getElementById('m-img').alt     = prop.title;
  document.getElementById('m-title').textContent  = prop.title;
  document.getElementById('m-loc').textContent    = '📍 ' + prop.location;
  document.getElementById('m-desc').textContent   = prop.description;
  document.getElementById('m-type-tag').textContent = prop.type;
  document.getElementById('m-mode-tag').textContent = prop.modes.join(' & ');

  // Badge
  const badge = document.getElementById('m-badge');
  if (prop.modes.includes('location') && prop.modes.includes('vente')) {
    badge.textContent = 'Location & Vente'; badge.className = 'badge badge-both';
  } else if (prop.modes.includes('vente')) {
    badge.textContent = 'À vendre'; badge.className = 'badge badge-sell';
  } else {
    badge.textContent = 'À louer'; badge.className = 'badge badge-loc';
  }

  // Features
  const feats = document.getElementById('m-feats');
  feats.innerHTML = Object.entries(prop.features).map(([k, v]) => `
    <div class="modal-feat">
      <span class="modal-feat-label">${k}</span>
      <span class="modal-feat-val">${v}</span>
    </div>`).join('');

  // Prices
  const prices = document.getElementById('m-prices');
  prices.innerHTML = (prop.prix_location ? `
    <div class="modal-price-box">
      <div class="modal-price-lbl">Location / mois</div>
      <div class="modal-price-amt">${prop.prix_location}</div>
    </div>` : '') +
    (prop.prix_vente ? `
    <div class="modal-price-box">
      <div class="modal-price-lbl">Prix de vente</div>
      <div class="modal-price-amt">${prop.prix_vente}</div>
    </div>` : '');

  bd.classList.add('show');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  const bd = document.getElementById('modal-backdrop');
  if (bd) { bd.classList.remove('show'); document.body.style.overflow = ''; }
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// ============================================================
// FAVORITES (localStorage)
// ============================================================
const FAV_KEY = 'ivoryimmo_favorites';

function getFavorites() {
  try { return JSON.parse(localStorage.getItem(FAV_KEY) || '[]'); }
  catch { return []; }
}
function saveFavorites(arr) {
  localStorage.setItem(FAV_KEY, JSON.stringify(arr));
}
function toggleFavorite(id) {
  let favs = getFavorites();
  const idx = favs.indexOf(id);
  if (idx >= 0) { favs.splice(idx, 1); }
  else          { favs.push(id); }
  saveFavorites(favs);
  refreshFavButtons();
  return idx < 0; // true = added
}
function isFavorite(id) { return getFavorites().includes(id); }
function refreshFavButtons() {
  document.querySelectorAll('[data-fav-id]').forEach(btn => {
    const id = parseInt(btn.dataset.favId);
    btn.classList.toggle('active', isFavorite(id));
    btn.title = isFavorite(id) ? 'Retirer des favoris' : 'Ajouter aux favoris';
  });
}

// ============================================================
// CHATBOT
// ============================================================
const CHAT_RESPONSES = [
  // Salutations
  {
    patterns: ['bonjour', 'bonsoir', 'salut', 'hello', 'hi', 'bonne journée'],
    response: "Bonjour et bienvenue chez IvoryImmo ! 👋 Je suis votre assistant immobilier. Puis-je vous aider à trouver une propriété, obtenir des informations sur nos services, ou autre chose ?"
  },
  // Propriétés disponibles
  {
    patterns: ['propriété', 'bien', 'maison', 'disponible', 'catalogue', 'liste'],
    response: "Nous proposons actuellement plusieurs types de biens : des <strong>appartements</strong>, des <strong>studios</strong> et des <strong>villas</strong>. Consultez notre page <a href='services.html' style='color:var(--gold)'>Nos Biens</a> pour voir tout notre catalogue avec filtres. Vous cherchez quelque chose en particulier ?"
  },
  // Villa
  {
    patterns: ['villa'],
    response: "Nos villas sont des propriétés d'exception allant de 280 à 500 m², disponibles à Riviera, Angré et Bingerville. Les prix varient entre 180 et 500 millions FCFA à la vente, et à partir de 1 500 000 FCFA/mois en location. Souhaitez-vous planifier une visite ?"
  },
  // Appartement
  {
    patterns: ['appartement', 'appart'],
    response: "Nos appartements vont de 65 à 120 m² et sont situés dans des quartiers prisés comme Cocody, Marcory et Grand-Bassam. Prix de location dès 200 000 FCFA/mois et à la vente à partir de 28 millions FCFA. Je peux vous en dire plus sur l'un d'eux !"
  },
  // Studio
  {
    patterns: ['studio'],
    response: "Nos studios sont idéaux pour les étudiants ou jeunes professionnels. Surface de 28 à 35 m², à partir de 80 000 FCFA/mois en location. Certains sont aussi disponibles à l'achat. Vous avez un budget en tête ?"
  },
  // Location
  {
    patterns: ['louer', 'location', 'loue', 'mensuel'],
    response: "Nos biens en location sont disponibles dès <strong>80 000 FCFA/mois</strong> pour un studio, et jusqu'à <strong>1 500 000 FCFA/mois</strong> pour une villa de prestige. Quel est votre budget mensuel pour vous proposer les meilleures options ?"
  },
  // Achat/Vente
  {
    patterns: ['acheter', 'achat', 'vente', 'vendre', 'prix'],
    response: "Les prix de vente varient selon le type de bien :<br>• <strong>Studios :</strong> à partir de 15 M FCFA<br>• <strong>Appartements :</strong> à partir de 28 M FCFA<br>• <strong>Villas :</strong> à partir de 180 M FCFA<br><br>Quel type de bien vous intéresse ?"
  },
  // Contact
  {
    patterns: ['contact', 'contacter', 'appeler', 'téléphone', 'email', 'rendez-vous', 'visite'],
    response: "Vous pouvez nous contacter facilement :<br>📞 <strong>+225 00 00 00 00</strong><br>✉️ <strong>contact@ivoryimmo.ci</strong><br>📍 Abidjan, Côte d'Ivoire<br><br>Ou visitez notre <a href='contact.html' style='color:var(--gold)'>page Contact</a> pour envoyer un message directement !"
  },
  // Équipe
  {
    patterns: ['équipe', 'agent', 'conseiller', 'personnel', 'staff'],
    response: "Notre équipe est composée d'agents immobiliers expérimentés et passionnés. Découvrez nos conseillers sur la page <a href='equipe.html' style='color:var(--gold)'>Notre Équipe</a>. Chaque agent est spécialisé dans un type de bien ou un quartier spécifique."
  },
  // Quartier / Zone
  {
    patterns: ['cocody', 'plateau', 'riviera', 'marcory', 'angré', 'bingerville', 'bassam', 'quartier'],
    response: "Nous avons des biens dans plusieurs quartiers d'Abidjan et ses environs : Cocody, Le Plateau, Riviera, Deux-Plateaux, Marcory, Angré, et même à Grand-Bassam. Vous avez une préférence géographique ? Je peux cibler ma recherche !"
  },
  // Visite
  {
    patterns: ['visit', 'voir', 'découvrir', 'planifier'],
    response: "Pour organiser une visite, contactez-nous sur la page <a href='contact.html' style='color:var(--gold)'>Contact</a> ou appelez-nous au <strong>+225 00 00 00 00</strong>. Nos agents sont disponibles du lundi au samedi, de 8h à 18h pour vous accompagner !"
  },
  // Délais / disponibilité
  {
    patterns: ['disponib', 'libre', 'quand', 'délai'],
    response: "La disponibilité varie selon les biens. Pour avoir une information précise sur un bien spécifique, contactez-nous directement ou consultez notre page services. Nos agents vous répondront sous 24h !"
  },
  // Financement / crédit
  {
    patterns: ['crédit', 'prêt', 'financement', 'banque', 'hypothèque'],
    response: "IvoryImmo peut vous orienter vers des partenaires bancaires pour le financement de votre acquisition. Nous travaillons avec plusieurs institutions financières de la place. Contactez-nous pour plus de détails sur les options disponibles !"
  },
  // Merci
  {
    patterns: ['merci', 'super', 'parfait', 'excellent', 'bravo', 'génial'],
    response: "Avec plaisir ! 😊 N'hésitez pas si vous avez d'autres questions. Nous sommes là pour vous aider à trouver le bien de vos rêves ! 🏠✨"
  },
  // Au revoir
  {
    patterns: ['au revoir', 'bye', 'bonne nuit', 'à bientôt', 'ciao'],
    response: "À bientôt ! 👋 N'hésitez pas à revenir si vous avez des questions. IvoryImmo est toujours là pour vous accompagner dans votre projet immobilier. Bonne journée !"
  },
];

const SUGGESTIONS_DEFAULT = [
  "Voir les appartements",
  "Prix des villas",
  "Comment vous contacter ?",
  "Biens en location"
];

function getBotResponse(userText) {
  const txt = userText.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  for (const item of CHAT_RESPONSES) {
    if (item.patterns.some(p => txt.includes(p.normalize('NFD').replace(/[\u0300-\u036f]/g, '')))) {
      return item.response;
    }
  }
  return "Je ne suis pas sûr de comprendre votre demande. 🤔 Vous pouvez me demander des infos sur nos <strong>appartements, studios, villas</strong>, les <strong>prix</strong>, la <strong>location</strong>, ou comment nous <strong>contacter</strong>. Ou appelez-nous directement au <strong>+225 00 00 00 00</strong> !";
}

function initChatbot() {
  const trigger = document.getElementById('chat-trigger');
  const window_ = document.getElementById('chat-window');
  const closeBtn = document.getElementById('chat-close');
  const input    = document.getElementById('chat-input');
  const sendBtn  = document.getElementById('chat-send');
  const messagesDiv = document.getElementById('chat-messages');
  const suggDiv  = document.getElementById('chat-suggestions');

  if (!trigger || !window_) return;

  let isOpen = false;
  let greeted = false;

  function toggleChat() {
    isOpen = !isOpen;
    window_.classList.toggle('open', isOpen);
    if (isOpen && !greeted) {
      greeted = true;
      setTimeout(() => {
        addBotMessage("Bonjour ! 👋 Je suis <strong>IvA</strong>, l'assistante virtuelle d'IvoryImmo. Comment puis-je vous aider aujourd'hui ?");
        showSuggestions(SUGGESTIONS_DEFAULT);
      }, 400);
    }
  }

  trigger.addEventListener('click', toggleChat);
  if (closeBtn) closeBtn.addEventListener('click', toggleChat);

  function getTime() {
    return new Date().toLocaleTimeString('fr-FR', {hour:'2-digit', minute:'2-digit'});
  }

  function addBotMessage(html, delay = 0) {
    const typing = addTyping();
    setTimeout(() => {
      typing.remove();
      const div = document.createElement('div');
      div.className = 'chat-msg bot';
      div.innerHTML = `<div class="chat-bubble">${html}</div><div class="chat-time">${getTime()}</div>`;
      messagesDiv.appendChild(div);
      scrollBottom();
    }, delay || 900);
  }

  function addUserMessage(text) {
    const div = document.createElement('div');
    div.className = 'chat-msg user';
    div.innerHTML = `<div class="chat-bubble">${escapeHtml(text)}</div><div class="chat-time">${getTime()}</div>`;
    messagesDiv.appendChild(div);
    scrollBottom();
  }

  function addTyping() {
    const div = document.createElement('div');
    div.className = 'chat-msg bot chat-typing';
    div.innerHTML = `<div class="chat-bubble"><div class="typing-dots"><span></span><span></span><span></span></div></div>`;
    messagesDiv.appendChild(div);
    scrollBottom();
    return div;
  }

  function scrollBottom() {
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
  }

  function showSuggestions(suggs) {
    if (!suggDiv) return;
    suggDiv.innerHTML = suggs.map(s =>
      `<button class="chat-sugg">${s}</button>`
    ).join('');
    suggDiv.querySelectorAll('.chat-sugg').forEach(btn => {
      btn.addEventListener('click', () => {
        sendMessage(btn.textContent);
        suggDiv.innerHTML = '';
      });
    });
  }

  function sendMessage(text) {
    text = text.trim();
    if (!text) return;
    addUserMessage(text);
    if (input) input.value = '';
    const response = getBotResponse(text);
    addBotMessage(response, 1000);
  }

  if (sendBtn) sendBtn.addEventListener('click', () => sendMessage(input.value));
  if (input) {
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') sendMessage(input.value);
    });
  }

  // Auto-open after 5s with tooltip
  setTimeout(() => {
    const tooltip = document.querySelector('.chat-tooltip');
    if (tooltip && !isOpen) {
      tooltip.style.opacity = '1';
      tooltip.style.transform = 'none';
      setTimeout(() => {
        tooltip.style.opacity = '';
        tooltip.style.transform = '';
      }, 3000);
    }
  }, 5000);
}

function escapeHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

// ============================================================
// INIT ON DOM READY
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
  initChatbot();
  refreshFavButtons();
});
