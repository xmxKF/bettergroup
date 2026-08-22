/* 倍特爾科技集團 — main.js
   純 vanilla JS，無相依套件、無外部請求。
   1) 行動選單開合  2) sticky header 狀態  3) fade-up 進場
   4) 依 pathname 標記目前導覽項  5) 詢問表單 mailto 組合器
   6) 表格橫捲提示  7) 媒體佔位載入偵測  8) 錨點展開手風琴 */
(function () {
  'use strict';

  var doc = document;
  var root = doc.documentElement;

  /* base.html 的 inline script 只有在這個標記出現時才會保留淡入的隱藏起始狀態；
     這裡先接手，再把全部初始化包進 try/catch —— 任何未預期的錯誤都不得讓內容留在隱藏狀態。 */
  root.classList.add('js-ready');

  try {

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── 1. 行動選單 ────────────────────────────────────────────── */
  var toggle = doc.querySelector('[data-nav-toggle]');
  var panel = doc.querySelector('[data-nav-panel]');
  if (toggle && panel) {
    var navLabel = function (open) {
      return toggle.getAttribute(open ? 'data-label-close' : 'data-label-open') ||
             (open ? '關閉主選單' : '開啟主選單');
    };
    var setNav = function (open) {
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
      toggle.setAttribute('aria-label', navLabel(open));
      panel.classList.toggle('is-open', open);
      doc.body.classList.toggle('nav-open', open);
    };
    toggle.addEventListener('click', function () {
      setNav(toggle.getAttribute('aria-expanded') !== 'true');
    });
    panel.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setNav(false); }
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setNav(false); toggle.focus();
      }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth >= 960) { setNav(false); }
    });
  }

  /* ── 2. Sticky header 狀態 ─────────────────────────────────── */
  var header = doc.querySelector('[data-header]');
  if (header) {
    var ticking = false;
    var onScroll = function () {
      if (ticking) { return; }
      ticking = true;
      window.requestAnimationFrame(function () {
        header.classList.toggle('is-stuck', window.scrollY > 8);
        ticking = false;
      });
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ── 3. Fade-up 進場（唯一的捲動動畫，只播一次） ───────────── */
  var reveals = [].slice.call(doc.querySelectorAll('.reveal'));
  if (reveals.length) {
    if (reduceMotion || !('IntersectionObserver' in window)) {
      reveals.forEach(function (el) { el.classList.add('is-visible'); });
    } else {
      var io = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.15, rootMargin: '0px 0px -10% 0px' });
      reveals.forEach(function (el) { io.observe(el); });
    }
  }

  /* ── 4. 目前導覽項 ─────────────────────────────────────────── */
  var path = window.location.pathname.split('/').pop() || 'index.html';
  [].forEach.call(doc.querySelectorAll('[data-nav]'), function (link) {
    var match = link.getAttribute('data-nav-match') || link.getAttribute('data-nav');
    var targets = match.split(' ');
    var hit = targets.some(function (t) { return t === path; });
    if (hit) { link.setAttribute('aria-current', 'page'); }
    else { link.removeAttribute('aria-current'); }
  });

  /* ── 5. 詢問表單 mailto 組合器（無表單的頁面自動略過） ──────── */
  var form = doc.querySelector('[data-mailto-form]');
  if (form) {
    var MAIL_TO = form.getAttribute('data-mailto') || 'better_stg@163.com';
    var t = function (name, fallback) {
      return form.getAttribute('data-' + name) || fallback;
    };
    var msgFor = function (field) {
      if (field.validity.valueMissing) {
        return field.tagName === 'SELECT'
          ? t('msg-select', '請選擇需求類別。')
          : t('msg-required', '此欄位為必填。');
      }
      if (field.validity.typeMismatch && field.type === 'email') {
        return t('msg-email', '請輸入正確的電子郵件格式。');
      }
      return '';
    };
    var validate = function (field) {
      var wrap = field.closest('.field');
      var out = wrap && wrap.querySelector('.error');
      var text = field.checkValidity() ? '' : msgFor(field);
      if (wrap) { wrap.classList.toggle('has-error', !!text); }
      if (out) { out.textContent = text; }
      field.setAttribute('aria-invalid', text ? 'true' : 'false');
      /* 讓已標紅的欄位在重新聚焦時也能唸出原因（role="alert" 只在訊息出現的當下播報一次） */
      if (out && out.id) {
        if (text) { field.setAttribute('aria-describedby', out.id); }
        else { field.removeAttribute('aria-describedby'); }
      }
      return !text;
    };
    var fields = [].slice.call(form.querySelectorAll('input, select, textarea'));
    fields.forEach(function (f) {
      f.addEventListener('blur', function () { validate(f); });
      f.addEventListener('input', function () {
        if (f.closest('.field') && f.closest('.field').classList.contains('has-error')) { validate(f); }
      });
    });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var ok = true, firstBad = null;
      fields.forEach(function (f) {
        if (!validate(f) && ok) { ok = false; firstBad = f; }
      });
      if (!ok) { if (firstBad) { firstBad.focus(); } return; }
      var v = function (n) { var el = form.elements[n]; return el ? el.value.trim() : ''; };
      var sep = t('mail-sep', '：');
      var ssep = t('mail-subject-sep', '｜');
      var subject = t('mail-subject', '網站詢問') + ssep + v('category') + ssep + v('company');
      var body = [
        t('mail-name', '姓名') + sep + v('name'),
        t('mail-company', '公司') + sep + v('company'),
        t('mail-email', 'Email') + sep + v('email'),
        t('mail-phone', '電話') + sep + v('phone'),
        t('mail-category', '需求類別') + sep + v('category'),
        '',
        t('mail-message', '訊息') + sep.replace(/\s+$/, ''),
        v('message')
      ].join('\r\n');
      window.location.href = 'mailto:' + MAIL_TO +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);
    });
    /* 送出鍵只有在上面的 submit 監聽器掛好之後才啟用；無 JS（或本檔載入失敗）時
       它維持 disabled，瀏覽器不會對沒有 action 的表單做 GET，詢問內容也就不會
       進到網址列與瀏覽歷史。無 JS 的替代路徑在 contact.html 的 <noscript> 內。 */
    var submitBtn = form.querySelector('[data-mailto-submit]');
    if (submitBtn) { submitBtn.disabled = false; }
  }

  /* ── 6. 表格橫捲：真的溢出時才顯示右緣漸隱提示 ─────────────── */
  var tableWraps = [].slice.call(doc.querySelectorAll('.table-wrap'));
  if (tableWraps.length) {
    var syncTableFade = function () {
      tableWraps.forEach(function (wrap) {
        var sc = wrap.querySelector('.table-scroll');
        if (!sc) { return; }
        wrap.classList.toggle('is-scrollable', sc.scrollWidth > sc.clientWidth + 1);
      });
    };
    syncTableFade();
    window.addEventListener('resize', syncTableFade);
    if (doc.fonts && doc.fonts.ready) { doc.fonts.ready.then(syncTableFade); }
  }

  /* ── 7. 媒體佔位：載入成功才顯示媒體，失敗則保留佔位 ───────── */
  [].forEach.call(doc.querySelectorAll('.media'), function (box) {
    var el = box.querySelector('img, video');
    if (!el) { return; }
    var ok = function () { box.classList.add('is-loaded'); el.hidden = false; };
    var fail = function () { box.classList.remove('is-loaded'); el.hidden = true; };
    if (el.tagName === 'IMG') {
      if (el.complete) { (el.naturalWidth > 0 ? ok : fail)(); }
      el.addEventListener('load', ok);
      el.addEventListener('error', fail);
    } else {
      // 影片檔尚未產出時，若已有 poster 就顯示 poster，否則保留佔位框
      var posterFallback = function () {
        var poster = el.getAttribute('poster');
        if (!poster) { fail(); return; }
        var probe = new Image();
        probe.onload = function () { ok(); box.classList.add('is-poster-only'); };
        probe.onerror = fail;
        probe.src = poster;
      };
      if (el.readyState >= 1) { ok(); }
      el.addEventListener('loadeddata', ok);
      el.addEventListener('error', posterFallback, true);
      [].forEach.call(el.querySelectorAll('source'), function (s) {
        s.addEventListener('error', function () { if (el.readyState < 1) { posterFallback(); } });
      });
      if (!reduceMotion && el.hasAttribute('data-autoplay')) {
        el.setAttribute('autoplay', '');
        var kick = el.play();
        if (kick && kick.catch) { kick.catch(function () {}); }
      }
      var ctrl = box.querySelector('[data-media-ctrl]');
      if (ctrl) {
        var ctrlLabel = function (attr, fallback) {
          return ctrl.getAttribute(attr) || fallback;
        };
        var sync = function () {
          var playing = !el.paused;
          ctrl.textContent = playing
            ? ctrlLabel('data-label-pause', '暫停影片')
            : ctrlLabel('data-label-play', '播放影片');
          ctrl.setAttribute('aria-label', playing
            ? ctrlLabel('data-aria-pause', '暫停背景影片')
            : ctrlLabel('data-aria-play', '播放背景影片'));
        };
        ctrl.addEventListener('click', function () { el.paused ? el.play() : el.pause(); });
        el.addEventListener('play', sync);
        el.addEventListener('pause', sync);
        sync();
      }
    }
  });

  /* ── 8. 錨點指向手風琴時自動展開該列 ───────────────────────── */
  var openHashAccordion = function () {
    if (!window.location.hash || window.location.hash.length < 2) { return; }
    var target;
    try { target = doc.querySelector(window.location.hash); } catch (err) { return; }
    if (!target || target.tagName !== 'DETAILS') { return; }
    target.open = true;
    /* fade-up 進場會把目標往上位移 16px，落點因此偏高；待捲動停止後校正一次 */
    var last = -1, tries = 0;
    var settle = window.setInterval(function () {
      var y = Math.round(window.scrollY);
      if (y === last || ++tries > 20) {
        window.clearInterval(settle);
        if (target.getBoundingClientRect().top < 88) { target.scrollIntoView(); }
      }
      last = y;
    }, 120);
  };
  window.addEventListener('hashchange', openHashAccordion);
  openHashAccordion();

  } catch (err) {
    /* 初始化失敗：撤掉淡入的隱藏起始狀態，內容立即完整可見。 */
    root.classList.remove('js-anim');
    if (window.console && window.console.error) { window.console.error(err); }
  }
})();
