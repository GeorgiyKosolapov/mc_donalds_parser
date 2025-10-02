McDonald's Ukraine Menu Scraper & API
Test Task for Udata Company

СТРУКТУРА ПРОЕКТУ:
├── parser.py          # Скрейпер для збору даних з сайту McDonald's
├── handles.py         # FastAPI сервер з API ендпоінтами
├── requirements.txt   # Залежності Python
├── products.json      # Зібрані дані (автоматично створюється)
└── README.txt         # Цей файл

ТЕХНІЧНИЙ СТЕК:
- Python 3.8+
- requests, BeautifulSoup4 (парсинг веб-сторінок)
- Selenium WebDriver (автоматизація браузера)
- FastAPI (веб API)
- JSON (зберігання даних)

ЯК ВСТАНОВИТИ:
1. Встановити Python 3.8+ і Google Chrome
2. Встановити залежності: pip install -r requirements.txt
3. Запустити скрейпер: python parser.py
4. Запустити API: uvicorn handles:app --reload
5. API доступне за адресою: http://localhost:8000

API ЕНДПОІНТИ:
- GET /products/ - всі продукти
- GET /products/{назва_продукту} - конкретний продукт
- GET /products/{назва_продукту}/{поле} - конкретне поле продукту
