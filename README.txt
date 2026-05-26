/* 1. ГЛОБАЛЬНЫЕ НАСТРОЙКИ */
body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; color: #333333; line-height: 1.6; }

/* Стандартные заголовки */
h1, h2, h3, h4 { color: #212529; font-weight: 600; letter-spacing: -0.02em; }

/* Специфический стиль для заголовков в карточках, чтобы они не конфликтовали */
.card-title {
    font-size: 1.25rem !important;
    font-weight: 600 !important; /* Убедись, что тут стоит 600 */
    color: #212529 !important;
}

/* 2. ТЕМА: БРЕНДОВАЯ ПАЛИТРА */
.bg-primary, .navbar, .btn-primary { background-color: #198754 !important; border-color: #198754 !important; }

/* 3. КОМПОНЕНТЫ: КАРТОЧКИ */
.card {
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    border: 1px solid rgba(0,0,0,0.08) !important; /* чуть четче рамка */
}

.card:hover {
    transform: translateY(-8px) !important; /* прыжок чуть выше */
    box-shadow: 0 20px 30px rgba(0,0,0,0.12) !important; /* тень мощнее */
    border-color: rgba(25, 135, 84, 0.3) !important; /* легкий зеленоватый контур */
}
/* Улучшение отступов внутри карточки */
.card-body {
    padding: 1.5rem !important; /* Больше "воздуха" */
}

/* Заголовок книги в карточке */
.card-title {
    font-size: 1.25rem !important;
    margin-bottom: 0.75rem !important;
    line-height: 1.3 !important;
}

/* Стиль автора */
.card-subtitle, .text-muted {
    font-size: 0.95rem !important;
    color: #6c757d !important;
    margin-bottom: 1rem !important;
}
/* Новая анимация только с прозрачностью, без трансформации */
@keyframes fadeIn { 
    from { opacity: 0; } 
    to { opacity: 1; } 
}

/* 4. КОМПОНЕНТЫ: БАДЖИ И ТЕГИ */
.badge { display: inline-block; padding: 0.4em 0.8em; font-size: 0.85em; font-weight: 600; border-radius: 6px; text-decoration: none !important; background-color: #198754 !important; color: #ffffff !important; }
.badge:hover { background-color: #157347 !important; color: #ffffff !important; }

/* --- СТИЛЬ ТЕГОВ --- */
.tag-link, a.tag-link, span.tag-link {
    display: inline-block !important;
    padding: 2px 10px !important;
    background-color: #198754 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    text-decoration: none !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    font-family: sans-serif !important;
    line-height: 1.5 !important;
    border: none !important;
}
.tag-link:hover, .tag-link:focus, .tag-link:active {
    background-color: #157347 !important;
    color: #ffffff !important;
    text-decoration: none !important;
    opacity: 1 !important;
    visibility: visible !important;
    -webkit-text-fill-color: #ffffff !important;
    background-image: none !important;
}

/* 5. ИКОНКИ */
.btn-primary i.bi { color: #ffffff !important; margin-left: 5px; }
.card .bi:not(.btn-primary i) { color: #198754 !important; }

/* 6. НАВИГАЦИЯ И ССЫЛКИ */
a:not(.navbar a):not(.dropdown-item):not(.btn):not(.card-title a):not(h1 a):not(h2 a):not(h3 a):not(.tag-link) { color: #198754 !important; text-decoration: none; }
a:not(.navbar a):not(.dropdown-item):not(.btn):not(.card-title a):not(h1 a):not(h2 a):not(h3 a):hover { color: #157347 !important; text-decoration: underline; }
.navbar a, .dropdown-item { color: rgba(255, 255, 255, 0.9) !important; }

/* 7. ЭЛЕМЕНТЫ ИНТЕРФЕЙСА */
.card-title, .card-title a, h1, h2, h3, h4, h5, h6 { color: #212529 !important; }
.btn-primary, .btn-primary a { color: #ffffff !important; }
footer { border-top: 1px solid #e9ecef; margin-top: 2rem; }
.avatar-small { width: 32px; height: 32px; border-radius: 50%; object-fit: cover; }

/* 8. ТЕГИ-ФИКС */
.tag-fix { display: inline-block !important; padding: 5px 12px !important; background-color: #198754 !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; border-radius: 6px !important; text-decoration: none !important; font-weight: 700 !important; font-size: 14px !important; border: none !important; opacity: 1 !important; filter: none !important; }
.tag-fix:hover { background-color: #157347 !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }

/* ПРИНУДИТЕЛЬНОЕ ВЫРАВНИВАНИЕ ВСЕХ ТЕГОВ */
h1 .tag-link, h2 .tag-link, h3 .tag-link, 
h1 .tag-fix, h2 .tag-fix, h3 .tag-fix,
.card-body .tag-link, .card-body .tag-fix {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: normal !important;
    font-size: 14px !important;
    text-transform: none !important;
}

/* 9. АНИМАЦИЯ КНОПОК (добавь это в конец файла) */
.btn {
    transition: transform 0.3s cubic-bezier(0.2, 0, 0, 1), box-shadow 0.3s ease !important;
}
.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

input.form-control:focus, 
input[type="text"]:focus {
    border-color: #198754 !important;
    box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

body {
    animation: fadeIn 0.3s ease-out; /* ускорили до 0.3с */
}

@keyframes fadeIn { 
    from { opacity: 0.8; } /* начинаем с 0.8, а не с 0 */
    to { opacity: 1; } 
}
