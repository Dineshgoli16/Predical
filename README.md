# PrediCAL

PrediCAL is a clinical decision-support web application that predicts the statistical probability of post-operative hypocalcemia using a machine learning model.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Machine Learning**: Scikit-Learn & XGBoost
- **Frontend**: Vanilla HTML/JS with Tailwind CSS

## Setup Instructions

### 1. Install Dependencies
Ensure you have Python 3.8+ installed. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 2. Train the Machine Learning Model
Run the training script to generate the synthetic clinical dataset, evaluate multiple models (Logistic Regression, Random Forest, XGBoost), and save the top-performing model (`model.joblib`).
```bash
python train_model.py
```

### 3. Start the Backend Server
Run the FastAPI application using Uvicorn. This will serve the prediction API locally.
```bash
uvicorn main:app --reload
```
The API will be available at `http://127.0.0.1:8000`. You can also view the auto-generated Swagger documentation at `http://127.0.0.1:8000/docs`.

### 4. Launch the Frontend
Open the `index.html` file in any modern web browser to access the PrediCAL clinical dashboard. It connects automatically to the locally running FastAPI backend.
