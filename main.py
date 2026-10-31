import math
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ==============================================================================
# PREDICAL - AI: CLINICAL DECISION SUPPORT ENGINE (8 VARIABLES, SEX OMITTED)
# Predicts postoperative hypocalcemia & Hungry Bone Syndrome risk in PHPT.
# ==============================================================================

# Multivariable Model Parameters from Derivation Cohort (Table 1B)
INTERCEPT = -1.8649

COEFFICIENTS = {
    'ALP': 2.2035,        # Adjusted OR = 9.06 (p < 0.0001)
    'PTH': 1.4303,        # Adjusted OR = 4.18 (p < 0.0001)
    'PHOSPHORUS': -1.2852, # Adjusted OR = 0.28 (p < 0.0001)
    'VIT_D': -1.2243,     # Adjusted OR = 0.29 (p < 0.0001)
    'CA': -0.6748         # Adjusted OR = 0.51 (p = 0.0001)
}

MEANS = {
    'ALP': 185.08,
    'PTH': 386.48,
    'PHOSPHORUS': 2.32,
    'VIT_D': 17.94,
    'CA': 12.37
}

STDS = {
    'ALP': 232.06,
    'PTH': 332.90,
    'PHOSPHORUS': 0.49,
    'VIT_D': 9.40,
    'CA': 1.41
}

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json or {}

    try:
        # The 8 clinical inputs (Biological sex omitted)
        ca = float(data.get('CA', MEANS['CA']))
        phos = float(data.get('PHOSPHORUS', MEANS['PHOSPHORUS']))
        pth = float(data.get('PTH', MEANS['PTH']))
        alp = float(data.get('ALP', MEANS['ALP']))
        vit_d = float(data.get('VIT_D', data.get('VIT D', MEANS['VIT_D'])))
        post_op_pth = float(data.get('POST_OP_PTH', data.get('POST OP PTH', 8.5)))
        no_of_tumours = int(data.get('NO_OF_TUMOURS', data.get('NO OF TUMOURS', 1)))
        bmd_n = int(data.get('BMD_N', 0))

        # Standardized log-odds calculation
        z_alp = (alp - MEANS['ALP']) / STDS['ALP'] if STDS['ALP'] > 0 else 0.0
        z_pth = (pth - MEANS['PTH']) / STDS['PTH'] if STDS['PTH'] > 0 else 0.0
        z_phos = (phos - MEANS['PHOSPHORUS']) / STDS['PHOSPHORUS'] if STDS['PHOSPHORUS'] > 0 else 0.0
        z_vitd = (vit_d - MEANS['VIT_D']) / STDS['VIT_D'] if STDS['VIT_D'] > 0 else 0.0
        z_ca = (ca - MEANS['CA']) / STDS['CA'] if STDS['CA'] > 0 else 0.0

        log_odds = INTERCEPT + (
            COEFFICIENTS['ALP'] * z_alp +
            COEFFICIENTS['PTH'] * z_pth +
            COEFFICIENTS['PHOSPHORUS'] * z_phos +
            COEFFICIENTS['VIT_D'] * z_vitd +
            COEFFICIENTS['CA'] * z_ca
        )

        probability = 1.0 / (1.0 + math.exp(-log_odds))
        probability_pct = round(probability * 100.0, 1)

        # 3-Tier Clinical Triage Protocol
        if probability < 0.15:
            risk_tier = "Mild Risk"
            tier_code = "MILD"
            discharge_pathway = "Safe for Same-Day Discharge (4–6 hours)"
            calcium_regimen = "Standard maintenance oral calcium (500 mg BID)"
            monitoring_protocol = "Standard vital checks; eligible for ambulatory fast-track discharge."
        elif probability < 0.50:
            risk_tier = "Moderate Risk"
            tier_code = "MODERATE"
            discharge_pathway = "Extended Observation (6–12 hrs) or Short-Stay Bed"
            calcium_regimen = "Prophylactic oral calcitriol (0.5 mcg qd) + oral calcium (1000 mg TID)"
            monitoring_protocol = "Discharge on Postoperative Day 1 if 6-hour calcium remains stable."
        else:
            risk_tier = "Severe Risk"
            tier_code = "SEVERE"
            discharge_pathway = "Mandatory Inpatient Telemetry (24–48 hours)"
            calcium_regimen = "Preemptive IV calcium gluconate access on standby"
            monitoring_protocol = "Continuous cardiac telemetry with serial 6-hourly ionized calcium checks."

        return jsonify({
            "probability": round(probability, 4),
            "probability_percentage": probability_pct,
            "risk_tier": risk_tier,
            "tier_code": tier_code,
            "discharge_pathway": discharge_pathway,
            "calcium_regimen": calcium_regimen,
            "monitoring_protocol": monitoring_protocol,
            "inputs_received": {
                "CA": ca, "PHOSPHORUS": phos, "PTH": pth, "ALP": alp,
                "VIT_D": vit_d, "POST_OP_PTH": post_op_pth,
                "NO_OF_TUMOURS": no_of_tumours, "BMD_N": bmd_n
            }
        })

    except Exception as e:
        return jsonify({"detail": f"Calculation error: {str(e)}"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
