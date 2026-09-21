from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder=".")

disputes_db = {}
counter = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dispute/create", methods=["POST"])
def create_dispute():
    global counter
    data = request.json
    counter += 1
    
    dispute = {
        "id": counter,
        "claimant": data.get("claimant"),
        "respondent": data.get("respondent"),
        "details": data.get("details"),
        "status": "PENDING",
        "verdict": "Waiting for GenLayer AI Consensus..."
    }
    disputes_db[counter] = dispute
    return jsonify({"success": True, "dispute": dispute})

@app.route("/api/dispute/resolve/<int:dispute_id>", methods=["POST"])
def resolve_dispute(dispute_id):
    if dispute_id not in disputes_db:
        return jsonify({"error": "Dispute not found"}), 404
        
    dispute = disputes_db[dispute_id]
    dispute["status"] = "RESOLVED"
    dispute["verdict"] = f"AI Verdict: Claim verified in favor of {dispute['claimant']} after analyzing provided evidence."
    
    return jsonify({"success": True, "dispute": dispute})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
