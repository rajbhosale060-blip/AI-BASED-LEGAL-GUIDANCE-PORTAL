"""
AI-Based Legal Aid and Case Guidance Portal
Flask Application — Main Entry Point
"""
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3, os, hashlib, random, string, json
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.utils import secure_filename

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from twilio.rest import Client as TwilioClient
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN  = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_PHONE       = os.getenv('TWILIO_PHONE')
    TWILIO_AVAILABLE   = bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE)
except ImportError:
    TWILIO_AVAILABLE = False

from models.nlp_processor import process_chat_query, analyze_case, analyze_bail
from models.maharashtra_police_directory import get_district_info, get_all_districts
from models.legal_reference import get_legal_acts, search_legal_acts

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'legal_aid_secret_2024_india')

# Production session settings
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

UPLOAD_FOLDER    = os.path.join('static', 'uploads')
ALLOWED_EXT      = {'png','jpg','jpeg','gif','pdf','mp4','avi','mov','doc','docx','txt'}
app.config['UPLOAD_FOLDER']        = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']   = 50 * 1024 * 1024
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# On Render, the filesystem is ephemeral — use /tmp for writable SQLite.
# Locally (Windows / dev), use the project directory.
if os.getenv('RENDER'):
    DB_PATH = '/tmp/database.db'
else:
    DB_PATH = 'database.db'

# ── DB helpers ─────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS criminal_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            severity TEXT NOT NULL CHECK(severity IN ("Serious","Minor","Clean")),
            case_details TEXT
        );
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            case_type TEXT,
            legal_area TEXT,
            keywords TEXT,
            severity TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS evidence_uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            original_name TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_type TEXT NOT NULL,
            file_size INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS otp_store (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mobile TEXT NOT NULL,
            otp_code TEXT NOT NULL,
            expires_at TEXT NOT NULL
        );
        ''')
        if db.execute('SELECT COUNT(*) FROM criminal_records').fetchone()[0] == 0:
            db.executemany(
                'INSERT INTO criminal_records (name,severity,case_details) VALUES (?,?,?)',
                [
                    ('Dawood Ibrahim','Serious','Organized crime, terrorism'),
                    ('Chhota Shakeel','Serious','Organized crime, extortion'),
                    ('Ram Kumar Sharma','Minor','Minor theft 2018'),
                    ('Priya Singh','Clean','No criminal record'),
                ]
            )
        db.commit()

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()
def gen_otp():   return ''.join(random.choices(string.digits, k=6))
def allowed(fn): return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED_EXT

def send_otp(mobile, otp):
    if TWILIO_AVAILABLE:
        try:
            TwilioClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN).messages.create(
                body=f"Legal Aid Portal OTP: {otp} (valid 10 min)",
                from_=TWILIO_PHONE, to=f"+91{mobile}")
            return "OTP sent via SMS."
        except Exception as e:
            print(f"Twilio error: {e}")
            return "Failed to send OTP via SMS. Check server console for Twilio errors."
    print(f"\n{'='*45}\n  DEMO OTP for {mobile}: {otp}\n{'='*45}\n")
    return f"DEMO MODE — OTP is <strong>{otp}</strong> (check server console too)"

def login_required(f):
    @wraps(f)
    def wrap(*a, **kw):
        if 'user_id' not in session:
            flash('Please login first.', 'warning')
            return redirect(url_for('login'))
        return f(*a, **kw)
    return wrap

# ── Auth Routes ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return redirect(url_for('dashboard') if 'user_id' in session else url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name   = request.form.get('name','').strip()
        mobile = request.form.get('mobile','').strip()
        email  = request.form.get('email','').strip().lower()
        pw     = request.form.get('password','')

        if not all([name, mobile, email, pw]):
            flash('All fields are required.', 'danger'); return render_template('register.html')
        if len(mobile) != 10 or not mobile.isdigit():
            flash('Enter valid 10-digit mobile.', 'danger'); return render_template('register.html')
        if len(pw) < 6:
            flash('Password must be at least 6 characters.', 'danger'); return render_template('register.html')

        db = get_db()
        if db.execute("SELECT id FROM criminal_records WHERE LOWER(name) LIKE ? AND severity='Serious'",
                      (f'%{name.lower()}%',)).fetchone():
            flash('⛔ Registration blocked — name found in serious criminal records.', 'danger')
            return render_template('register.html')

        if db.execute('SELECT id FROM users WHERE mobile=? OR email=?', (mobile,email)).fetchone():
            flash('Mobile or email already registered.', 'danger'); return render_template('register.html')

        db.execute('INSERT INTO users (name,mobile,email,password_hash,verified) VALUES (?,?,?,?,1)',
                   (name, mobile, email, hash_pw(pw)))
        db.commit()
        flash('✅ Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if 'user_id' in session: return redirect(url_for('dashboard'))
    if request.method == 'POST':
        identifier = request.form.get('email','').strip().lower()
        pw = request.form.get('password','')
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE (email=? OR mobile=?) AND password_hash=? AND verified=1',
            (identifier, identifier, hash_pw(pw))).fetchone()
        if not user:
            flash('Invalid credentials or account not verified.','danger')
            return render_template('login.html')
        session['user_id']   = user['id']
        session['user_name'] = user['name']
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.','info')
    return redirect(url_for('login'))

# ── Core Pages ─────────────────────────────────────────────────────────────────
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    cases = db.execute(
        'SELECT case_type,severity,created_at FROM cases WHERE user_id=? ORDER BY created_at DESC LIMIT 10',
        (session['user_id'],)).fetchall()
    ct_counts = {}
    sv_counts = {'High':0,'Medium':0,'Low':0}
    for c in cases:
        ct = c['case_type'] or 'Unknown'
        ct_counts[ct] = ct_counts.get(ct,0)+1
        sv = c['severity'] or 'Low'
        if sv in sv_counts: sv_counts[sv] += 1
    ev_count = db.execute('SELECT COUNT(*) FROM evidence_uploads WHERE user_id=?',(session['user_id'],)).fetchone()[0]
    return render_template('dashboard.html',
        cases=cases, ct_counts=json.dumps(ct_counts),
        sv_counts=json.dumps(sv_counts),
        total_cases=len(cases), ev_count=ev_count)

@app.route('/chatbot')
@login_required
def chatbot():
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.get_json()
    msg  = (data or {}).get('message','').strip()
    if not msg: return jsonify({'error':'Empty message'}), 400

    # Get conversation history from session
    history = session.get('chat_history', [])

    result = process_chat_query(msg, language='auto', history=history)

    # Save to conversation history (keep last 20 exchanges)
    if not result.get('blocked'):
        history.append({'role': 'user', 'text': msg})
        history.append({'role': 'model', 'text': result.get('response', '')})
        session['chat_history'] = history[-40:]  # 20 exchanges = 40 messages

    return jsonify(result)

@app.route('/api/chat/clear', methods=['POST'])
@login_required
def api_chat_clear():
    session.pop('chat_history', None)
    return jsonify({'status': 'ok', 'message': 'Conversation cleared'})

@app.route('/case-analyzer')
@login_required
def case_analyzer():
    db = get_db()
    past = db.execute('SELECT * FROM cases WHERE user_id=? ORDER BY created_at DESC LIMIT 5',(session['user_id'],)).fetchall()
    return render_template('case_analyzer.html', past_cases=past)

@app.route('/bail-checker')
@login_required
def bail_checker():
    return render_template('bail_checker.html')

@app.route('/api/analyze-bail', methods=['POST'])
@login_required
def api_analyze_bail():
    data = request.get_json()
    if not data: return jsonify({'error': 'No data provided'}), 400
    
    result = analyze_bail({
        'summary': data.get('summary', ''),
        'sections': data.get('sections', ''),
        'nature': data.get('nature', ''),
        'evidence': data.get('evidence', ''),
        'record': data.get('record', ''),
        'arrest_status': data.get('arrest_status', '')
    })
    return jsonify(result)

@app.route('/api/analyze-case', methods=['POST'])
@login_required
def api_analyze_case():
    data = request.get_json()
    desc = (data or {}).get('description','').strip()
    if len(desc) < 20: return jsonify({'error':'Provide at least 20 characters.'}), 400
    result = analyze_case(desc)
    db = get_db()
    db.execute('INSERT INTO cases (user_id,description,case_type,legal_area,keywords,severity) VALUES (?,?,?,?,?,?)',
               (session['user_id'], desc, result['case_type'], result['legal_area'],
                ','.join(result['keywords']), result['severity']))
    db.commit()
    return jsonify(result)

@app.route('/evidence', methods=['GET','POST'])
@login_required
def evidence():
    db = get_db()
    if request.method == 'POST':
        f = request.files.get('file')
        if not f or f.filename == '':
            flash('No file selected.','danger'); return redirect(url_for('evidence'))
        if allowed(f.filename):
            orig = f.filename
            ext  = orig.rsplit('.',1)[1].lower()
            fname= f"{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(orig)}"
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            f.save(path)
            ftype = 'image' if ext in {'png','jpg','jpeg','gif'} else \
                    'pdf'   if ext == 'pdf' else \
                    'video' if ext in {'mp4','avi','mov'} else 'document'
            db.execute('INSERT INTO evidence_uploads (user_id,original_name,filename,file_type,file_size) VALUES (?,?,?,?,?)',
                       (session['user_id'], orig, fname, ftype, os.path.getsize(path)))
            db.commit()
            flash('✅ Evidence uploaded successfully!','success')
        else:
            flash('Invalid file type.','danger')
        return redirect(url_for('evidence'))
    uploads = db.execute('SELECT * FROM evidence_uploads WHERE user_id=? ORDER BY uploaded_at DESC',(session['user_id'],)).fetchall()
    return render_template('evidence.html', uploads=uploads)

@app.route('/legal-aid')
@login_required
def legal_aid():
    return render_template('legal_aid.html')

@app.route('/legal-acts')
@login_required
def legal_acts():
    return render_template('legal_acts.html', acts=get_legal_acts())

@app.route('/api/search-acts')
@login_required
def api_search_acts():
    return jsonify(search_legal_acts(request.args.get('q','')))

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')

@app.route('/map')
@login_required
def map_page():
    return render_template('map.html', districts=get_all_districts())

@app.route('/api/district-info')
@login_required
def api_district_info():
    return jsonify(get_district_info(request.args.get('district','')))

@app.route('/interactive-map')
@login_required
def interactive_map():
    return render_template('interactive_map.html')

@app.route('/video-assistant')
@login_required
def video_assistant():
    return render_template('video_assistant.html')

# ── Initialize DB at import time (required for gunicorn / Render) ──────────────
init_db()

# ── Run (local development only — Render uses gunicorn via Procfile) ───────────
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("\n" + "="*55)
    print(f"  AI Legal Aid Portal  |  http://localhost:{port}")
    print("="*55 + "\n")
    app.run(debug=True, host='0.0.0.0', port=port)
