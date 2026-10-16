const cart = JSON.parse(localStorage.getItem('swarup-cart') || '[]');
let catalog = [];
const drawer = document.getElementById('cartDrawer');
const cartCount = document.getElementById('cartCount');
const drawerCount = document.getElementById('drawerCount');
const cartItems = document.getElementById('cartItems');
const cartTotal = document.getElementById('cartTotal');
const toast = document.getElementById('toast');

function saveCart() { localStorage.setItem('swarup-cart', JSON.stringify(cart)); }
function openCart() { drawer.classList.add('open'); drawer.setAttribute('aria-hidden', 'false'); }
function closeCart() { drawer.classList.remove('open'); drawer.setAttribute('aria-hidden', 'true'); }
function showToast(message = 'Added to your bag') { toast.textContent = message; toast.classList.add('show'); window.setTimeout(() => toast.classList.remove('show'), 1800); }

document.getElementById('cartButton').addEventListener('click', openCart);
document.getElementById('closeCart').addEventListener('click', closeCart);
document.getElementById('drawerBackdrop').addEventListener('click', closeCart);
document.querySelector('.menu-toggle').addEventListener('click', (event) => { const nav = document.getElementById('site-nav'); const isOpen = nav.classList.toggle('open'); event.currentTarget.setAttribute('aria-expanded', String(isOpen)); });
document.querySelectorAll('#site-nav a').forEach((link) => link.addEventListener('click', () => document.getElementById('site-nav').classList.remove('open')));

function renderCart() {
  const count = cart.reduce((sum, item) => sum + item.qty, 0);
  cartCount.textContent = count; drawerCount.textContent = count;
  if (!cart.length) { cartItems.innerHTML = '<p class="empty-cart">Your bag is waiting for a little self-care.</p>'; cartTotal.textContent = '₹0'; saveCart(); return; }
  cartItems.innerHTML = cart.map((item, index) => `<div class="cart-row"><span class="cart-thumb"></span><div><strong>${item.name}</strong><small>₹${item.price} × ${item.qty}</small></div><button class="remove-item" data-index="${index}" aria-label="Remove ${item.name}">×</button></div>`).join('');
  cartTotal.textContent = `₹${cart.reduce((sum, item) => sum + item.price * item.qty, 0)}`;
  document.querySelectorAll('.remove-item').forEach((button) => button.addEventListener('click', () => { cart.splice(Number(button.dataset.index), 1); renderCart(); }));
  saveCart();
}

function findVariant(size, packQuantity) { return catalog.flatMap((product) => product.variants).find((variant) => variant.size_gm === Number(size) && variant.pack_quantity === packQuantity); }
function addVariant(variant, fallbackName) {
  if (!variant || variant.price_pending || variant.price === null) { showToast('This price is pending confirmation'); return; }
  const product = { variantId: variant.id, name: fallbackName, price: Number(variant.price), qty: 1 };
  const existing = cart.find((item) => item.variantId === product.variantId);
  if (existing) existing.qty += 1; else cart.push(product);
  renderCart(); showToast();
}

function bindCatalog() {
  document.querySelectorAll('.size-product-card').forEach((card) => {
    const size = Number(card.dataset.name.match(/(\d+) GM/)?.[1]);
    const variant = findVariant(size, 1); const button = card.querySelector('.add-button');
    if (variant) button.addEventListener('click', () => addVariant(variant, card.dataset.name));
  });
  const packSize = document.getElementById('packSize'); const packPrice = document.getElementById('packPrice'); const addPackButton = document.getElementById('addPackButton');
  function updatePackDisplay() { const option = packSize.options[packSize.selectedIndex]; const variant = findVariant(option.value, 10); if (!variant || variant.price_pending || variant.price === null) { packPrice.textContent = 'Price pending'; addPackButton.disabled = true; return; } packPrice.textContent = `₹${variant.price}`; addPackButton.disabled = false; }
  packSize.querySelectorAll('option').forEach((option) => { const variant = findVariant(option.value, 10); option.textContent = !variant || variant.price_pending || variant.price === null ? `${option.value} GM · price pending` : `${option.value} GM · ₹${variant.price}`; });
  packSize.addEventListener('change', updatePackDisplay); addPackButton.addEventListener('click', () => { const option = packSize.options[packSize.selectedIndex]; addVariant(findVariant(option.value, 10), `Swarup Soap · Pack of 10 · ${option.value} GM`); }); updatePackDisplay();
}

const staticCatalog = [{ id: 1, name: 'Swarup Soap', description: 'Everyday bathing bars made in Nadgaon, Nashik.', image_path: 'assets/soap-15gm.jpg', variants: [
  { id: 1, size_gm: 15, pack_quantity: 1, sku: 'SWARUP-15-SINGLE', price: 15, stock_quantity: 100, is_active: true, price_pending: false },
  { id: 2, size_gm: 20, pack_quantity: 1, sku: 'SWARUP-20-SINGLE', price: 20, stock_quantity: 100, is_active: true, price_pending: false },
  { id: 3, size_gm: 50, pack_quantity: 1, sku: 'SWARUP-50-SINGLE', price: 30, stock_quantity: 100, is_active: true, price_pending: false },
  { id: 4, size_gm: 100, pack_quantity: 1, sku: 'SWARUP-100-SINGLE', price: 50, stock_quantity: 100, is_active: true, price_pending: false },
  { id: 5, size_gm: 15, pack_quantity: 10, sku: 'SWARUP-15-PACK10', price: 100, stock_quantity: 50, is_active: true, price_pending: false },
  { id: 6, size_gm: 20, pack_quantity: 10, sku: 'SWARUP-20-PACK10', price: null, stock_quantity: 0, is_active: false, price_pending: true },
  { id: 7, size_gm: 50, pack_quantity: 10, sku: 'SWARUP-50-PACK10', price: 250, stock_quantity: 50, is_active: true, price_pending: false },
  { id: 8, size_gm: 100, pack_quantity: 10, sku: 'SWARUP-100-PACK10', price: 400, stock_quantity: 50, is_active: true, price_pending: false },
] }];

async function loadCatalog() { try { const response = await fetch('/api/products'); if (!response.ok) throw new Error('Catalog request failed'); catalog = await response.json(); } catch (error) { console.info('Static GitHub Pages catalog fallback in use.'); catalog = staticCatalog; } bindCatalog(); }

document.getElementById('checkoutButton').addEventListener('click', () => { if (!cart.length) { showToast('Add a bar to your bag first'); return; } const summary = cart.map((item) => `${item.name} x${item.qty}`).join(', '); window.open(`https://wa.me/918888799462?text=${encodeURIComponent(`Hello Swarup Soap, I would like to enquire about: ${summary}. Please share availability and delivery details.`)}`, '_blank'); });
const observer = new IntersectionObserver((entries) => entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.style.opacity = '1'; entry.target.style.transform = 'translateY(0)'; observer.unobserve(entry.target); } }), { threshold: 0.12 });
document.querySelectorAll('.product-card,.value,.media-tile,.contact-card').forEach((element) => { element.style.opacity = '0'; element.style.transform = 'translateY(14px)'; element.style.transition = 'opacity .7s ease, transform .7s ease'; observer.observe(element); });
renderCart(); loadCatalog();
