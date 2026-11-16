// ====== EDIT THESE ======
const CONFIG = {
  whatsapp: "910000000000",            // country code + number, no "+" or spaces
  phoneDisplay: "+91 00000 00000",
  instagram: "https://instagram.com/thepaanbox",
  currency: "₹",
};

const PRODUCTS = [
  { name: "Meetha Paan",        cat: "classic", emoji: "🍃", price: 40,   desc: "Gulkand, saunf, coconut and cherry in a fresh betel leaf." },
  { name: "Sada Paan",          cat: "classic", emoji: "🌿", price: 30,   desc: "Simple and traditional: lime, katha and light fennel." },
  { name: "Chocolate Paan",     cat: "classic", emoji: "🍫", price: 60,   desc: "Dark chocolate, gulkand and crunchy nuts. A modern favourite." },
  { name: "Fire Paan",          cat: "premium", emoji: "🔥", price: 90,   desc: "Flaming showstopper — a party-counter classic." },
  { name: "Silver Leaf Paan",   cat: "premium", emoji: "✨", price: 120,  desc: "Edible silver varak, saffron gulkand and dry fruits." },
  { name: "Royal Rose Paan",    cat: "premium", emoji: "🌹", price: 110,  desc: "Rose petal preserve, cardamom and pistachio." },
  { name: "Classic Gift Box (6)",cat: "box",    emoji: "🎁", price: 299,  desc: "Six assorted paans in a keepsake box." },
  { name: "Celebration Box (12)",cat: "box",    emoji: "🎊", price: 599,  desc: "Twelve paans with silver-leaf specials and dry fruits." },
  { name: "Custom Wedding Box", cat: "box",     emoji: "💍", price: null, desc: "Colours, names and quantities tailored to your event." },
];
// ========================

const wa = msg => `https://wa.me/${CONFIG.whatsapp}?text=${encodeURIComponent(msg)}`;

function renderProducts(filter = "all") {
  const el = document.getElementById("products");
  el.innerHTML = "";
  PRODUCTS.filter(p => filter === "all" || p.cat === filter).forEach(p => {
    const card = document.createElement("article");
    card.className = "card";
    const tag = { classic: "Classic", premium: "Premium", box: "Gift Box" }[p.cat];
    const price = p.price ? CONFIG.currency + p.price : "On request";
    card.innerHTML = `
      <div class="art" style="background:${p.cat === "box" ? "#f3e6bf" : p.cat === "premium" ? "#e2efdf" : "#eef4e6"}">${p.emoji}</div>
      <div class="body">
        <span class="tag">${tag}</span>
        <h3></h3><p></p>
        <div class="row"><span class="price">${price}</span><a class="btn btn-gold" target="_blank" rel="noopener">Order</a></div>
      </div>`;
    card.querySelector("h3").textContent = p.name;
    card.querySelector("p").textContent = p.desc;
    card.querySelector("a").href = wa(`Hi! I'd like to order: ${p.name}${p.price ? " (" + price + ")" : ""}.`);
    el.appendChild(card);
  });
}

document.querySelectorAll(".chip").forEach(c => c.addEventListener("click", () => {
  document.querySelectorAll(".chip").forEach(x => x.classList.remove("active"));
  c.classList.add("active");
  renderProducts(c.dataset.filter);
}));

document.querySelectorAll(".wa-link").forEach(a => {
  a.href = wa(a.dataset.msg || "Hi!");
  a.target = "_blank";
  a.rel = "noopener";
});

document.getElementById("phoneText").textContent = CONFIG.phoneDisplay;
document.getElementById("igLink").href = CONFIG.instagram;
document.getElementById("year").textContent = new Date().getFullYear();

document.getElementById("enquiry").addEventListener("submit", e => {
  e.preventDefault();
  const f = new FormData(e.target);
  const msg = `Hi! I'm ${f.get("name")}.\nInterested in: ${f.get("what") || "-"}\nDate needed: ${f.get("date") || "-"}\n${f.get("msg") || ""}`;
  window.open(wa(msg), "_blank", "noopener");
});

const btn = document.querySelector(".menu-btn"), nav = document.querySelector(".nav nav");
btn.addEventListener("click", () => btn.setAttribute("aria-expanded", nav.classList.toggle("open")));
nav.addEventListener("click", e => { if (e.target.tagName === "A") { nav.classList.remove("open"); btn.setAttribute("aria-expanded", "false"); } });

renderProducts();
