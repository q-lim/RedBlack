# Question Flip

Tap **Get a question** and the card flips to reveal a random question.
A question won't repeat until more than half the bank has been shown since it last appeared.

## Files
| File | Job |
|---|---|
| `index.html` / `style.css` | Page layout and the flip-card look |
| `app.js` | Button, flip animation, loading the questions |
| `deck.js` | The "no early repeats" logic |
| `questions.json` | The question bank |
| `validate_questions.py` | Python checker for the question bank |

## Add questions
Add a line to `questions.json` with a new unique `id`, then run:

    python validate_questions.py

## Try it on your computer
    python -m http.server
Then open http://localhost:8000 (opening index.html directly won't load the questions).

## Publish on GitHub
1. Upload all files to a new repository.
2. Settings → Pages → Source: "Deploy from a branch" → `main` / `(root)`.
3. Your app appears at `https://<username>.github.io/<repo>/`.
