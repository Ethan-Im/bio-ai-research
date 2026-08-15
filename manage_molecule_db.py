import sqlite3
import json
import os

DB_NAME = "molecules_repository.db"

def init_db():
    """Initialize SQLite database table for molecular repository."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS molecules (
            id TEXT PRIMARY KEY,
            smiles TEXT NOT NULL,
            mw REAL,
            logp REAL,
            qed REAL,
            herg_risk REAL,
            dili_risk REAL,
            fitness REAL,
            admet_passed INTEGER,
            image_path TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ Database '{DB_NAME}' initialized successfully.")

def import_candidates_from_json(json_file="rdkit_multiobj_results.json"):
    """Read optimization results JSON and store molecules into SQLite DB."""
    if not os.path.exists(json_file):
        print(f"Error: JSON file '{json_file}' not found.")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    candidates = data.get("candidates", [])
    if not candidates:
        print("No candidates found in JSON file.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    inserted_count = 0
    for cand in candidates:
        cand_id = cand.get("id")
        smiles = cand.get("smiles")
        mw = cand.get("mw")
        logp = cand.get("logp")
        qed = cand.get("qed")
        herg_risk = cand.get("herg_risk")
        dili_risk = cand.get("dili_risk")
        fitness = cand.get("fitness")
        admet_passed = 1 if cand.get("admet_passed", False) else 0
        image_path = f"molecule_images/{cand_id}.png" if os.path.exists(f"molecule_images/{cand_id}.png") else None

        cursor.execute('''
            INSERT OR REPLACE INTO molecules 
            (id, smiles, mw, logp, qed, herg_risk, dili_risk, fitness, admet_passed, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cand_id, smiles, mw, logp, qed, herg_risk, dili_risk, fitness, admet_passed, image_path))
        inserted_count += 1

    conn.commit()
    conn.close()
    print(f"📥 Successfully imported/updated {inserted_count} candidate records into SQLite DB.")

def query_top_molecules(limit=5):
    """Query and display top molecules ranked by fitness score."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, smiles, mw, logp, qed, herg_risk, dili_risk, fitness, admet_passed 
        FROM molecules 
        ORDER BY fitness DESC 
        LIMIT ?
    ''', (limit,))

    rows = cursor.fetchall()
    conn.close()

    print("\n==================================================")
    print("📊 TOP CANDIDATES STORED IN DATABASE")
    print("==================================================")
    for r in rows:
        passed_str = "PASSED" if r[8] == 1 else "REJECTED"
        print(f"[{r[0]}] {r[1][:25]}... | MW: {r[2]} | LogP: {r[3]} | QED: {r[4]} | Fit: {r[7]} -> {passed_str}")
    print("==================================================\n")

if __name__ == "__main__":
    init_db()
    import_candidates_from_json()
    query_top_molecules()
