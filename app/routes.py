"""Routes module — Defines all URL endpoints for the Y2K blog.

This module contains the view functions to be registered with the
Flask app. Each function includes a Flasgger (OpenAPI 3.0) docstring
for automatic documentation at ``/apidocs``.
"""

from flask import Flask, render_template, request, redirect, url_for
from app.models import db, GuestbookEntry


def register_routes(application: Flask) -> None:
    """Registers all URL rules with the Flask app instance.

    Binds three endpoints — Home (``/``), Write (``/write``), and
    Guestbook (``/guestbook``) — to the Flask app. Each view function
    contains a Flasgger OpenAPI YAML docstring for automatic exposure
    in Swagger UI.

    Args:
        application (Flask): Flask application instance.
            The app object created by the ``create_app()`` factory.

    Returns:
        None: This function has no return value. It registers routes
            on the app as a side effect.
    """

    # ── 1. Home Page ─────────────────────────────────────────────
    @application.route('/')
    @application.route('/home')
    def home() -> str:
        """Renders the Y2K blog main page.

        Serves as the blog landing page with a retro visitor counter
        aesthetic and a recent posts feed.

        Returns:
            str: Rendered ``index.html`` template HTML string.

        ---
        tags:
          - Home
        summary: Retrieve main page
        description: |
          The blog landing page. Features a retro visitor counter
          aesthetic and a recent posts feed.
        responses:
          200:
            description: Successfully returns the home page HTML.
            content:
              text/html:
                schema:
                  type: string
                  example: "<html>...Y2K Home...</html>"
        """
        return render_template('index.html')

    # ── 2. Write Page ────────────────────────────────────────────
    # TODO: Enable DB persistence after Post model is implemented (set feature_ready=True)
    @application.route('/write', methods=['GET', 'POST'])
    def write() -> str:
        """Renders the terminal-style writing page.

        On GET request, displays a hacker/cyber-themed terminal-style
        writing form. On POST request, submits the title to the server.
        DB persistence is currently disabled.

        Returns:
            str: Rendered ``write.html`` template HTML string.
                Includes the submitted title on POST requests.

        ---
        tags:
          - Write
        summary: View write form / submit post
        description: |
          **GET**: Displays a hacker/cyber-themed terminal-style writing form.
          **POST**: Submits the title to the server.
          *DB persistence is currently disabled (feature_ready=False).*
        parameters:
          - in: formData
            name: title
            type: string
            required: false
            description: Post title (for POST requests)
            example: "Millennium Diary ✨"
        responses:
          200:
            description: Successfully returns the write page HTML.
            content:
              text/html:
                schema:
                  type: string
        """
        if request.method == 'POST':
            title = request.form.get('title')
            return render_template('write.html', title=title, feature_ready=False)
        return render_template('write.html', feature_ready=False)

    # ── 3. Guestbook Page ────────────────────────────────────────
    @application.route('/guestbook', methods=['GET', 'POST'])
    def guestbook() -> str:
        """Retrieves or creates Y2K mini-homepage style guestbook entries.

        On GET request, displays the 10 most recent guestbook entries
        in descending order. On POST request, validates the author and
        content fields before saving to the database.

        Validation rules:
            - author: required, no whitespace-only, max 50 chars
            - content: required, no whitespace-only, max 500 chars

        Returns:
            str: Rendered ``guestbook.html`` HTML string on GET request.
                A 302 redirect response to ``/guestbook`` on POST request.

        Raises:
            sqlalchemy.exc.IntegrityError: May occur if a database
                constraint is violated. However, pre-validation ensures
                this does not happen under normal flow.

        ---
        tags:
          - Guestbook
        summary: View guestbook / create new entry
        description: |
          **GET**: Displays the 10 most recent guestbook entries in descending order.
          **POST**: Validates author and content, then saves to the database.

          ### Validation Rules
          | Field   | Constraint                              |
          |---------|-----------------------------------------|
          | author  | Required, no whitespace-only, max 50    |
          | content | Required, no whitespace-only, max 500   |
        parameters:
          - in: formData
            name: author
            type: string
            required: true
            description: Guestbook author name (max 50 chars, whitespace-only not allowed)
            example: "Neo"
          - in: formData
            name: content
            type: string
            required: true
            description: Guestbook message content (max 500 chars, whitespace-only not allowed)
            example: "Follow the white rabbit 🐇"
        responses:
          200:
            description: Successfully returns the guestbook page HTML (GET request).
            content:
              text/html:
                schema:
                  type: string
          302:
            description: |
              Redirects to the guestbook page after POST request.
              - On successful save → redirects to guestbook list
              - On validation failure → redirects to guestbook list (no save)
            headers:
              Location:
                description: Redirect target URL
                schema:
                  type: string
                  example: "/guestbook"
        """
        if request.method == 'POST':
            author = request.form.get('author', '').strip()
            content = request.form.get('content', '').strip()

            if not author or not content:
                return redirect(url_for('guestbook'))
            if len(author) > 50 or len(content) > 500:
                return redirect(url_for('guestbook'))

            entry = GuestbookEntry(author=author, content=content)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('guestbook'))

        entries = GuestbookEntry.query.order_by(
            GuestbookEntry.created_at.desc()
        ).limit(10).all()
        return render_template('guestbook.html', entries=entries)
