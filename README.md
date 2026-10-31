# PrediCAL – AI

Clinical decision-support web application for predicting postoperative hypocalcemia and Hungry Bone Syndrome in Primary Hyperparathyroidism (PHPT), guiding safe ambulatory same-day discharge versus inpatient calcium replacement.

## Tech Stack
- **Backend Engine**: Flask (Python 3.8+)
- **Production Server**: Gunicorn (WSGI)
- **Frontend Dashboard**: Responsive, mobile-first HTML5 / Tailwind CSS
- **Model**: Multivariable Logistic Regression (Table 1B, TRIPOD Type 2b Validated, N = 979)

## Deployment on Render.com

This repository is pre-configured with `render.yaml` and `Procfile` for 1-click deployment on [Render](https://render.com):

1. **Push this repository to GitHub**:
   ```bash
   git remote add origin https://github.com/<your-username>/predical.git
   git push -u origin main
   ```
2. **Deploy on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com).
   - Click **New +** -> **Web Service**.
   - Connect your `predical` GitHub repository.
   - Settings are detected automatically from `render.yaml`:
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn main:app`
   - Click **Deploy Web Service**.
3. **Live URL**: Render will assign a free live HTTPS URL (e.g., `https://predical-ai.onrender.com`).
