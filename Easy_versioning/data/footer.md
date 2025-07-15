<!-- Versions and languages set-up -->
<style>
  .fixed-bar {
    position: fixed;
    bottom: 10px;
    right: 10px;
    background: rgba(240, 240, 240, 0.85);
    border: 1px solid rgba(100, 100, 100, 0.3);
    border-radius: 6px;
    box-shadow: 0 1px 6px rgba(0, 0, 0, 0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 0.9rem;
    color: #222;
    display: flex;
    gap: 12px;
    padding: 6px 12px;
    align-items: center;
    z-index: 9999;
    backdrop-filter: saturate(180%) blur(10px);
  }

  @media print {
    .fixed-bar {
      display: none !important;
    }
  }

  .fixed-bar .dropdown {
    position: relative;
    user-select: none;
  }

  .fixed-bar .dropdown-toggle {
    background-color: rgba(200, 200, 200, 0.4);
    color: #222;
    padding: 6px 10px;
    border: 1px solid rgba(100, 100, 100, 0.3);
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    white-space: nowrap;
    transition: background-color 0.3s ease;
  }

  .fixed-bar .dropdown-toggle::after {
    content: none !important;
    display: none !important;
  }

  .fixed-bar .dropdown-toggle:hover {
    background-color: rgba(100, 150, 220, 0.2);
    color: #1a3e72;
    border-color: rgba(26, 62, 114, 0.6);
  }

  .fixed-bar .dropdown-toggle .fa {
    font-size: 0.9rem;
  }

  .fixed-bar .dropdown-menu {
    position: absolute;
    bottom: 100%;
    left: 0;
    background-color: rgba(250, 250, 250, 0.95);
    border: 1px solid rgba(150, 150, 150, 0.3);
    border-radius: 4px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
    min-width: 140px;
    max-height: 200px;
    overflow-y: auto;
    display: none;
    flex-direction: column;
    z-index: 10000;
    backdrop-filter: saturate(180%) blur(8px);
  }

  .fixed-bar .dropdown-menu.show {
    display: flex;
  }

  .fixed-bar .dropdown-menu a {
    padding: 8px 12px;
    color: #1a3e72;
    text-decoration: none;
    border-bottom: 1px solid rgba(200, 200, 200, 0.5);
    white-space: nowrap;
    transition: background-color 0.25s ease;
  }

  .fixed-bar .dropdown-menu a:last-child {
    border-bottom: none;
  }

  .fixed-bar .dropdown-menu a:hover {
    background-color: rgba(100, 150, 220, 0.15);
  }
</style>

<div class="fixed-bar" role="region" aria-label="Version and language selector">
  <div class="dropdown">
    <div class="dropdown-toggle" tabindex="0" aria-haspopup="listbox" aria-expanded="false">
      <span class="fa fa-book" aria-hidden="true"></span>
      Version: <span class="current-value">{version}</span>
      <span class="fa caret-icon fa-caret-down" aria-hidden="true"></span>
    </div>
    <div class="dropdown-menu" role="listbox">
      {html_v}
    </div>
  </div>

  <div class="dropdown">
    <div class="dropdown-toggle" tabindex="0" aria-haspopup="listbox" aria-expanded="false">
      <span class="fa fa-globe" aria-hidden="true"></span>
      Language: <span class="current-value">{language}</span>
      <span class="fa caret-icon fa-caret-down" aria-hidden="true"></span>
    </div>
    <div class="dropdown-menu" role="listbox">
      {html_l}
    </div>
  </div>
</div>

<script>
  document.querySelectorAll('.fixed-bar .dropdown').forEach(dropdown => {
    const toggle = dropdown.querySelector('.dropdown-toggle');
    const menu = dropdown.querySelector('.dropdown-menu');
    const displaySpan = dropdown.querySelector('.current-value');

    toggle.addEventListener('click', e => {
      e.stopPropagation();
      const isExpanded = toggle.getAttribute('aria-expanded') === 'true';

      document.querySelectorAll('.fixed-bar .dropdown-menu').forEach(m => {
        if (m !== menu) m.classList.remove('show');
      });
      dropdown.closest('.fixed-bar').querySelectorAll('.dropdown-toggle').forEach(t => {
        t.setAttribute('aria-expanded', 'false');
        const caret = t.querySelector('.caret-icon');
        if (caret) {
          caret.classList.remove('fa-caret-up');
          caret.classList.add('fa-caret-down');
        }
      });

      if (!isExpanded) {
        menu.classList.add('show');
        toggle.setAttribute('aria-expanded', 'true');
        const caret = toggle.querySelector('.caret-icon');
        if (caret) {
          caret.classList.remove('fa-caret-down');
          caret.classList.add('fa-caret-up');
        }
      }
    });

    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', e => {
        e.preventDefault();
        const selectedValue = link.textContent.trim();
        displaySpan.textContent = selectedValue;

        const currentPath = window.location.pathname;
        const segments = currentPath.split('/').filter(Boolean);

        const languages = {l_list}; // languages placeholder
        const versions = {v_list};  // Versions placeholder
        const defaultLang = '{default_language}'; // languages fallback

        const langIndex = segments.findIndex(s => languages.includes(s));
        const verIndex = segments.findIndex(s => versions.includes(s));

        if (toggle.textContent.includes('Language') && langIndex !== -1) {
          segments[langIndex] = selectedValue;
        }

        if (toggle.textContent.includes('Version') && verIndex !== -1) {
          segments[verIndex] = selectedValue;
        }

        const newPath = '/' + segments.join('/');

        // Changing version/language
        fetch(newPath, { method: 'HEAD' })
          .then(response => {
            if (response.ok) {
              window.location.pathname = newPath;
            } else {
              const fallbackPath = `/${segments[verIndex]}/${segments[langIndex]}/index.html`;
              fetch(fallbackPath, { method: 'HEAD' })
                .then(fallbackResponse => {
                  if (fallbackResponse.ok) {
                    window.location.pathname = fallbackPath;
                  } else {
                    const defaultPath = `/${segments[verIndex]}/${defaultLang}/index.html`;
                    window.location.pathname = defaultPath;
                  }
                })
                .catch(() => {
                  const defaultPath = `/${segments[verIndex]}/${defaultLang}/index.html`;
                  window.location.pathname = defaultPath;
                });
            }
          })
          .catch(() => {
            const fallbackPath = `/${segments[verIndex]}/${segments[langIndex]}/index.html`;
            window.location.pathname = fallbackPath;
          });

        menu.classList.remove('show');
        toggle.setAttribute('aria-expanded', 'false');
        const caret = toggle.querySelector('.caret-icon');
        if (caret) {
          caret.classList.remove('fa-caret-up');
          caret.classList.add('fa-caret-down');
        }
      });
    });
  });

  window.addEventListener('click', () => {
    document.querySelectorAll('.fixed-bar .dropdown-menu').forEach(menu => menu.classList.remove('show'));
    document.querySelectorAll('.fixed-bar .dropdown-toggle').forEach(t => {
      t.setAttribute('aria-expanded', 'false');
      const caret = t.querySelector('.caret-icon');
      if (caret) {
        caret.classList.remove('fa-caret-up');
        caret.classList.add('fa-caret-down');
      }
    });
  });

  window.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      document.querySelectorAll('.fixed-bar .dropdown-menu').forEach(menu => menu.classList.remove('show'));
      document.querySelectorAll('.fixed-bar .dropdown-toggle').forEach(t => {
        t.setAttribute('aria-expanded', 'false');
        const caret = t.querySelector('.caret-icon');
        if (caret) {
          caret.classList.remove('fa-caret-up');
          caret.classList.add('fa-caret-down');
        }
      });
    }
  });
</script>


<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
