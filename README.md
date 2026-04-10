# 🛸 Cyber Y2K Personal Digital Space

**A retro-futuristic personal blog inspired by early-2000s internet culture — built with Flask.**

---

## 📸 Visual Demonstration

<!-- Replace the comments below with actual screenshots or a demo GIF -->
<!-- ![Demo GIF](docs/assets/demo.gif) -->

| Home | Write | Guestbook |
|:----:|:-----:|:---------:|
| ![Home](<img width="1920" height="917" alt="image" src="https://github.com/user-attachments/assets/38c49559-5cb9-4f6e-98ff-53acd41c08b0" />
) | ![Write](<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/f01bee0a-ce09-4465-97a5-08f059facc97" />
) | ![Guestbook](<img width="1920" height="911" alt="image" src="https://github.com/user-attachments/assets/4969e7c7-94b7-4610-adbc-6fcc50dc0de0" />
) |

---

## 💡 Motivation & Problem

Modern web design has become homogeneous — clean, minimal, and predictable.
This project is a deliberate throwback to the raw creativity of early-2000s personal homepages:
Cyworld mini-hompys, chrome textures, CRT monitor glow, and visitor counters.

The goal was to learn **full-stack web fundamentals** (routing, templating, ORM, testing, API documentation)
by building something fun rather than another generic CRUD app.
Every technical decision was made to maximize learning while keeping the Y2K vibe alive.

---

## 🛠 Tech Stack & Rationale

| Technology | Why I Chose It |
|------------|---------------|
| **Flask 3.1.2** | Micro-framework with zero boilerplate — gives full control over architecture instead of hiding it behind magic. |
| **Flask-SQLAlchemy** | ORM-based DB access prevents raw SQL and provides built-in protection against SQL injection. |
| **Flasgger** | Generates interactive Swagger UI directly from docstrings — API docs stay in sync with code automatically. |
| **Sphinx** | Extracts Google-style docstrings into browsable HTML docs; deployable to GitHub Pages. |
| **pytest** | 8 test cases covering CRUD, SQL injection, XSS, length limits, whitespace bypass, and pagination. |

---

## ✨ Key Features

- **Y2K Aesthetic** — CRT glow effects, chrome textures, retro visitor counter, and Cyworld-inspired guestbook UI.
- **Guestbook CRUD** — Create and read entries with full server-side input validation (empty, whitespace-only, length overflow).
- **Security by Default** — SQL injection blocked by SQLAlchemy ORM; XSS neutralized by Jinja2 auto-escaping.
- **Pagination** — Guestbook queries are capped at 10 entries to prevent memory exhaustion from unbounded `.all()` calls.
- **Interactive API Docs** — Swagger UI at `/apidocs` with OpenAPI specs embedded in every route's docstring.
- **Auto-generated Code Docs** — Sphinx + Napoleon parse Google-style docstrings into a full HTML documentation site.

---

## 🚀 Getting Started

> WSL (Ubuntu) environment. Works identically on macOS and native Linux.

```bash
# 1. Clone the repository
git clone https://github.com/bobbingi0000/OSP_Flask-blog.git
cd OSP_Flask-blog

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the development server
export FLASK_APP=run.py
flask run --debug

# 5. Run tests
pytest -v
```

- **App** → http://127.0.0.1:5000
- **Swagger UI** → http://127.0.0.1:5000/apidocs
- **Sphinx Docs** → [GitHub Pages](https://bobbingi0000.github.io/OSP_Flask-blog/) *(deploy to activate)*
