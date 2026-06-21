#!/usr/bin/env python3
# build-pages-v1.py — stamps the full Tesote sitemap prototype from the locked v53 design system.
# Output: 15 page-*.html + v54-homepage.html (new mega-menu nav, footer, chapter links -> pages).
# Re-runnable: regenerates everything from v53 + the data dicts below.
import re, sys

SRC = open('v53-homepage.html').read()
HOME = 'v61-homepage.html'
DEMO = HOME + '#agenda'

# ---------- v56 chrome patches (Luis 2026-06-12) ----------
# Flat chrome: hero has NO wave-bars and NO gradient; CTA band is the light surface with NO gradient.
# (v55's black-gradient experiment reverted same day.)
_s = re.sub(r'\n?\s*<div class="hero-lines".*?</div>', '', SRC, count=1)
assert _s != SRC, 'v56: hero-lines div not removed'
SRC = _s
_s = re.sub(r'<style id="hero-lines-v52">.*?</style>\n*', '', SRC, count=1, flags=re.S)
assert _s != SRC, 'v56: hero-lines CSS not removed'
SRC = _s
_old_glow = 'background: radial-gradient(ellipse at top, rgba(18,17,15,0.05), transparent 60%);'
assert SRC.count(_old_glow) == 1, 'v56: hero glow anchor not found'
SRC = SRC.replace(_old_glow, 'display: none;')  # .hero::before { display: none; } — flat hero
CTA_FLAT_V56 = '''<style id="cta-flat-v56">
  /* v56: CTA band flat — light surface, no gradient (kills the compiled CSS blue radial glow). */
  .cta-section::before { display: none; }
</style>'''
_m = re.search(r'<style id="cta-dark-v53">.*?</style>', SRC, re.S)
assert _m, 'v56: cta-dark block not found'
SRC = SRC.replace(_m.group(0), CTA_FLAT_V56, 1)

# ---------- extract locked design-system blocks from v53 ----------
def grab(pattern, label):
    m = re.search(pattern, SRC, re.S)
    assert m, 'extraction failed: ' + label
    return m.group(0)

LIGHT     = grab(r'<style id="light-theme-overrides">.*?</style>', 'light')
DENSITY   = grab(r'<style id="density-pass">.*?</style>', 'density')
CTA_DARK  = grab(r'<style id="cta-flat-v56">.*?</style>', 'cta-flat')
HERO15    = grab(r'<style id="hero-pass-v15">.*?</style>', 'hero15')
CHAPTERS  = grab(r'<style>\s*/\* ===== Story chapters.*?</style>', 'chapters')
PCARD     = grab(r'<style>\s*/\* ===== Product row \(Brex-style\).*?</style>', 'pcard')
TESTI_CSS = grab(r'<style>\s*\.testi-grid.*?</style>', 'testi')
FAQ_CSS   = grab(r'<style>\s*\.booking.*?</style>', 'faq')
CTA_BAND  = grab(r'<section class="section">\s*<style>\s*\.cta-section__list.*?</section>', 'cta-band')
STATS     = grab(r'<section class="stat-grid-section".*?</section>', 'stats')
TESTI_SEC = grab(r'<section id="testimonios".*?</section>', 'testi-sec')
FAB       = grab(r'<a class="whatsapp-fab".*?</a>', 'fab')

CTA_BAND_PAGES = CTA_BAND.replace('href="#agenda"', 'href="' + DEMO + '"')

# ---------- nav / mega menu ----------
MEGA_CSS = '''<style id="mega-nav-v57">
  /* v57 mega-menu — Brex 1:1 (Luis ref screenshot 2026-06-12), Tesote blue as the accent.
     Sheet spans the CONTAINER (logo -> CTA button), not the viewport. CSS-only hover/focus. */
  .site-navbar__inner { position: relative; }
  .site-navbar__nav-item { position: static; }
  .site-navbar__link .mega-caret { font-size: .55rem; margin-left: .35rem; opacity: .6; position: relative; top: -1px; transition: transform .18s ease, color .18s ease; }
  /* open trigger = bordered box + caret flips and tints blue (Brex: orange) */
  .site-navbar__nav-item--dd > .site-navbar__link { border: 1px solid transparent; border-radius: 8px; }
  .site-navbar__nav-item--dd:hover > .site-navbar__link,
  .site-navbar__nav-item--dd:focus-within > .site-navbar__link {
    border-color: var(--border-strong); background: #FFFFFF;
  }
  .site-navbar__nav-item--dd:hover > .site-navbar__link .mega-caret,
  .site-navbar__nav-item--dd:focus-within > .site-navbar__link .mega-caret {
    transform: rotate(180deg); color: var(--accent); opacity: 1;
  }
  /* the sheet */
  .mega {
    position: absolute; top: 100%; left: 0; right: 0; z-index: 1200; text-align: left;
    display: flex; gap: 3rem; padding: 1.6rem 1.5rem 2.4rem;
    background: #FFFFFF; border: 1px solid var(--border-subtle); border-radius: 0 0 16px 16px;
    box-shadow: 0 30px 60px rgba(18, 17, 15, 0.14);
    opacity: 0; visibility: hidden; pointer-events: none; transform: translateY(-8px);
    transition: opacity .18s ease, transform .18s ease, visibility .18s;
  }
  .mega::before { content: ""; position: absolute; top: -16px; left: 0; right: 0; height: 16px; }
  .site-navbar__nav-item:hover > .mega,
  .site-navbar__nav-item:focus-within > .mega {
    opacity: 1; visibility: visible; pointer-events: auto; transform: translateY(0);
  }
  /* zones: sentence-case header + hairline rule, then an item grid */
  .mega__zone { flex: 1; min-width: 0; }
  .mega__zone--grow { flex: 1.7; }
  .mega__head {
    font-family: var(--font-display); font-size: .82rem; font-weight: var(--fw-medium);
    color: var(--text-secondary); padding-bottom: .65rem; border-bottom: 1px solid var(--border-subtle);
    margin-bottom: 1rem;
  }
  .mega__grid { display: grid; grid-template-columns: 1fr; gap: .35rem 1.5rem; }
  .mega__grid--2 { grid-template-columns: 1fr 1fr; }
  /* items: big white icon tile; on hover the ROW tints gray and the GLYPH tints blue (tile stays white) */
  .mega__item { display: flex; align-items: center; gap: .9rem; padding: .6rem .7rem; border-radius: 12px; text-decoration: none; }
  .mega__item:hover, .mega__item:focus-visible { background: var(--bg-surface-2); }
  .mega__icon {
    inline-size: 44px; block-size: 44px; flex: none; display: inline-flex; align-items: center; justify-content: center;
    background: #FFFFFF; border: 1px solid var(--border-subtle); border-radius: 11px;
    color: var(--text-primary); font-size: 1rem; box-shadow: var(--shadow-sm);
  }
  .mega__item:hover .mega__icon i { color: var(--accent); }
  .mega__txt { display: flex; flex-direction: column; gap: 2px; }
  .mega__title { font-size: .9rem; font-weight: var(--fw-semi); color: var(--text-primary); font-family: var(--font-display); }
  .mega__desc { font-size: .78rem; color: var(--text-muted); }
  @media (max-width: 991px) { .mega { display: none; } }

  /* footer grid (pages exist) */
  .site-footer__nav { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 2rem; }
  @media (max-width: 991px) { .site-footer__nav { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 560px) { .site-footer__nav { grid-template-columns: 1fr; } }
</style>'''

def mega_item(href, icon, title, desc):
    return ('<a class="mega__item" href="%s"><span class="mega__icon"><i class="fa-solid %s" aria-hidden="true"></i></span>'
            '<span class="mega__txt"><span class="mega__title">%s</span><span class="mega__desc">%s</span></span></a>'
            % (href, icon, title, desc))

PRODUCTOS_ITEMS = [
    ('page-connect.html',      'fa-building-columns', 'Connect',                 'Saldos y movimientos, en vivo'),
    ('page-pagos.html',        'fa-money-bill-transfer', 'Pagos',                'Individuales o masivos, desde tu ERP'),
    ('page-cobros.html',       'fa-link',             'Cobros',                  'Débito inmediato o botón, vía enlace'),
    ('page-conciliacion.html', 'fa-check-double',     'Conciliación automática', 'Tu banco y tu ERP, en sync'),
]
PLATAFORMA_ITEMS = [
    ('page-tesote-ai.html',     'fa-wand-magic-sparkles', 'Tesote AI',     'Agentes para tus finanzas'),
    ('page-integraciones.html', 'fa-plug',                'Integraciones', 'Tu ERP, en ambas direcciones'),
    ('page-seguridad.html',     'fa-shield-halved',       'Seguridad',     'Cifrado, permisos y auditoría'),
]
TAMANO_ITEMS = [
    ('page-medianas.html',     'fa-building', 'Medianas',     'Equipos financieros de 5-20 personas'),
    ('page-corporativas.html', 'fa-city',     'Corporativas', 'Equipos financieros de 20+ personas'),
]
INDUSTRIA_ITEMS = [
    ('page-retail.html',                'fa-bag-shopping', 'Retail y consumo masivo',    'Cuadre diario multi-tienda'),
    ('page-alimentos.html',             'fa-utensils',     'Alimentos y Agricultura',    'De la producción a la venta, cuadrado'),
    ('page-distribucion.html',          'fa-truck-fast',   'Distribución y Manufactura', 'Cartera B2B cobrada y cuadrada'),
    ('page-servicios-financieros.html', 'fa-landmark',     'Servicios Financieros',      'Cobros masivos, identificados solos'),
    ('page-tecnologia.html',            'fa-microchip',    'Tecnología',                 'Cobros recurrentes y multi-moneda'),
    ('page-petroleo-gas.html',          'fa-oil-well',     'Petróleo y Gas',             'Multi-moneda y alto monto, cuadrado'),
]
PARTNER_ITEMS = [
    ('page-partners.html', 'fa-handshake', 'Programa de partners', 'Integradores, consultoras, contables y asesores'),
]
RECURSOS_ITEMS = [
    ('https://marketing.tesote.com/blog', 'fa-newspaper',       'Blog',            'Ideas y guías de finanzas'),
    ('#',                                  'fa-circle-question', 'Centro de ayuda', 'Documentación y soporte'),
]

def zone(head, items, grid2=False, grow=False):
    """Brex-style zone: sentence-case header + hairline rule + item grid (1 or 2 cols)."""
    zcls = 'mega__zone' + (' mega__zone--grow' if grow else '')
    gcls = 'mega__grid' + (' mega__grid--2' if grid2 else '')
    return ('<div class="%s"><div class="mega__head">%s</div><div class="%s">%s</div></div>'
            % (zcls, head, gcls, ''.join(mega_item(*i) for i in items)))

def build_nav(demo_href):
    mega_prod = '<div class="mega">%s%s</div>' % (
        zone('Productos', PRODUCTOS_ITEMS, grid2=True, grow=True), zone('Plataforma', PLATAFORMA_ITEMS))
    mega_sol  = '<div class="mega">%s%s%s</div>' % (
        zone('Por tamaño', TAMANO_ITEMS), zone('Por industria', INDUSTRIA_ITEMS, grid2=True, grow=True), zone('Partners', PARTNER_ITEMS))
    mega_rec  = '<div class="mega">%s</div>' % zone('Recursos', RECURSOS_ITEMS, grid2=True, grow=True)
    caret = '<i class="fa-solid fa-chevron-down mega-caret" aria-hidden="true"></i>'
    drawer_links = (PRODUCTOS_ITEMS + PLATAFORMA_ITEMS + TAMANO_ITEMS + INDUSTRIA_ITEMS + PARTNER_ITEMS
                    + [('page-clientes.html', '', 'Clientes', '')])
    drawer_lis = ''.join('<li><a class="site-navbar__drawer-link site-navbar__drawer-link--top" href="%s">%s</a></li>' % (h, t)
                         for (h, ic, t, d) in drawer_links)
    return '''<nav class="site-navbar" aria-label="Primary">
  <div class="container site-navbar__inner">
    <a class="site-navbar__brand" href="''' + HOME + '''" aria-label="Tesote">
      <img class="site-navbar__brand-wordmark" alt="Tesote" src="current/assets/logos/tesote/text-white-9d9d1f73.svg" />
    </a>
    <ul class="site-navbar__nav">
      <li class="site-navbar__nav-item site-navbar__nav-item--dd"><a class="site-navbar__link" href="#" onclick="return false">Productos ''' + caret + '''</a>''' + mega_prod + '''</li>
      <li class="site-navbar__nav-item site-navbar__nav-item--dd"><a class="site-navbar__link" href="#" onclick="return false">Soluciones ''' + caret + '''</a>''' + mega_sol + '''</li>
      <li class="site-navbar__nav-item"><a class="site-navbar__link" href="page-clientes.html">Clientes</a></li>
      <li class="site-navbar__nav-item site-navbar__nav-item--dd"><a class="site-navbar__link" href="#" onclick="return false">Recursos ''' + caret + '''</a>''' + mega_rec + '''</li>
    </ul>
    <div class="site-navbar__right">
      <a href="https://equipo.tesote.com/users/sign_in" class="btn btn-sm site-navbar__login" target="_blank" rel="noopener">
        <i class="fa-solid fa-arrow-right-to-bracket me-1" aria-hidden="true"></i>
        Acceder
      </a>
      <a href="''' + demo_href + '''" class="btn btn-primary btn-sm site-navbar__cta">
        Agenda una demo
        <i class="fa-solid fa-arrow-right ms-2" aria-hidden="true"></i>
      </a>
    </div>
    <button type="button" class="site-navbar__toggle" onclick="document.getElementById('site-navbar-drawer').classList.toggle('is-open')" aria-label="Abrir menú" aria-controls="site-navbar-drawer">
      <i class="fa-solid fa-bars" aria-hidden="true"></i>
    </button>
  </div>
  <div class="site-navbar__drawer" id="site-navbar-drawer">
    <div class="site-navbar__drawer-backdrop" onclick="document.getElementById('site-navbar-drawer').classList.remove('is-open')" aria-hidden="true"></div>
    <aside class="site-navbar__drawer-panel" role="dialog" aria-modal="true" aria-label="Menú">
      <div class="site-navbar__drawer-header">
        <span class="site-navbar__drawer-title">Menú</span>
        <button type="button" class="site-navbar__drawer-close" onclick="document.getElementById('site-navbar-drawer').classList.remove('is-open')" aria-label="Cerrar">
          <i class="fa-solid fa-xmark" aria-hidden="true"></i>
        </button>
      </div>
      <div class="site-navbar__drawer-body"><ul class="site-navbar__drawer-list">''' + drawer_lis + '''</ul></div>
      <div class="site-navbar__drawer-footer">
        <a href="https://equipo.tesote.com/users/sign_in" class="btn btn-outline-light w-100 mt-3" target="_blank" rel="noopener">
          <i class="fa-solid fa-arrow-right-to-bracket me-1" aria-hidden="true"></i>
          Acceder
        </a>
        <a href="''' + demo_href + '''" class="btn btn-primary w-100 mt-2">Agenda una demo</a>
      </div>
    </aside>
  </div>
</nav>'''

NAV_PAGES = build_nav(DEMO)
NAV_HOME  = build_nav('#agenda')

# ---------- footer ----------
def flink(href, label):
    return '<li><a class="site-footer__link" href="%s">%s</a></li>' % (href, label)

def build_footer(demo_href):
    prod = ''.join(flink(h, t) for (h, ic, t, d) in PRODUCTOS_ITEMS)
    plat = ''.join(flink(h, t) for (h, ic, t, d) in PLATAFORMA_ITEMS)
    sol  = ''.join(flink(h, t) for (h, ic, t, d) in TAMANO_ITEMS + PARTNER_ITEMS)
    comp = (flink('page-clientes.html', 'Clientes')
            + flink('https://marketing.tesote.com/blog', 'Blog')
            + flink('#', 'Centro de ayuda')
            + flink('https://equipo.tesote.com/users/sign_in', 'Iniciar sesión')
            + flink(demo_href, 'Agenda una demo'))
    return '''<footer class="site-footer">
  <div class="container">
    <div class="site-footer__top">
      <div class="site-footer__brand">
        <img class="site-footer__logo" alt="Tesote" src="current/assets/logos/tesote/text-white-9d9d1f73.svg" />
        <p class="site-footer__tagline">Automatización Financiera</p>
        <ul class="social-links social-links--icons">
          <li><a href="https://www.linkedin.com/company/tesote" class="social-links__item" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn"><i class="fa-brands fa-linkedin-in" aria-hidden="true"></i></a></li>
          <li><a href="https://x.com/tesote_" class="social-links__item" target="_blank" rel="noopener noreferrer" aria-label="X (Twitter)"><i class="fa-brands fa-x-twitter" aria-hidden="true"></i></a></li>
          <li><a href="https://www.instagram.com/tesote__" class="social-links__item" target="_blank" rel="noopener noreferrer" aria-label="Instagram"><i class="fa-brands fa-instagram" aria-hidden="true"></i></a></li>
        </ul>
      </div>
      <div class="site-footer__nav">
        <div class="site-footer__nav-col"><h6 class="site-footer__col-heading">Productos</h6><ul class="site-footer__list">''' + prod + '''</ul></div>
        <div class="site-footer__nav-col"><h6 class="site-footer__col-heading">Plataforma</h6><ul class="site-footer__list">''' + plat + '''</ul></div>
        <div class="site-footer__nav-col"><h6 class="site-footer__col-heading">Soluciones</h6><ul class="site-footer__list">''' + sol + '''</ul></div>
        <div class="site-footer__nav-col"><h6 class="site-footer__col-heading">Compañía</h6><ul class="site-footer__list">''' + comp + '''</ul></div>
      </div>
    </div>
    <div class="site-footer__bottom">
      <p class="site-footer__copyright">&copy; 2026 Tesote. Todos los derechos reservados.</p>
      <ul class="site-footer__legal-links">
        <li><a href="/privacidad">Política de Privacidad</a></li>
        <li><a href="/terminos">Términos y Condiciones</a></li>
      </ul>
    </div>
  </div>
</footer>'''

FOOTER_PAGES = build_footer(DEMO)
FOOTER_HOME  = build_footer('#agenda')

# ---------- page chrome css ----------
PAGE_CSS = '''<style id="page-shell-v1">
  /* page hero (phero) — does NOT use .hero so the homepage 100svh density rule never applies */
  .phero { position: relative; background: var(--bg-hero); overflow: hidden; padding-block: 4.5rem 6rem; }
  /* v56: flat hero — no lines, no gradient */
  .phero > .container { position: relative; z-index: 2; }
  .phero__grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: 3rem; align-items: center; }
  @media (max-width: 900px) { .phero__grid { grid-template-columns: 1fr; } .phero { padding-block: 3rem 6rem; } }
  .phero__eyebrow { display: block; font-family: var(--font-display); font-size: var(--fs-sm); font-weight: var(--fw-semi); letter-spacing: var(--tracking-wide); text-transform: uppercase; color: var(--accent); margin-bottom: var(--space-3); }
  .phero__title { font-family: var(--font-display); font-size: clamp(2rem, 3.2vw, 2.75rem); font-weight: var(--fw-semi); line-height: var(--lh-tight); letter-spacing: var(--tracking-tight); color: var(--text-primary); margin: 0 0 var(--space-4); }
  .phero__sub { font-size: 1.0625rem; color: var(--text-muted); line-height: var(--lh-normal); margin: 0 0 var(--space-6); max-width: 54ch; }
  .phero--center { text-align: center; }
  .phero--center .phero__sub { margin-inline: auto; }
  .phero--dark { background: #12110F; }
  .phero--dark .phero__title { color: #FFFFFF; }
  .phero--dark .phero__sub { color: #C7C0B5; }
  .phero--dark .phero__eyebrow { color: var(--tesote-blue-300); }
  /* helpers */
  .pcard-grid--fit { grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); }
  .logo-wall { display: flex; flex-wrap: wrap; gap: 2.2rem 3rem; justify-content: center; align-items: center; padding-block: var(--space-8); }
  .logo-wall img { filter: grayscale(1) brightness(0.25) opacity(0.75); max-width: 124px; max-height: 38px; width: auto; height: auto; }
  .logo-wall--sm img { max-width: 104px; max-height: 32px; }
  .testi-grid--one { grid-template-columns: minmax(0, 620px); justify-content: center; }
  .section--head-only { padding-block: var(--space-12) var(--space-4); }
  .mock-arrow { display: flex; justify-content: center; padding: 2px 0; color: var(--tesote-success); font-size: var(--fs-xs); }
</style>'''


# ---------- shared mock snippets (reuse locked homepage panels; ids de-duped) ----------
PANEL_CONNECT = '''<div class="chapter__panel" aria-hidden="true">
  <div class="ui-card">
    <div class="ui-card__label">Posición consolidada · USD · En vivo</div>
    <div class="ui-card__figure">$1.545.220,80</div>
    <div class="pcard__chip"><span class="pcard__dot"></span><span class="pcard__chip-label">Cuenta Operativa</span><span class="pcard__chip-value">Bs. 18.245.709</span></div>
    <div class="pcard__chip"><span class="pcard__dot"></span><span class="pcard__chip-label">Cuenta Nómina</span><span class="pcard__chip-value">Bs. 6.420.330</span></div>
    <div class="pcard__chip"><span class="pcard__dot"></span><span class="pcard__chip-label">Cuenta en USD</span><span class="pcard__chip-value">$84.210</span></div>
  </div>
  <div class="ui-card">
    <div class="ui-card__label">Flujo de caja · últimos 30 días</div>
    <svg class="chapter-flow-chart" viewBox="0 0 320 56" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
      <defs><linearGradient id="pg-flow" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1661E2" stop-opacity="0.3"/><stop offset="100%" stop-color="#1661E2" stop-opacity="0"/></linearGradient></defs>
      <path d="M0 42 L40 37 L80 44 L120 29 L160 33 L200 20 L240 24 L280 11 L320 8 L320 56 L0 56 Z" fill="url(#pg-flow)"/>
      <path d="M0 42 L40 37 L80 44 L120 29 L160 33 L200 20 L240 24 L280 11 L320 8" stroke="#1661E2" stroke-width="2" stroke-linejoin="round"/>
    </svg>
    <div class="chapter-flow-deltas">
      <span class="chapter-flow--in"><i class="fa-solid fa-caret-up" aria-hidden="true"></i> Entró $84,2K</span>
      <span class="chapter-flow--out"><i class="fa-solid fa-caret-down" aria-hidden="true"></i> Salió $31,5K</span>
      <span class="chapter-flow--in">Neto +$52,7K</span>
    </div>
  </div>
  <p class="chapter__panel-note">+120 bancos · VE · Panamá · RD · EE.&nbsp;UU.</p>
</div>'''

PANEL_PAGOS = '''<div class="chapter__panel" aria-hidden="true">
  <div class="ui-card">
    <div class="ui-card__label">Lote #88 · 23 proveedores</div>
    <div class="ui-card__figure" style="font-size: var(--fs-xl);">$48.250,00</div>
    <div class="chapter-steps">
      <div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>Validado contra facturas y retenciones</span></div>
      <div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>Aprobado por la directora de finanzas</span></div>
      <div class="chapter-step chapter-step--working"><i class="fa-solid fa-circle-notch fa-spin" aria-hidden="true"></i><span>Ejecutando por API bancaria…</span></div>
      <div class="chapter-step chapter-step--pending"><i class="fa-regular fa-circle" aria-hidden="true"></i><span>Asiento en tu ERP — se registra solo</span></div>
    </div>
  </div>
  <div class="ui-card">
    <div class="pcard__chip"><span class="pcard__chip-label">Pago anterior · #87</span><span class="pcard__chip-value">$31.900,00</span><span class="pcard__pill">Conciliado</span></div>
  </div>
  <p class="chapter__panel-note">Por la API oficial de tu banco</p>
</div>'''

PANEL_COBROS = '''<div class="chapter__panel" aria-hidden="true">
  <div class="ui-card">
    <div class="ui-card__label">Factura #2210 · Bs. 312.500,00</div>
    <div class="chapter-steps">
      <div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>Link enviado al cliente · lun 9:00 am</span></div>
      <div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>Abierto · lun 9:42 am</span></div>
      <div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>Pagado por pago móvil · lun 10:15 am</span></div>
      <div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>Conciliado y registrado en tu ERP · automático</span></div>
    </div>
  </div>
  <div class="ui-card">
    <div class="ui-card__label">Este mes</div>
    <div class="pcard__chip"><span class="pcard__chip-label">64 cobros por link</span><span class="pcard__chip-value">Bs. 18.840.000</span><span class="pcard__pill">Todo conciliado</span></div>
  </div>
  <p class="chapter__panel-note">Sin recordatorios manuales, sin cruzar nada</p>
</div>'''

MATCH_SVG = '''<div class="pcard__match">
  <svg width="16" height="14" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M8 0v14" stroke="#24AD72" stroke-width="1.5" stroke-dasharray="2 2"/>
    <circle cx="8" cy="7" r="5" fill="#FFFFFF" stroke="#24AD72" stroke-width="1.5"/>
    <path d="M5.8 7l1.5 1.5L10.2 5.6" stroke="#24AD72" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</div>'''

PANEL_CONCILIA = '''<div class="chapter__panel" aria-hidden="true">
  <div class="ui-card">
    <div class="ui-card__label">Match automático</div>
    <div class="pcard__chip"><span class="pcard__chip-label">Banco · Transferencia</span><span class="pcard__chip-value">$4.520,00</span></div>
    ''' + MATCH_SVG + '''
    <div class="pcard__chip"><span class="pcard__chip-label">ERP · Factura #1042</span><span class="pcard__pill">Conciliado</span></div>
  </div>
  <div class="ui-card">
    <div class="ui-card__label">Devuelto a tu ERP</div>
    <div class="pcard__chip"><span class="pcard__chip-label">Partida conciliada · #1042</span><span class="pcard__pill">Registrada</span></div>
    <div class="pcard__chip"><span class="pcard__chip-label">Proveedor nuevo · creado</span><span class="pcard__pill pcard__pill--accent">Sincronizado</span></div>
  </div>
  <p class="chapter__panel-note">En ambas direcciones — sube enriquecido, baja conciliado</p>
</div>'''

PANEL_AI_DIGEST = '''<div class="chapter__panel" aria-hidden="true">
  <div class="pcard__bubble pcard__bubble--user">Mándame un resumen de la semana pasada.</div>
  <div class="pcard__bubble pcard__bubble--ai ai-digest">
    <p class="ai-digest__lead">Semana del 25 al 31 de mayo — conciliada y lista.</p>
    <div class="ai-digest__neto">
      <span class="ai-digest__neto-value">Neto +$58.440</span>
      <span class="ai-digest__neto-sub">entradas $214.380 · salidas $155.940 · tu mejor semana del mes</span>
    </div>
    <p class="ai-digest__label">Por qué</p>
    <ul class="ai-digest__list">
      <li>Cobros +23% vs. la semana previa; 88% de tus clientes al día.</li>
      <li>Salida no recurrente: $18.600 en honorarios (tu firma legal).</li>
    </ul>
    <p class="ai-digest__label">Quiénes</p>
    <ul class="ai-digest__list">
      <li>Top entradas: Distribuidora Caruba $32.500 y Comercial Vethia $24.800. Nueva: Academia Norvel (+$7.450).</li>
    </ul>
    <p class="ai-digest__label">Lo que ya hice por ti</p>
    <ul class="ai-digest__list">
      <li>Concilié el 93% en tu ERP y categoricé los 318 movimientos (solo 4 por revisar).</li>
      <li>Detuve una factura duplicada de $7.490 antes de pagarla.</li>
    </ul>
    <p class="ai-digest__label">Atención</p>
    <ul class="ai-digest__list">
      <li>Una transferencia interna de $9.800 sigue en tránsito desde el viernes.</li>
      <li>$48.250 en pagos a proveedores vencen el jueves — listos para tu aprobación.</li>
    </ul>
  </div>
  <div class="ai-actions">
    <span class="ai-action"><i class="fa-solid fa-bookmark" aria-hidden="true"></i>Guardar como mi reporte</span>
    <span class="ai-action"><i class="fa-solid fa-arrows-rotate" aria-hidden="true"></i>Correr cada lunes</span>
  </div>
  <p class="chapter__panel-note">Con tus bancos, tus pagos y tu ERP ya conectados</p>
</div>'''

# smaller chapter mocks
def panel(*cards, note=None):
    n = '<p class="chapter__panel-note">%s</p>' % note if note else ''
    return '<div class="chapter__panel" aria-hidden="true">%s%s</div>' % (''.join(cards), n)

def card(label, *rows):
    lab = '<div class="ui-card__label">%s</div>' % label if label else ''
    return '<div class="ui-card">%s%s</div>' % (lab, ''.join(rows))

def chip(label, value=None, pill=None, accent=False, dot=False):
    d = '<span class="pcard__dot"></span>' if dot else ''
    v = '<span class="pcard__chip-value">%s</span>' % value if value else ''
    p = '<span class="pcard__pill%s">%s</span>' % (' pcard__pill--accent' if accent else '', pill) if pill else ''
    return '<div class="pcard__chip">%s<span class="pcard__chip-label">%s</span>%s%s</div>' % (d, label, v, p)

def step(text, state='done'):
    if state == 'working':
        return '<div class="chapter-step chapter-step--working"><i class="fa-solid fa-circle-notch fa-spin" aria-hidden="true"></i><span>%s</span></div>' % text
    if state == 'pending':
        return '<div class="chapter-step chapter-step--pending"><i class="fa-regular fa-circle" aria-hidden="true"></i><span>%s</span></div>' % text
    return '<div class="chapter-step"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>%s</span></div>' % text

MOCK_TX = panel(card('Transferencia recibida · hoy 10:42 am',
    chip('Monto', '$4.520,00'),
    chip('Categoría · Ventas', None, 'Automática'),
    chip('Contraparte · Distribuidora Caruba', None, 'Identificada')),
    note='Categorizado e identificado al llegar — no al cierre')

# ---------- Connect page: Inicio render (modeled on product/dashboard/prototypes/dashboard-v5.html, the frozen Inicio) ----------
# Marketing mock numbers (rate 567, never displayed): USD holdings 215.300 + 84.620 + 292.750,30 = 592.670,30
# Bs holdings 364.070.700 + 176.025.433,50 = 540.096.133,50 ≈ $952.550,50 → total $1.545.220,80 (= homepage hero)
# 30d decomp: Entró +84.200 − Salió 31.500 = flujos +52.700; Devaluación −18.400 → Δ +34.300; inicio $1.510.920,80
CONNECT_CSS = '''<style id="connect-render-v1">
.app-render { max-width: 1080px; margin: -8px auto 0; border: 1px solid var(--border-primary); border-radius: 14px; background: var(--bg-surface-1); box-shadow: 0 24px 48px -24px rgba(18,17,15,.18), 0 4px 12px rgba(18,17,15,.05); overflow: hidden; }
.app-render__bar { display: flex; align-items: center; gap: 6px; padding: 10px 16px; border-bottom: 1px solid var(--border-primary); background: var(--bg-surface-2); }
.app-render__dot { inline-size: 9px; block-size: 9px; border-radius: 50%; background: var(--border-primary); }
.app-render__url { margin-inline: auto; font-size: 12px; color: var(--text-tertiary); letter-spacing: .01em; }
.app-render__body { display: grid; grid-template-columns: 1.55fr 1fr; gap: 16px; padding: 20px; }
.app-render__body > * { min-inline-size: 0; }
.cr-box { border: 1px solid var(--border-primary); border-radius: 10px; background: #FFFFFF; padding: 18px 20px; }
.cr-label { font-size: 11px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--text-tertiary); margin-block-end: 6px; }
.cr-headrow { display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }
.cr-figure { font-size: 34px; font-weight: 600; letter-spacing: -0.02em; color: var(--text-primary); font-variant-numeric: tabular-nums; }
.cr-delta { font-size: 13px; font-weight: 600; color: var(--accent); }
.cr-chart { display: block; inline-size: 100%; block-size: auto; margin-block: 12px 4px; }
.cr-band { display: grid; grid-template-columns: repeat(4, 1fr); border-block: 1px solid var(--border-primary); margin-block: 10px 14px; }
.cr-band__cell { padding: 10px 12px; border-inline-start: 1px solid var(--border-primary); }
.cr-band__cell:first-child { border-inline-start: 0; padding-inline-start: 0; }
.cr-band__k { font-size: 11px; color: var(--text-tertiary); margin-block-end: 2px; }
.cr-band__v { font-size: 14px; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--text-primary); }
.cr-band__v.is-in { color: #24AD72; } .cr-band__v.is-out { color: var(--text-secondary); } .cr-band__v.is-net { color: var(--accent); }
.cr-monedas { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-block-end: 14px; }
.cr-moneda { border: 1px solid var(--border-primary); border-radius: 8px; padding: 10px 12px; }
.cr-moneda__k { font-size: 11px; color: var(--text-tertiary); } .cr-moneda__v { font-size: 15px; font-weight: 600; font-variant-numeric: tabular-nums; }
.cr-moneda__sub { font-size: 12px; color: var(--text-secondary); font-variant-numeric: tabular-nums; }
.cr-row { display: flex; align-items: center; gap: 10px; padding-block: 8px; border-block-start: 1px solid var(--border-primary); font-size: 13px; min-inline-size: 0; }
.cr-row__name { color: var(--text-primary); font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; min-inline-size: 0; } .cr-row__meta { color: var(--text-tertiary); font-size: 12px; white-space: nowrap; flex: none; }
.cr-row__vals { margin-inline-start: auto; display: flex; gap: 14px; font-variant-numeric: tabular-nums; color: var(--text-secondary); white-space: nowrap; flex: none; }
.cr-cf { display: flex; flex-direction: column; }
.cf-neto { font-size: 24px; font-weight: 600; letter-spacing: -0.01em; color: var(--accent); font-variant-numeric: tabular-nums; margin-block-end: 2px; }
.cf-neto__k { font-size: 12px; color: var(--text-secondary); margin-block-end: 12px; }
.cf-group { font-size: 10.5px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; color: var(--text-tertiary); margin-block: 10px 4px; }
.cf-row { display: flex; align-items: center; gap: 10px; padding-block: 5px; font-size: 13px; }
.cf-row__name { flex: none; inline-size: 132px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.cf-row__track { flex: 1; block-size: 6px; border-radius: 3px; background: var(--bg-surface-2); overflow: hidden; }
.cf-row__bar { display: block; block-size: 100%; border-radius: 3px; background: #24AD72; }
.cf-row--out .cf-row__bar { background: var(--tesote-gray-100, #E7E5E0); background: #B7B2A7; }
.cf-row__amt { flex: none; inline-size: 76px; text-align: end; font-variant-numeric: tabular-nums; color: var(--text-secondary); }
.cf-row--out .cf-row__amt { color: var(--text-secondary); } .cf-row__amt.is-in { color: #1B8A5A; }
.cr-minis { margin-block-start: auto; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; padding-block-start: 12px; }
.cr-mini { border: 1px solid var(--border-primary); border-radius: 8px; padding: 9px 12px; }
.cr-mini__k { font-size: 11px; color: var(--text-tertiary); } .cr-mini__v { font-size: 15px; font-weight: 600; font-variant-numeric: tabular-nums; color: var(--text-primary); }
.app-render__foot { padding: 0 20px 16px; }
.fmock-pills { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.fpill { display: inline-flex; align-items: center; gap: 6px; border: 1px solid var(--border-primary); border-radius: 8px; padding: 5px 10px; font-size: 12.5px; color: var(--text-primary); background: var(--bg-primary); }
.fpill b { font-weight: 600; } .fpill .fpill__x { color: var(--text-tertiary); font-size: 11px; }
.fpill--add { border-style: dashed; color: var(--text-secondary); }
.fpill--views { color: var(--text-secondary); }
@media (max-width: 991.98px) { .app-render__body { grid-template-columns: 1fr; } }
@media (max-width: 639.98px) { .cr-band { grid-template-columns: 1fr 1fr; } .cr-band__cell:nth-child(3) { border-inline-start: 0; padding-inline-start: 0; } .cr-monedas { grid-template-columns: 1fr; } }
/* split hero w/ flat right-edge bleed (gallery v1 option 4, Luis 2026-06-12) */
.phero--connect { overflow-x: clip; }
.phero--connect .phero__grid { grid-template-columns: 0.82fr 1.18fr; }
.chero-bleed { min-inline-size: 0; }
/* right edge tracks the viewport (container = 1200px → gutter = 50vw − 600px), constant 40px overhang at any width; capped so ultrawide just floats the box */
.chero-bleed .app-render { inline-size: calc(100% + 50vw - 600px + 40px); max-inline-size: 1080px; max-width: none; margin: 0; }
.chero-bleed .cr-figure { font-size: 30px; }
.chero-bleed .cf-row__name { inline-size: 110px; }
.chero-bleed .cf-row__amt { inline-size: 64px; font-size: 12px; }
.chero-bleed .cr-row__vals { font-size: 12px; gap: 8px; }
@media (max-width: 900px) { .chero-bleed .app-render { inline-size: 100%; } }
</style>'''

CONNECT_APP = '''<div class="app-render">
    <div class="app-render__bar"><span class="app-render__dot"></span><span class="app-render__dot"></span><span class="app-render__dot"></span><span class="app-render__url">app.tesote.com · Inicio</span></div>
    <div class="app-render__body">
      <div class="cr-box">
        <div class="cr-label">Posición total · USD consolidado · En vivo</div>
        <div class="cr-headrow"><span class="cr-figure">$1.545.220,80</span><span class="cr-delta"><i class="fa-solid fa-caret-up" aria-hidden="true"></i> +$34.300 · 30 días</span></div>
        <svg class="cr-chart" viewBox="0 0 640 130" fill="none" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="none">
          <defs><linearGradient id="cr-area" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#1661E2" stop-opacity="0.22"/><stop offset="100%" stop-color="#1661E2" stop-opacity="0"/></linearGradient></defs>
          <path d="M8 84 L72 78 L136 92 L200 64 L264 72 L328 46 L392 56 L456 30 L520 38 L632 18 L632 130 L8 130 Z" fill="url(#cr-area)"/>
          <path d="M8 84 L72 78 L136 92 L200 64 L264 72 L328 46 L392 56 L456 30 L520 38 L632 18" stroke="#1661E2" stroke-width="2.5" stroke-linejoin="round"/>
          <circle cx="8" cy="84" r="4.5" fill="#FFFFFF" stroke="#1661E2" stroke-width="2"/>
          <circle cx="632" cy="18" r="5" fill="#1661E2"/>
        </svg>
        <div class="cr-row__meta" style="margin-block-end:4px">Inicio del período · $1.510.920,80</div>
        <div class="cr-band">
          <div class="cr-band__cell"><div class="cr-band__k">Entró</div><div class="cr-band__v is-in">+$84.200</div></div>
          <div class="cr-band__cell"><div class="cr-band__k">Salió</div><div class="cr-band__v is-out">−$31.500</div></div>
          <div class="cr-band__cell"><div class="cr-band__k">Variación neta</div><div class="cr-band__v is-net">+$52.700</div></div>
          <div class="cr-band__cell"><div class="cr-band__k">Devaluación</div><div class="cr-band__v is-out">−$18.400</div></div>
        </div>
        <div class="cr-monedas">
          <div class="cr-moneda"><div class="cr-moneda__k">Dólares</div><div class="cr-moneda__v">$592.670,30</div></div>
          <div class="cr-moneda"><div class="cr-moneda__k">Bolívares</div><div class="cr-moneda__v">Bs. 540.096.133,50</div><div class="cr-moneda__sub">≈ $952.550,50</div></div>
        </div>
        <div class="cr-label">Por entidad</div>
        <div class="cr-row"><span class="cr-row__name">Tesote Tecnología, C.A.</span><span class="cr-row__meta">6 cuentas</span><span class="cr-row__vals"><span>$215.300,00</span><span>Bs. 364.070.700,00</span></span></div>
        <div class="cr-row"><span class="cr-row__name">Tesote IA, C.A.</span><span class="cr-row__meta">4 cuentas</span><span class="cr-row__vals"><span>$84.620,00</span><span>Bs. 176.025.433,50</span></span></div>
        <div class="cr-row"><span class="cr-row__name">Tesote Tech, Inc.</span><span class="cr-row__meta">2 cuentas · solo USD</span><span class="cr-row__vals"><span>$292.750,30</span></span></div>
      </div>
      <div class="cr-box cr-cf">
        <div class="cr-label">Flujo de caja por categoría · 30 días</div>
        <div class="cf-neto">+$52.700</div>
        <div class="cf-neto__k">entradas $84.200 · salidas $31.500</div>
        <div class="cf-group">Entradas</div>
        <div class="cf-row"><span class="cf-row__name">Cobros de clientes</span><span class="cf-row__track"><span class="cf-row__bar" style="inline-size:100%"></span></span><span class="cf-row__amt is-in">+$76.800</span></div>
        <div class="cf-row"><span class="cf-row__name">Otros ingresos</span><span class="cf-row__track"><span class="cf-row__bar" style="inline-size:10%"></span></span><span class="cf-row__amt is-in">+$7.400</span></div>
        <div class="cf-group">Salidas</div>
        <div class="cf-row cf-row--out"><span class="cf-row__name">Nómina</span><span class="cf-row__track"><span class="cf-row__bar" style="inline-size:18%"></span></span><span class="cf-row__amt">−$14.200</span></div>
        <div class="cf-row cf-row--out"><span class="cf-row__name">Proveedores</span><span class="cf-row__track"><span class="cf-row__bar" style="inline-size:13%"></span></span><span class="cf-row__amt">−$9.800</span></div>
        <div class="cf-row cf-row--out"><span class="cf-row__name">Impuestos</span><span class="cf-row__track"><span class="cf-row__bar" style="inline-size:6%"></span></span><span class="cf-row__amt">−$4.300</span></div>
        <div class="cf-row cf-row--out"><span class="cf-row__name">Servicios bancarios</span><span class="cf-row__track"><span class="cf-row__bar" style="inline-size:4%"></span></span><span class="cf-row__amt">−$3.200</span></div>
        <div class="cr-label" style="margin-block-start:16px">Top movimientos · 30 días</div>
        <div class="cr-row"><span class="cr-row__name">Distribuidora Caruba</span><span class="cr-row__meta">Cobro de clientes</span><span class="cr-row__vals"><span style="color:#1B8A5A">+$12.400</span></span></div>
        <div class="cr-row"><span class="cr-row__name">Nómina · quincena</span><span class="cr-row__meta">Nómina</span><span class="cr-row__vals"><span>−$7.100</span></span></div>
        <div class="cr-row"><span class="cr-row__name">Comercial Vethia</span><span class="cr-row__meta">Cobro de clientes</span><span class="cr-row__vals"><span style="color:#1B8A5A">+$8.900</span></span></div>
      </div>
    </div>
  </div>'''

# Connect chapter mocks — grounded in the Saldos v4 / Movimientos v7 specs
MOCK_SALDOS = panel(card('Saldos por moneda',
    chip('Dólares', '$592.670,30'),
    chip('Bolívares · Bs. 540.096.133,50', '≈ $952.550,50')),
    card('Cuenta Operativa · ··4210',
    chip('Estado', None, 'Conexión OK'),
    chip('Último sync', 'hace 2 min')),
    note='Tu posición real, sin pedírsela a nadie')

MOCK_FILTROS = panel(card('Filtra como piensas',
    '<div class="fmock-pills">'
    + '<span class="fpill"><b>Fecha</b> · Este mes <span class="fpill__x">✕</span></span>'
    + '<span class="fpill"><b>Categoría</b> · Nómina <span class="fpill__x">✕</span></span>'
    + '<span class="fpill"><b>Cuenta</b> · Operativa y 1 más <span class="fpill__x">✕</span></span>'
    + '<span class="fpill fpill--add">+ Filtrar</span>'
    + '<span class="fpill fpill--views"><i class="fa-regular fa-bookmark" aria-hidden="true"></i> Vistas (3)</span>'
    + '</div>'),
    card(None, chip('23 movimientos · Bs. 86.480.000,00', None, 'En vivo', accent=True)),
    note='Los totales se recalculan con cada filtro')

MOCK_EQUIPO = panel(card('Transferencia · $4.520,00',
    chip('Nota de Tesorería · "Anticipo de Distribuidora Caruba — confirmado con ventas."', None, None),
    chip('Compartido con Contabilidad', None, 'Link')),
    card('Permisos por rol',
    chip('Tesorería', None, 'Ve y aprueba'),
    chip('Contabilidad', None, 'Concilia'),
    chip('Gerencia', None, 'Solo lectura', accent=True)),
    note='El contexto queda donde ocurrió — no en un chat aparte')

# entity USD-equivalents mirror the homepage hero (Bs at 567, rate never shown): 857.400 + 395.070,50 + 292.750,30 = 1.545.220,80
MOCK_MULTI = panel(card('Tres entidades, todos los bancos',
    chip('Tesote Tecnología, C.A. · 6 cuentas', '$857.400,00', dot=True),
    chip('Tesote IA, C.A. · 4 cuentas', '$395.070,50', dot=True),
    chip('Tesote Tech, Inc. · 2 cuentas · solo USD', '$292.750,30', dot=True)),
    card(None, chip('Posición consolidada · USD', '$1.545.220,80', 'En vivo', accent=True)),
    note='Cada entidad cuadra — y el total también')

MOCK_REVISION = panel(card('Conciliado solo · hoy',
    chip('Movimientos cruzados contra tu ERP', None, 'Automático'),
    chip('Monto · fecha · referencia · contraparte', None, 'Match')),
    card('Lo que queda, lo decides tú',
    chip('Transferencia Bs. 8.120.000,00 · ¿Factura #1027?', None, 'Confirmar', accent=True)),
    note='Tu equipo decide excepciones — no transcribe planillas')

MOCK_PERMS = panel(card('Permisos por rol',
    chip('Tesorería', None, 'Ve y aprueba'),
    chip('Contabilidad', None, 'Concilia'),
    chip('Gerencia', None, 'Solo lectura', accent=True)),
    card('Auditoría', chip('Cada acción registrada: quién, qué y cuándo', None, 'Completa')),
    note='Cada quien ve exactamente lo que le toca')

MOCK_VALIDACION = panel(card('Antes de salir un bolívar',
    '<div class="chapter-steps">' + step('Cruzado contra facturas abiertas') + step('Retenciones calculadas y verificadas') + step('Doble aprobación configurable') + '</div>'),
    note='El error se detiene antes del pago, no después')

MOCK_API = panel(card('Orden #88 · aprobada y liberada',
    '<div class="chapter-steps">' + step('Aprobada por finanzas') + step('Liberada al banco por API') + step('Ejecutando…', 'working') + step('Confirmación bancaria', 'pending') + '</div>'),
    note='Por la API oficial del banco, con su grado de seguridad')

MOCK_AP_INTAKE = panel(card('Factura del proveedor · #4471',
    chip('Monto', '$12.400,00'),
    chip('Retención de impuestos', '−$372,00'),
    chip('En Tesote', None, 'Creada'),
    chip('En tu ERP', None, 'Creada', accent=True)),
    note='De la factura al pago, sin transcribir')

MOCK_ERP_INSTANT = panel(card('Al ejecutarse',
    chip('Pago a proveedor · #88', '$48.250,00', 'Conciliado'),
    chip('Asiento contable', None, 'Registrado', accent=True)),
    note='Tu ERP se entera solo, en el momento')

MOCK_LINK_FACTURA = panel(card('Link de cobro · Factura #2210',
    chip('Factura adentro · Bs. 312.500,00', None, 'Adjunta'),
    chip('Enviado por WhatsApp', None, 'Abierto')),
    note='Tu cliente paga en un clic, sin registrarse')

MOCK_METODOS = panel(card('Tu cliente elige',
    chip('Pago móvil', None, 'Disponible'),
    chip('Transferencia', None, 'Disponible'),
    chip('Tarjeta', None, 'Disponible')),
    note='Cada pago entra identificado con su factura')

MOCK_CERO_CONC = panel(card('Pago recibido',
    chip('Bs. 312.500,00 · Distribuidora Caruba', None, 'Identificado'),
    MATCH_SVG,
    chip('Factura #2210', None, 'Conciliada')),
    note='No hay nada que cruzar a fin de mes')

MOCK_DOS_DIRECCIONES = panel(card('Sube a tu ERP',
    chip('Movimientos enriquecidos', None, 'Categorías + contrapartes')),
    card('Baja de tu ERP', chip('Facturas abiertas', None, 'Para el match')),
    note='Una sola fuente de verdad, sin copiar y pegar')

MOCK_ACCIONES_ERP = panel(card('Acciones en tu ERP',
    chip('Proveedor nuevo', None, 'Creado'),
    chip('Factura #1031 · monto corregido', None, 'Actualizada'),
    chip('Pago #87', None, 'Conciliado')),
    note='Tesote no solo lee tu ERP — también escribe')

MOCK_CHAT = panel(
    '<div class="pcard__bubble pcard__bubble--user">¿Cuánto cobramos esta semana?</div>',
    '<div class="pcard__bubble pcard__bubble--ai">Cobraste <span class="pcard__chip-value">$48.230</span> en 312 transacciones, 12% más que la semana pasada.</div>',
    '<div class="pcard__bubble pcard__bubble--user">¿Quién nos debe más de 30 días?</div>',
    '<div class="pcard__bubble pcard__bubble--ai">3 clientes: Comercial Vethia ($12.400), Academia Norvel ($7.450) y uno nuevo por revisar.</div>',
    note='Respuestas con tus datos reales, al día')

MOCK_AGENTES = panel(card('Tesote AI · Trabajando',
    '<div class="hero-panel__feed">'
    + '<div class="hero-panel__feed-item"><i class="fa-solid fa-shield-halved is-guard" aria-hidden="true"></i><span class="hero-panel__feed-text">Factura duplicada <b>detenida antes del pago</b> · $7.490</span><span class="hero-panel__feed-time">hace 1 h</span></div>'
    + '<div class="hero-panel__feed-item"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span class="hero-panel__feed-text"><b>14 facturas vencidas cobradas</b> · $96.400 recuperados</span><span class="hero-panel__feed-time">este mes</span></div>'
    + '<div class="hero-panel__feed-item"><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span class="hero-panel__feed-text"><b>142 partidas</b> enviadas al ERP · cero diferencias</span><span class="hero-panel__feed-time">hoy</span></div>'
    + '<div class="hero-panel__feed-item"><i class="fa-solid fa-circle-notch fa-spin is-working" aria-hidden="true"></i><span class="hero-panel__feed-text">Armando el <b>cierre del mes</b> · va 87%…</span><span class="hero-panel__feed-time">ahora</span></div>'
    + '</div>'),
    note='Trabajan de fondo; tú apruebas lo que importa')

MOCK_REPORTES = panel(card('Resumen semanal',
    chip('Se corre cada lunes · 7:00 am', None, 'Programado', accent=True),
    chip('Llega listo, conciliado y explicado', None, 'Automático')),
    '<div class="ai-actions"><span class="ai-action"><i class="fa-solid fa-bookmark" aria-hidden="true"></i>Guardar como mi reporte</span><span class="ai-action"><i class="fa-solid fa-arrows-rotate" aria-hidden="true"></i>Correr cada lunes</span></div>',
    note='Defínelo una vez; recíbelo siempre')

ARROW_DOWN = '<div class="mock-arrow"><i class="fa-solid fa-arrow-down" aria-hidden="true"></i></div>'
ARROW_UP   = '<div class="mock-arrow"><i class="fa-solid fa-arrow-up" aria-hidden="true"></i></div>'

PANEL_INTEGRACION = panel(
    card('Banco → Tesote → ERP',
        chip('120+ bancos', None, 'En vivo'),
        ARROW_DOWN,
        chip('Tesote · categoriza, identifica, concilia', None, 'Automático'),
        ARROW_DOWN,
        chip('Tu ERP · asientos y partidas listos', None, 'Registrado')),
    card('Y de vuelta', chip('Facturas abiertas de tu ERP', None, 'Bajan para el match', accent=True)),
    note='Bidireccional — tu ERP sigue siendo la fuente contable')

MOCK_ERPS = panel(card('Funciona con',
    '<div class="ui-card__pills">'
    + '<span class="pcard__chip" style="flex:none">Odoo</span>'
    + '<span class="pcard__chip" style="flex:none">Profit Plus</span>'
    + '<span class="pcard__chip" style="flex:none">SAP</span>'
    + '<span class="pcard__chip" style="flex:none">+ el tuyo</span>'
    + '</div>'),
    card(None, chip('¿Otro sistema?', None, 'Lo conectamos en la implementación')),
    note='La integración la hace nuestro equipo, no el tuyo')

SEC_GRID = '''<div class="sec-grid">
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-lock"></i></div>
    <h3 class="sec-card__title">Cifrado de grado bancario</h3>
    <p class="sec-card__body">AES-256-GCM en reposo, TLS en tránsito e integridad verificada con SHA-256. Tu información se cifra y se protege con los estándares más altos de la industria.</p>
  </div>
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-user-shield"></i></div>
    <h3 class="sec-card__title">Tú controlas quién ve y hace qué</h3>
    <p class="sec-card__body">Permisos granulares por banco, cuenta y módulo; 2FA en cada acceso; y una auditoría completa que registra quién vio o movió qué, y cuándo.</p>
  </div>
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-certificate"></i></div>
    <h3 class="sec-card__title">Probado, no solo prometido</h3>
    <p class="sec-card__body">Pruebas de penetración recurrentes y trabajo bajo SOC 2 Type II (en curso), el estándar de controles más exigente de la industria.</p>
  </div>
</div>'''

FAQ_SEG = '''<div class="faq__list">
  <details class="faq__item">
    <summary class="faq__q">¿Qué tan segura está mi información?<i class="fa-solid fa-chevron-down faq__chevron" aria-hidden="true"></i></summary>
    <p class="faq__a">Cifrado de grado bancario (AES-256-GCM, TLS, integridad SHA-256), 2FA en cada acceso, permisos granulares y auditoría completa de cada acción. Estamos en proceso de certificación SOC 2 Type II.</p>
  </details>
  <details class="faq__item">
    <summary class="faq__q">¿Tesote tiene acceso a mi dinero?<i class="fa-solid fa-chevron-down faq__chevron" aria-hidden="true"></i></summary>
    <p class="faq__a">No. Tesote no custodia tus fondos. Los pagos se ejecutan por la API de tu propio banco y cada acción la autorizas tú — Tesote ve y organiza, tú decides y apruebas.</p>
  </details>
</div>'''

# ---------- testimonial cards (REAL quotes only — never invent) ----------
def testi(quote, logo, alt, name, role):
    stars = '<i class="fa-solid fa-star" aria-hidden="true"></i>' * 5
    return ('<figure class="testi-card"><blockquote class="testi-card__quote">“%s”</blockquote>'
            '<div class="testi-card__stars" aria-label="5 de 5 estrellas">%s</div>'
            '<figcaption class="testi-card__cite"><img class="testi-card__logo" src="current/assets/clients/%s" alt="%s" loading="lazy">'
            '<span class="testi-card__person"><span class="testi-card__name">%s</span><span class="testi-card__role">%s</span></span>'
            '</figcaption></figure>') % (quote, stars, logo, alt, name, role)

T_AMA = testi('Nuestra tesorería ha experimentado una transformación gracias a Tesote. Tenemos la información bancaria consolidada al instante, facilitando nuestros reportes y destinando más tiempo del equipo al análisis y toma de decisiones importantes.',
              'ama-de-casa-f367519b.webp', 'Grupo Ama de Casa', 'Carlos Domínguez', 'VP Ejecutivo · Grupo Ama de Casa')
T_CINES = testi('Tesote ha potenciado nuestra tesorería con acceso inmediato a saldos bancarios, unificando todas las transacciones de todos los bancos en un solo lugar con filtros avanzados, gráficos que muestran ingresos, débitos por cuenta y banco al alcance de un clic.',
                'cines-unidos-88a1fcbc.webp', 'Cines Unidos', 'José Daniel López', 'Jefe de Tesorería · Cines Unidos')
T_PAISA = testi('Tesote nos ha permitido disminuir significativamente los tiempos de consultas bancarias y agilizar las confirmaciones de pagos de clientes, generando así un impacto positivo en nuestros procesos administrativos de ventas y flujo de caja.',
                'paisa-8727515c.webp', 'Paisa', 'Jorge Guerra', 'Gerente de Finanzas · Paisa')

def testi_band(card_html):
    return (TESTI_CSS + '<section class="chapter"><div class="container">'
            '<div class="testi-grid testi-grid--one">' + card_html + '</div></div></section>')

# ---------- section builders ----------
def chapter_sec(title, body, bullets, panel_html, flip=False, dark=False, link=None, linktext=None, eyebrow=None):
    cls = 'chapter' + (' chapter--flip' if flip else '') + (' chapter--dark' if dark else '')
    eb = '<span class="chapter__eyebrow">%s</span>' % eyebrow if eyebrow else ''
    bl = ''
    if bullets:
        bl = '<ul class="chapter__list">' + ''.join(
            '<li><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>%s</span></li>' % b for b in bullets) + '</ul>'
    lk = ''
    if link:
        lk = '<a class="chapter__link" href="%s">%s <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>' % (link, linktext)
    return ('<section class="%s"><div class="container"><div class="chapter__row">'
            '<div class="chapter__copy">%s<h2 class="chapter__title">%s</h2><p class="chapter__body">%s</p>%s%s</div>'
            '%s</div></div></section>') % (cls, eb, title, body, bl, lk, panel_html)

def center_head(title, body=None, eyebrow=None):
    eb = '<span class="chapter__eyebrow">%s</span>' % eyebrow if eyebrow else ''
    bd = '<p class="chapter__body">%s</p>' % body if body else ''
    return '<header class="chapter__header-center">%s<h2 class="chapter__title">%s</h2>%s</header>' % (eb, title, bd)

def phero(eyebrow, title, sub, mock=None, dark=False, lines=True, center=False):
    cls = 'phero' + (' phero--dark' if dark else '') + (' phero--center' if center else '')
    cta = ('<a href="%s" class="btn btn-primary">Agenda una demo <i class="fa-solid fa-arrow-right ms-2" aria-hidden="true"></i></a>' % DEMO)
    copy = ('<div><span class="phero__eyebrow">%s</span><h1 class="phero__title">%s</h1><p class="phero__sub">%s</p>%s</div>'
            % (eyebrow, title, sub, cta))
    inner = ('<div class="phero__grid">%s%s</div>' % (copy, mock)) if mock else copy
    return '<section class="%s"><div class="container">%s</div></section>' % (cls, inner)

def prod_fit(items, title='Lo que usarías de Tesote'):
    cards = ''.join(
        ('<a class="pcard" href="%s"><div class="pcard__head"><h3 class="pcard__title">%s</h3>'
         '<p class="pcard__body">%s</p></div>'
         '<div class="pcard__visual" aria-hidden="true"><span class="chapter__link">Conocer <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span></div></a>')
        % (href, t, d) for (href, t, d) in items)
    return ('<section class="section"><div class="container">' + center_head(title)
            + '<div class="pcard-grid pcard-grid--fit">' + cards + '</div></div></section>')

def pains_sec(title, pains, body=None):
    items = ''.join('<li><i class="fa-solid fa-circle-check" aria-hidden="true"></i><span>%s</span></li>' % p for p in pains)
    return ('<section class="section section--head-only"><div class="container">' + center_head(title, body)
            + '<ul class="chapter__list" style="max-width:54ch;margin-inline:auto">' + items + '</ul></div></section>')

def logo_row(files, heading=None, small=True):
    h = '<h2 class="logo-strip__heading">%s</h2>' % heading if heading else ''
    imgs = ''.join('<img src="current/assets/clients/%s" alt="Logo de %s" loading="lazy">' % (f, a) for (f, a) in files)
    return ('<section class="section section--tight"><div class="container">' + h
            + '<div class="logo-wall%s">' % (' logo-wall--sm' if small else '') + imgs + '</div></div></section>')

# ---------- Conciliación page: "Motor de reglas" hero render (gallery v2 option 1, Luis 2026-06-20) ----------
# Mechanism-forward hero: the rule list (condición DSL -> categoría + contraparte + % cobertura).
# Render contained (not bled) so the coverage column stays fully visible.
CONCILIA_CSS = '''<style id="concilia-rules-v1">
.phero--rules { overflow-x: clip; }
.phero--rules .phero__grid { grid-template-columns: 0.9fr 1.1fr; align-items: center; }
@media (max-width: 900px) { .phero--rules .phero__grid { grid-template-columns: 1fr; } }
.chero-rules { min-inline-size: 0; }
.app-render { width: 100%; max-width: none; margin: 0; border: 1px solid #E7E5E0; border-radius: 14px; background: #FCFBF7; box-shadow: 0 24px 48px -24px rgba(18,17,15,.18), 0 4px 12px rgba(18,17,15,.05); overflow: hidden; }
.app-render__bar { display: flex; align-items: center; gap: 6px; padding: 10px 16px; border-bottom: 1px solid #E7E5E0; background: #F7F5F0; }
.app-render__dot { inline-size: 9px; block-size: 9px; border-radius: 50%; background: #DCD6CB; }
.app-render__url { margin-inline: auto; font-size: 12px; color: #857D73; letter-spacing: .01em; }
.app-render__body { padding: 20px; }
.rc-box { background:#fff; border:1px solid #E7E5E0; border-radius:12px; padding:16px; }
.rc-head { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:12px; }
.rc-head__title { font-size:13px; font-weight:600; color:#12110F; }
.rc-head__meta { font-size:11.5px; color:#6B675E; }
.rv-rules { display:flex; flex-direction:column; gap:8px; }
.rv-rule { display:grid; grid-template-columns:1fr auto; gap:6px 12px; align-items:center; padding:11px 13px; border:1px solid #EEECE6; border-radius:10px; background:#fff; }
.rv-rule__map { display:flex; align-items:center; gap:9px; min-width:0; flex-wrap:wrap; }
.rv-code { font-family:var(--font-mono, ui-monospace, monospace); font-size:11.5px; color:#3A3833; background:#F4F2EC; border:1px solid #E7E4DC; border-radius:6px; padding:3px 7px; white-space:nowrap; }
.rv-code b { color:#12110F; font-weight:600; }
.rv-to { color:#9A958B; font-size:11px; flex:none; }
.rv-act { display:inline-flex; flex-direction:column; gap:1px; min-width:0; }
.rv-act__cat { font-size:12.5px; font-weight:600; color:#12110F; white-space:nowrap; }
.rv-act__cp { font-size:11px; color:#6B675E; white-space:nowrap; }
.rv-cov { justify-self:end; font-size:11px; color:#0E7A56; font-weight:600; font-variant-numeric:tabular-nums; white-space:nowrap; }
.rv-rules__foot { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-top:12px; font-size:11.5px; color:#6B675E; }
.rv-rules__foot a { color:#1A56C4; text-decoration:none; font-weight:600; }
</style>'''

def _crule(cond, cat, cp, cov):
    cp_html = '<span class="rv-act__cp">%s</span>' % cp if cp else ''
    return ('<div class="rv-rule"><div class="rv-rule__map"><span class="rv-code">%s</span>'
            '<span class="rv-to"><i class="fa-solid fa-arrow-right" aria-hidden="true"></i></span>'
            '<span class="rv-act"><span class="rv-act__cat">%s</span>%s</span></div>'
            '<span class="rv-cov">%s</span></div>') % (cond, cat, cp_html, cov)

CONCILIA_APP = ('<div class="chero-rules" aria-hidden="true"><div class="app-render">'
    '<div class="app-render__bar"><span class="app-render__dot"></span><span class="app-render__dot"></span><span class="app-render__dot"></span>'
    '<span class="app-render__url">app.tesote.com · Conciliación · Reglas</span></div>'
    '<div class="app-render__body"><div class="rc-box">'
    '<div class="rc-head"><span class="rc-head__title">Reglas de conciliación</span><span class="rc-head__meta">47 activas · 71% de cobertura</span></div>'
    '<div class="rv-rules">'
    + _crule('descripción contiene <b>"CARUBA"</b>', 'Ingresos › Clientes', 'Distribuidora Caruba', '99%')
    + _crule('descripción empieza con <b>"PAGO VETHIA"</b>', 'Proveedores › Mercancía', 'Comercial Vethia', '98%')
    + _crule('descripción contiene <b>"NOMINA"</b>', 'Personal › Nómina', '—', '100%')
    + _crule('descripción contiene <b>"COMISION"</b> y tipo = <b>egreso</b>', 'Servicios bancarios', '—', '97%')
    + _crule('descripción contiene <b>"POS COMPRA"</b>', 'Gastos › Compras', '—', '94%')
    + '</div>'
    '<div class="rv-rules__foot"><span>8 reglas listas para promover a automático</span>'
    '<a href="#">Revisar <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a></div>'
    '</div></div></div></div>')

# ---------- page assembly ----------
STYLE_BUNDLE = CHAPTERS + PCARD + HERO15 + FAQ_CSS

def render_page(fname, title, desc, body_html):
    html = (
        '<!DOCTYPE html>\n<html lang="es" data-theme="light">\n<head>\n'
        '<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<title>' + title + '</title>\n<meta name="description" content="' + desc + '">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<link rel="icon" type="image/svg+xml" href="/icon.svg">\n<meta name="theme-color" content="#FCFBF7">\n'
        '<link rel="preload" href="current/assets/inter/inter-latin-0555e090.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="preload" href="current/assets/aspekta/AspektaVF-36354009.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<link rel="stylesheet" href="current/assets/fontawesome/css/all.min-8e150040.css">\n'
        '<link rel="stylesheet" href="current/assets/admin-1f3f92b5.css">\n'
        '<link rel="stylesheet" href="current/assets/application-23a5d970.css">\n'
        + LIGHT + '\n' + MEGA_CSS + '\n' + PAGE_CSS + '\n' + CTA_DARK + '\n'
        '</head>\n<body>\n' + NAV_PAGES + '\n<main>\n' + STYLE_BUNDLE + '\n'
        + body_html + '\n' + CTA_BAND_PAGES + '\n</main>\n' + FOOTER_PAGES + '\n' + FAB + '\n' + DENSITY + '\n'
        '</body>\n</html>\n')
    open(fname, 'w').write(html)
    return fname

written = []

# ===== PRODUCT PAGES =====
written.append(render_page('page-connect.html',
    'Connect — Saldos y movimientos en tiempo real | Tesote',
    'Saldos y movimientos de más de 120 bancos — Venezuela, Panamá, RD y EE. UU. — consolidados en Bs y USD, en tiempo real.',
    CONNECT_CSS
    + phero('Producto · Connect',
          'Saldos y movimientos de todos tus bancos, en tiempo real.',
          'Más de 120 bancos — Venezuela, Panamá, RD y EE.&nbsp;UU. — consolidados en Bs y USD, sin que nadie arme un reporte.',
          '<div class="chero-bleed" aria-hidden="true">' + CONNECT_APP + '</div>').replace('<section class="phero">', '<section class="phero phero--connect">', 1)
    + chapter_sec('Tu posición de caja, cuando quieras verla.',
        'Entras y está ahí: todas tus cuentas, de todos tus bancos y entidades, consolidadas a USD. No se lo pides a nadie y nadie lo arma a mano — tu posición de caja, en el momento en que la quieres ver.',
        ['Tu total consolidado, o el desglose por entidad, banco o moneda.',
         'Es lo que dicen tus bancos, no un Excel que ya venía viejo.',
         'Disponible cuando entras — tu equipo no para a armarlo.'],
        MOCK_SALDOS, flip=True)
    + chapter_sec('Cualquier pregunta, respondida al instante.',
        'Cuando surge la duda — "¿qué fue ese pago?", "¿cuánto le pagamos a este proveedor?" — la respuesta está en segundos, no en un correo a tu equipo. Todos los movimientos de todos tus bancos en una sola tabla, con los totales recalculándose en vivo.',
        ['Busca en todo: descripción, referencia, contraparte, nota.',
         'Filtros que se combinan: fecha, cuenta, categoría, contraparte, monto.',
         'Vistas guardadas: el filtro que tu equipo usa cada lunes, a un clic.'],
        MOCK_FILTROS)
    + chapter_sec('Cada movimiento llega trabajado.',
        'No es un espejo del banco: cada transacción entra categorizada, con su contraparte identificada y lista para usarse.',
        ['Categorización automática desde el primer día.',
         'Contrapartes identificadas: sabes quién te pagó y a quién pagaste.',
         'Insights por transacción: similares, comparaciones, historia.'],
        MOCK_TX, flip=True)
    + chapter_sec('Hecho para que trabaje todo el equipo.',
        'Connect no es una consulta de saldos: es donde finanzas trabaja — con notas, contexto compartido y permisos por rol.',
        ['Notas en cada movimiento — el contexto queda donde ocurrió.',
         'Comparte un movimiento con quien lo necesita.',
         'Permisos por rol y auditoría completa de cada acción.'],
        MOCK_EQUIPO)
    + STATS
    + testi_band(T_CINES)))

written.append(render_page('page-pagos.html',
    'Pagos — Cuentas por pagar, de la factura al banco | Tesote',
    'Cuentas por pagar de punta a punta: la factura entra a Tesote y a tu ERP, apruebas y programas el pago —individual o en lote— y se ejecuta por la API oficial de tu banco.',
    phero('Producto · Pagos',
          'Aprueba y paga desde un solo lugar — y se concilia solo.',
          'Tus cuentas por pagar, de punta a punta: la factura de tu proveedor entra a Tesote y a tu ERP, tú la apruebas y programas el pago —individual o en lote— y se ejecuta por la API oficial de tu banco, con su mismo grado de seguridad.',
          PANEL_PAGOS)
    + chapter_sec('El pago empieza en la factura, no en un formulario.',
        'La factura de tu proveedor entra a Tesote y se crea en tu ERP, con su monto, sus retenciones y su contraparte ya identificados. El pago nace listo para aprobarse — nadie lo transcribe a mano.',
        ['Captura la factura del proveedor y créala en Tesote y en tu ERP.',
         'Monto, impuestos y retenciones calculados desde el documento.',
         'Contraparte y cuenta destino identificadas automáticamente.'],
        MOCK_AP_INTAKE, flip=True)
    + chapter_sec('Tú apruebas y programas. Un pago o quinientos.',
        'Programa un pago individual o arma un lote de cientos de proveedores. Todo pasa por el flujo de aprobación que tú defines —por monto y por rol— antes de que se libere un solo bolívar.',
        ['Pagos individuales o lotes de cientos de proveedores.',
         'Flujo de aprobación por monto y rol, con doble control.',
         'Cada pago validado contra su factura y retención antes de aprobar.'],
        MOCK_VALIDACION)
    + chapter_sec('Con el grado de seguridad de tu banco, no a pesar de él.',
        'Los bancos exigen aprobación y liberación por una razón. Tesote no reemplaza esos controles: cada pago aprobado se ejecuta por la API oficial de tu banco, con su mismo grado de seguridad y el mismo proceso de aprobación y liberación. Es el patrón que las grandes empresas ya automatizan entre su ERP y el banco — Tesote lo hace integrado, sin archivos ni pasos manuales.',
        ['API oficial del banco: canal cifrado y autorizado por la entidad.',
         'El proceso de aprobación y liberación del banco, respetado de punta a punta.',
         'Sin claves ni tokens compartidos entre el equipo.',
         'Auditoría completa: quién aprobó, quién liberó y cuándo.'],
        MOCK_API, flip=True)
    + chapter_sec('El cierre no acumula trabajo.',
        'Cada pago queda conciliado y registrado en el momento en que se ejecuta — llegas a fin de mes sin una pila de pagos por identificar.',
        ['Asiento contable registrado automáticamente.',
         'Cada pago amarrado a su factura y contraparte.',
         'Cero pagos "por identificar" a fin de mes.'],
        MOCK_ERP_INSTANT)
    + testi_band(T_AMA)))

written.append(render_page('page-cobros.html',
    'Cobros — Te pagan más rápido y entra conciliado | Tesote',
    'Cobra con un link de pago con la factura adentro: tu cliente paga en un clic y el pago entra identificado y conciliado.',
    phero('Producto · Cobros',
          'Cobra con un link: te pagan más rápido y entra conciliado.',
          'Tu cliente paga en un clic y el dinero entra ya identificado con su factura — cobras más rápido y no queda nada que conciliar.',
          PANEL_COBROS)
    + chapter_sec('Te pagan más rápido, sin perseguir a nadie.',
        'En vez de mandar un número de cuenta y esperar, mandas un link con el monto y la factura ya adentro — tu cliente paga en el momento, no cuando encuentra los datos.',
        ['Compártelo por WhatsApp, correo o dentro de tu factura.',
         'Tu cliente no se registra ni descarga nada.',
         'Cada link sabe exactamente qué factura está cobrando.'],
        MOCK_LINK_FACTURA, flip=True)
    + chapter_sec('Mientras más fácil le sea pagar, más rápido cobras.',
        'Pago móvil, transferencia o tarjeta — tu cliente elige, el dinero llega a tu cuenta y Tesote sabe de quién es y de qué factura.',
        ['Pago móvil, transferencia o tarjeta.',
         'Confirmación al instante para ti y para tu cliente.',
         'Funciona para cobro puntual o recurrente.'],
        MOCK_METODOS)
    + chapter_sec('Y no hay nada que conciliar.',
        'El pago entra identificado con su factura y su contraparte — la conciliación ya ocurrió cuando te avisó que te pagaron.',
        ['Cada pago amarrado a su factura desde el origen.',
         'Registrado en tu ERP automáticamente.',
         'Cero "transferencias por identificar" a fin de mes.'],
        MOCK_CERO_CONC, flip=True)
    + testi_band(T_PAISA)))

written.append(render_page('page-conciliacion.html',
    'Conciliación automática — Banco y ERP cuadrados solos | Tesote',
    'Tesote cruza tus bancos contra tu ERP en ambas direcciones: sube data enriquecida, baja facturas y devuelve partidas conciliadas.',
    CONCILIA_CSS
    + phero('Producto · Conciliación automática',
          'Llega al cierre con la conciliación ya hecha.',
          'Cada movimiento llega al cierre ya cuadrado contra tu ERP — el cierre deja de ser un proyecto de fin de mes y pasa a estar siempre listo.',
          CONCILIA_APP).replace('<section class="phero">', '<section class="phero phero--rules">', 1)
    + chapter_sec('Lo que cuadra, cuadra solo. Lo demás lo decides tú.',
        'Cada movimiento bancario se cruza contra tus facturas abiertas y queda conciliado sin que nadie toque una planilla.',
        ['90% de categorización automática.',
         'Match por monto, fecha, referencia y contraparte.',
         'Lo que no cuadra solo, te lo presenta para decidir en un clic.'],
        MOCK_REVISION, flip=True)
    + chapter_sec('Tu ERP, siempre al día.',
        'Tesote no solo lee tu ERP — también escribe: crea proveedores, corrige facturas y registra partidas conciliadas.',
        ['Sube tu data bancaria ya enriquecida: categorías, contrapartes, tasas.',
         'Baja tus facturas abiertas para el match.',
         'Devuelve asientos y partidas conciliadas, registradas.'],
        MOCK_ACCIONES_ERP)
    + STATS))

# ===== PLATFORM PAGES =====
written.append(render_page('page-tesote-ai.html',
    'Tesote AI — Agentes para las finanzas de tu empresa | Tesote',
    'La IA más avanzada aplicada a tus finanzas — con tus bancos, tus pagos y tu ERP ya conectados. Pregunta, automatiza y recibe reportes solos.',
    phero('Plataforma · Tesote AI',
          'Todo conectado. Ahora, inteligente.',
          'La IA más avanzada, aplicada a las finanzas de tu empresa — con tus bancos, tus pagos y tu ERP ya conectados.',
          '<div class="chapter--dark" style="background:transparent">' + PANEL_AI_DIGEST + '</div>',
          dark=True, lines=False)
    + chapter_sec('Pregúntale a tus finanzas.',
        'Respuestas con tus datos reales y al día — no con un PDF de hace tres semanas.',
        ['Saldos, cobros, pagos y tendencias en lenguaje natural.',
         'Para todo el equipo de finanzas, no solo tesorería.',
         'Cada respuesta sale de tus bancos y tu ERP conectados.'],
        MOCK_CHAT, flip=True)
    + chapter_sec('Agentes que hacen el trabajo.',
        'No es un chat que opina: son agentes que concilian, categorizan, detienen errores y persiguen facturas — de fondo, todos los días.',
        ['Detiene pagos duplicados antes de que salgan.',
         'Persigue facturas vencidas y registra lo cobrado.',
         'Arma el cierre del mes mientras tu equipo hace otra cosa.'],
        MOCK_AGENTES)
    + chapter_sec('Reportes que se corren solos.',
        'Define el reporte una vez — la IA lo corre cada semana, conciliado y explicado, sin que nadie lo arme.',
        ['Resumen semanal con el porqué detrás de cada número.',
         'Programable: cada lunes, cada cierre, cuando quieras.',
         'Listo para reenviar a gerencia o al directorio.'],
        MOCK_REPORTES, flip=True)))

written.append(render_page('page-integraciones.html',
    'Integraciones — Tu ERP, en ambas direcciones | Tesote',
    'Tesote se integra con tu ERP en ambas direcciones: sube data bancaria enriquecida y devuelve partidas conciliadas y registradas.',
    phero('Plataforma · Integraciones',
          'Tesote habla con tu ERP. En ambas direcciones.',
          'Tu ERP sigue siendo la fuente contable — Tesote le entrega la data bancaria trabajada y le devuelve la conciliación lista.',
          PANEL_INTEGRACION)
    + chapter_sec('Sube data enriquecida, no data cruda.',
        'Lo que llega a tu ERP ya viene categorizado, con contrapartes identificadas y tasas aplicadas.',
        ['Categorías y contrapartes resueltas antes de llegar al ERP.',
         'Tasas y monedas aplicadas con criterio consistente.',
         'Tu contador recibe trabajo terminado, no trabajo por hacer.'],
        MOCK_DOS_DIRECCIONES, flip=True)
    + chapter_sec('Funciona con tu sistema.',
        'Trabajamos con los ERP más usados de la región — y si el tuyo es distinto, lo conectamos durante la implementación.',
        ['Integración configurada por nuestro equipo, llave en mano.',
         'Sin migraciones: tu ERP se queda donde está.',
         'El match y las escrituras respetan tu plan de cuentas.'],
        MOCK_ERPS)))

written.append(render_page('page-seguridad.html',
    'Seguridad — Tu data operativa, protegida | Tesote',
    'Cifrado de grado bancario, permisos granulares, 2FA, auditoría completa y trabajo bajo SOC 2 Type II.',
    phero('Plataforma · Seguridad',
          'Tu data operativa, tratada como lo que es.',
          'La seguridad no es una sección de esta página — es la condición para que todo lo demás exista.',
          None, center=True)
    + '<section class="section"><div class="container">' + SEC_GRID + '</div></section>'
    + chapter_sec('Tú decides quién ve y hace qué.',
        'Permisos granulares por banco, cuenta y módulo — y una auditoría que registra cada acción.',
        ['Roles y permisos por banco, cuenta y módulo.',
         '2FA en cada acceso.',
         'Auditoría completa: quién vio o movió qué, y cuándo.'],
        MOCK_PERMS, flip=True)
    + '<section class="section faq"><div class="container"><header class="faq__header"><h2 class="section__title">Preguntas frecuentes</h2></header>' + FAQ_SEG + '</div></section>'))

# ===== SOLUTIONS: SIZE =====
written.append(render_page('page-medianas.html',
    'Tesote para medianas empresas | Tesote',
    'Las cuentas al día sin un departamento de finanzas gigante: bancos en vivo, cobros con link y conciliación automática.',
    phero('Soluciones · Por tamaño',
          'Las cuentas al día, sin un departamento de finanzas gigante.',
          'Tu equipo es chico y los bancos son muchos. Tesote hace el trabajo operativo para que las dos o tres personas de finanzas decidan, no transcriban.',
          None, center=True)
    + pains_sec('Te suena, ¿verdad?',
        ['El día se va entrando a portales bancarios y descargando estados de cuenta.',
         'La cobranza vive en WhatsApp y nadie sabe qué pago corresponde a qué factura.',
         'El cierre del mes tarda semanas porque la conciliación es a mano.'])
    + prod_fit([
        ('page-connect.html', 'Connect', 'Saldos y movimientos de todos tus bancos, en vivo.'),
        ('page-cobros.html', 'Cobros', 'Links de pago que entran conciliados.'),
        ('page-conciliacion.html', 'Conciliación automática', 'El cierre deja de ser un proyecto.')])
    + testi_band(T_PAISA)))

written.append(render_page('page-corporativas.html',
    'Tesote para corporativas | Tesote',
    'Multi-entidad, multi-banco, multi-moneda — consolidación en vivo, aprobaciones con control y auditoría completa.',
    phero('Soluciones · Por tamaño',
          'Multi-entidad, multi-banco, multi-moneda — bajo control.',
          'Consolidación en vivo entre entidades, aprobaciones con doble control y una auditoría que aguanta cualquier revisión.',
          None, center=True)
    + pains_sec('El problema a escala corporativa',
        ['Consolidar entidades y monedas toma días — y llega vencido.',
         'Permisos y aprobaciones viven en correos, no en un sistema.',
         'El volumen de conciliación crece más rápido que el equipo.'])
    + prod_fit([
        ('page-connect.html', 'Connect', 'Posición consolidada multi-entidad, en vivo.'),
        ('page-pagos.html', 'Pagos', 'Lotes validados con doble aprobación.'),
        ('page-conciliacion.html', 'Conciliación automática', 'El volumen crece sin crecer el equipo.'),
        ('page-seguridad.html', 'Seguridad', 'Permisos granulares y auditoría completa.')])
    + testi_band(T_CINES)))

# ===== SOLUTIONS: INDUSTRY =====
written.append(render_page('page-retail.html',
    'Tesote para retail y consumo masivo | Tesote',
    'El cuadre diario de todas tus tiendas, automático: alto volumen, múltiples cuentas y conciliación sin planillas.',
    phero('Soluciones · Por industria',
          'El cuadre diario de todas tus tiendas, automático.',
          'Alto volumen, muchas cuentas y ventas todos los días: Tesote concilia el detal sin que tu equipo viva en planillas.',
          None, center=True)
    + pains_sec('El día a día del retail',
        ['Miles de transacciones diarias entre puntos de venta, transferencias y pago móvil.',
         'Una cuenta por banco por tienda — y todas hay que cuadrarlas.',
         'El cierre diario depende de gente descargando estados de cuenta.'])
    + prod_fit([
        ('page-connect.html', 'Connect', 'Todas las cuentas de todas las tiendas, en vivo.'),
        ('page-conciliacion.html', 'Conciliación automática', 'El cuadre diario, hecho solo.'),
        ('page-pagos.html', 'Pagos', 'Proveedores pagados en lotes validados.')])
    + logo_row([('traki-d615adf4.webp', 'Traki'), ('blue-mall-c9ca5e52.webp', 'Blue Mall'), ('zara-22c602db.webp', 'Zara'),
                ('balu.png', 'Balú'), ('canguro.png', 'Canguro'), ('farmabien.png', 'Farmabien')],
               'Equipos del sector que ya operan con Tesote')))

written.append(render_page('page-alimentos.html',
    'Tesote para alimentos y agricultura | Tesote',
    'De la producción a la venta sin planillas: cobros y ventas conciliados, proveedores e insumos pagados a tiempo, márgenes a la vista.',
    phero('Soluciones · Por industria',
          'De la producción a la venta, sin planillas.',
          'Del campo y la planta al punto de venta: cosechas, insumos, proveedores toda la semana y márgenes que no perdonan. Tesote mantiene las cuentas al día en cada eslabón.',
          None, center=True)
    + pains_sec('El día a día del sector',
        ['Cobros y ventas todos los días — del mayorista al punto de venta, en varios métodos de pago.',
         'Pagos frecuentes a productores, proveedores e insumos, con retenciones que no pueden fallar.',
         'Márgenes ajustados y precios que se mueven: exigen visibilidad inmediata del flujo de caja.'])
    + prod_fit([
        ('page-connect.html', 'Connect', 'La venta de ayer, cuadrada hoy.'),
        ('page-pagos.html', 'Pagos', 'Proveedores pagados a tiempo, validados.'),
        ('page-conciliacion.html', 'Conciliación automática', 'Cierre del mes sin proyecto.')])
    + logo_row([('burger-king-831b823c.webp', 'Burger King'), ('paisa-8727515c.webp', 'Paisa'), ('munchy-6a10dc4d.webp', 'Munchy'), ('ama-de-casa-f367519b.webp', 'Ama de Casa'),
                ('inveca.png', 'Corporación Inveca')],
               'Equipos del sector que ya operan con Tesote')
    + testi_band(T_PAISA)))

written.append(render_page('page-distribucion.html',
    'Tesote para distribución y manufactura | Tesote',
    'Cobra tu cartera B2B y cuadra cada despacho: cobros identificados con su factura y pagos a proveedores en lotes.',
    phero('Soluciones · Por industria',
          'Cobra tu cartera B2B — y cuadra cada despacho.',
          'Crédito a clientes, transferencias difíciles de identificar y lotes de pagos a proveedores: el corazón de tu operación financiera, automatizado.',
          None, center=True)
    + pains_sec('El día a día de la distribución',
        ['Cartera B2B con crédito: saber quién pagó qué factura es un trabajo de detective.',
         'Transferencias entrantes sin referencia que alguien tiene que identificar.',
         'Pagos a proveedores en lotes grandes, con retenciones.'])
    + prod_fit([
        ('page-cobros.html', 'Cobros', 'Cada cobro entra amarrado a su factura.'),
        ('page-connect.html', 'Connect', 'Contrapartes identificadas automáticamente.'),
        ('page-pagos.html', 'Pagos', 'Lotes validados contra facturas y retenciones.'),
        ('page-conciliacion.html', 'Conciliación automática', 'Tu ERP al día, en ambas direcciones.')])
    + logo_row([('disbattery-126e11c0.webp', 'Disbattery'), ('hageco-3aa95de4.webp', 'Hageco'), ('mimesa-49410e74.webp', 'Grupo Mimesa'), ('asoportuguesa-819c5c19.webp', 'Asoportuguesa'), ('cencozotti-669c9c13.webp', 'Cencozotti'), ('armi-cc1041ee.webp', 'Armi'),
                ('promaker.png', 'Promaker')],
               'Equipos del sector que ya operan con Tesote')))

written.append(render_page('page-servicios-financieros.html',
    'Tesote para servicios financieros | Tesote',
    'Aseguradoras, casas de bolsa y financieras: miles de cobros identificados, pagos con doble control y todo trazable para el regulador.',
    phero('Soluciones · Por industria',
          'Miles de cobros y pagos — identificados, cuadrados y auditables.',
          'Primas, aportes y suscripciones que entran por miles; siniestros y desembolsos que exigen trazabilidad; reservas repartidas en varios bancos y monedas. Tesote lo deja cuadrado, trazable y listo para el regulador.',
          None, center=True)
    + pains_sec('El día a día de una institución financiera',
        ['Miles de cobros entran por transferencia y pago móvil — identificar cada uno es un equipo entero.',
         'Desembolsos y siniestros que exigen aprobaciones y una auditoría impecable.',
         'Reservas y fondos en múltiples bancos y monedas que hay que consolidar para el regulador.'])
    + prod_fit([
        ('page-connect.html', 'Connect', 'Posición consolidada multi-banco, en vivo.'),
        ('page-conciliacion.html', 'Conciliación automática', 'Cada cobro identificado y conciliado solo.'),
        ('page-pagos.html', 'Pagos', 'Desembolsos con doble control y auditoría.'),
        ('page-seguridad.html', 'Seguridad', 'Cifrado, permisos y auditoría completa.')])
    + logo_row([('estar-seguros-6bd639f4.webp', 'Estar Seguros'), ('seguros-crecer-3709fe89.webp', 'Seguros Crecer'), ('seguros-venezuela-3bbc7c60.webp', 'Seguros Venezuela')],
               'Instituciones financieras que ya operan con Tesote')))

# --- NEW industry pages (logos pending — Luis to add per 2026-06-18 decision) ---
written.append(render_page('page-tecnologia.html',
    'Tesote para empresas de tecnología | Tesote',
    'SaaS y tecnología: cobros recurrentes en Bs y USD, conciliados solos, con la posición de caja siempre a la vista del board.',
    phero('Soluciones · Por industria',
          'Cobros recurrentes, en cualquier moneda — conciliados solos.',
          'Suscripciones que se renuevan, cobros en Bs y en USD, y un board que pide números al día. Tesote cobra, identifica y concilia cada pago para que finanzas no viva detrás de la facturación.',
          None, center=True)
    + pains_sec('El día a día de una empresa de tecnología',
        ['Cobros recurrentes a muchos clientes — manejar la renovación y la mora a mano no escala.',
         'Ingresos en Bs y en USD que hay que consolidar a una sola posición para decidir.',
         'El board pide caja, runway y MRR al día — y armarlo cada mes toma una semana.'])
    + prod_fit([
        ('page-cobros.html', 'Cobros', 'Links de cobro recurrentes que entran conciliados.'),
        ('page-connect.html', 'Connect', 'Tu posición en Bs y USD, consolidada en vivo.'),
        ('page-conciliacion.html', 'Conciliación automática', 'Cada cobro recurrente, cuadrado solo.'),
        ('page-tesote-ai.html', 'Tesote AI', 'Pregúntale a tus finanzas y arma el reporte del board.')])
    + logo_row([('yummy.png', 'Yummy')],
               'Equipos del sector que ya operan con Tesote')))

written.append(render_page('page-petroleo-gas.html',
    'Tesote para petróleo y gas | Tesote',
    'Pagos de alto monto multi-moneda, multi-entidad y joint ventures: doble control, trazabilidad total y conciliación automática.',
    phero('Soluciones · Por industria',
          'Alto monto, multi-moneda y trazabilidad total — cuadrado.',
          'Pagos grandes a contratistas, operaciones en USD y en Bs, joint ventures y entidades que hay que consolidar. Tesote mueve cada bolívar y cada dólar con doble control y lo deja trazable de punta a punta.',
          None, center=True)
    + pains_sec('El día a día del sector',
        ['Pagos de alto monto a contratistas y proveedores que no admiten un error.',
         'Operación en varias monedas y entidades — y joint ventures que hay que consolidar.',
         'Cada movimiento tiene que quedar trazable para auditoría y para el socio operador.'])
    + prod_fit([
        ('page-connect.html', 'Connect', 'Posición multi-entidad y multi-moneda, en vivo.'),
        ('page-pagos.html', 'Pagos', 'Alto monto con doble control y auditoría.'),
        ('page-conciliacion.html', 'Conciliación automática', 'Cada movimiento cuadrado y trazable.'),
        ('page-seguridad.html', 'Seguridad', 'Permisos por rol y auditoría completa.')])))

# ===== PARTNERS =====
PARTNER_GRID = '''<div class="sec-grid" style="grid-template-columns:repeat(auto-fit,minmax(200px,1fr))">
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-screwdriver-wrench"></i></div>
    <h3 class="sec-card__title">Integradores de ERP</h3>
    <p class="sec-card__body">Implementas Odoo, Profit u otro ERP. Suma Tesote a tus proyectos y entrega la conciliación bancaria resuelta desde el día uno.</p>
  </div>
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-code"></i></div>
    <h3 class="sec-card__title">Empresas de software</h3>
    <p class="sec-card__body">Tu producto toca cobros, facturación u operación financiera. La data bancaria en vivo de Tesote puede potenciar lo que ya construiste.</p>
  </div>
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-person-chalkboard"></i></div>
    <h3 class="sec-card__title">Firmas de consultoría</h3>
    <p class="sec-card__body">Asesoras a empresas en transformación financiera. Tesote es la capa de automatización que cierra la brecha entre los bancos y el ERP de tus clientes.</p>
  </div>
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-file-invoice-dollar"></i></div>
    <h3 class="sec-card__title">Firmas contables</h3>
    <p class="sec-card__body">Llevas la contabilidad de varias empresas. Tesote entrega la data bancaria ya categorizada y la conciliación lista — tus clientes cierran más rápido.</p>
  </div>
  <div class="sec-card">
    <div class="sec-card__icon" aria-hidden="true"><i class="fa-solid fa-user-tie"></i></div>
    <h3 class="sec-card__title">Asesores</h3>
    <p class="sec-card__body">Acompañas a empresas en crecimiento. Referir Tesote les da visibilidad financiera real desde el primer día.</p>
  </div>
</div>'''

written.append(render_page('page-partners.html',
    'Partners — Crece con Tesote | Tesote',
    'Integradores de ERP, empresas de software, firmas de consultoría, firmas contables y asesores: construyamos juntos sobre la data bancaria en vivo de Tesote.',
    phero('Partners',
          'Crece con Tesote.',
          'Si integras ERPs, desarrollas software, consultas, llevas la contabilidad o asesoras empresas — hay un lugar para ti en el ecosistema Tesote.',
          None, center=True)
    + '<section class="section"><div class="container">' + center_head('Tu lugar en el ecosistema Tesote') + PARTNER_GRID + '</div></section>'
    + pains_sec('Qué recibes como partner',
        ['Entrenamiento y soporte dedicado de nuestro equipo.',
         'Acompañamiento técnico en cada implementación conjunta.',
         'Un modelo comercial que crece contigo.'])))

# ===== CLIENTES =====
ALL_LOGOS = [
    ('traki-d615adf4.webp', 'Traki'), ('blue-mall-c9ca5e52.webp', 'Blue Mall'), ('ama-de-casa-f367519b.webp', 'Ama de Casa'),
    ('estar-seguros-6bd639f4.webp', 'Estar Seguros'), ('burger-king-831b823c.webp', 'Burger King'), ('seguros-crecer-3709fe89.webp', 'Seguros Crecer'),
    ('armi-cc1041ee.webp', 'Armi'), ('mimesa-49410e74.webp', 'Grupo Mimesa'), ('grupo-cometa-0b0de340.webp', 'Grupo Cometa'),
    ('paisa-8727515c.webp', 'Paisa'), ('hageco-3aa95de4.webp', 'Hageco'), ('cines-unidos-88a1fcbc.webp', 'Cines Unidos'),
    ('nueve-once-cdb4ecbd.webp', 'Grupo Nueve Once'), ('la-sante-ffa54f67.webp', 'La Santé'), ('megalabs-45b426d7.webp', 'Megalabs'),
    ('seguros-venezuela-3bbc7c60.webp', 'Seguros Venezuela'), ('munchy-6a10dc4d.webp', 'Munchy'), ('zara-22c602db.webp', 'Zara'),
    ('asoportuguesa-819c5c19.webp', 'Asoportuguesa'), ('disbattery-126e11c0.webp', 'Disbattery'), ('abodom-09751a41.webp', 'Abodom'),
    ('cencozotti-669c9c13.webp', 'Cencozotti'),
    # added 2026-06-18 (transparent assets only; 13 solid-bg logos pending transparent re-export)
    ('yummy.png', 'Yummy'), ('inveca.png', 'Corporación Inveca'), ('promaker.png', 'Promaker'),
    ('balu.png', 'Balú'), ('canguro.png', 'Canguro'), ('farmabien.png', 'Farmabien'),
]
written.append(render_page('page-clientes.html',
    'Clientes — Equipos de finanzas que operan con Tesote | Tesote',
    'Más de 150 empresas operan sus finanzas con Tesote: retail, alimentos, distribución, seguros y más.',
    phero('Clientes',
          'Equipos de finanzas que ya operan con Tesote.',
          'Ninguno implementó solo — cada uno arrancó con nuestro equipo adentro.',
          None, center=True)
    + STATS
    + logo_row(ALL_LOGOS, None, small=False)
    + TESTI_SEC))

# ===== v54 HOMEPAGE =====
v54 = SRC
nav_old = re.search(r'<nav class="site-navbar".*?</nav>', v54, re.S)
assert nav_old, 'home nav not found'
v54 = v54.replace(nav_old.group(0), NAV_HOME, 1)
foot_old = re.search(r'<footer class="site-footer">.*?</footer>', v54, re.S)
assert foot_old, 'home footer not found'
v54 = v54.replace(foot_old.group(0), FOOTER_HOME, 1)
v54 = v54.replace('</head>', MEGA_CSS + '\n</head>', 1)
# chapter "Conoce X" links now go to the real pages (naming: Conciliación, per Luis 2026-06-11)
v54 = v54.replace('href="#agenda">Conoce Connect', 'href="page-connect.html">Conoce Connect')
v54 = v54.replace('href="#agenda">Conoce Pagos', 'href="page-pagos.html">Conoce Pagos')
v54 = v54.replace('href="#agenda">Conoce Cobros', 'href="page-cobros.html">Conoce Cobros')
v54 = v54.replace('href="#agenda">Conoce Contabilidad automática', 'href="page-conciliacion.html">Conoce Conciliación automática')
v54 = v54.replace('href="#agenda">Conoce Tesote AI', 'href="page-tesote-ai.html">Conoce Tesote AI')
open(HOME, 'w').write(v54)
written.append(HOME)

print('WROTE %d files:' % len(written))
for f in written:
    print('  ', f)
