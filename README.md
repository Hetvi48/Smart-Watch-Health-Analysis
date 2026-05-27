# Smart Watch Health Analysis Website

A simple static website for smartwatch health analysis with two prediction flows:

- `Health Model`: predicts health category using all features, including stress level.
- `Stress Model`: first estimates stress level, then predicts health category for devices without stress tracking.

## Files

- `index.html` — landing page, feature overview, and prediction form.
- `styles.css` — sporty pastel green/light grey styling and animations.
- `script.js` — form handling and mock prediction logic.

## Run locally

This site uses the trained Random Forest models saved in `health_system_v1.pkl`. Run the Flask server from the project root and open the app in your browser.

```bash
python -m pip install -r requirements.txt
python app.py
```

Then visit `http://127.0.0.1:5000`.
# Working on a project
