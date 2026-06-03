"""
NLP Processor — Gemini AI-powered legal assistant with rule-based fallback
"""
import re
import os
import random
import time
import json

# ── Gemini API Setup ───────────────────────────────────────────────────────────
GEMINI_AVAILABLE = False
gemini_model = None

try:
    from google import genai
    from google.genai import types

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_gemini_api_key_here":
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        gemini_config = types.GenerateContentConfig(
            system_instruction=(
                "You are an expert AI Legal Aid Assistant for Indian citizens. "
                "Your STRICT AND ONLY role is to provide accurate, helpful legal guidance based on "
                "Indian law (e.g., IPC, CrPC, CPC, Constitution of India, IT Act, POCSO, DV Act, etc.).\n\n"
                "CRITICAL GUARDRAIL: You MUST ONLY answer questions related to law, crime, legal procedures, "
                "rights, and justice. If a user asks about ANYTHING else (e.g., coding, math, general knowledge, "
                "weather, small talk), you MUST firmly refuse and state: 'I am a legal aid assistant and can only "
                "answer questions related to Indian law and legal procedures.'\n\n"
                "RULES:\n"
                "1. Always cite specific legal sections (e.g., Section 154 CrPC, Article 21).\n"
                "2. Respond in the SAME LANGUAGE the user writes in.\n"
                "3. Be empathetic and supportive.\n"
                "4. Always include emergency helpline numbers when relevant: Police: 100, Women: 1091, Cyber: 1930, NALSA: 15100.\n"
                "5. Add a disclaimer that this is legal awareness, not professional advice.\n"
                "6. NEVER help with illegal activities — refuse clearly if asked.\n"
                "7. Use markdown formatting with bold, bullet points, and emojis for clarity.\n"
                "8. Keep responses concise but thorough (under 400 words)."
            ),
            temperature=0.7,
            max_output_tokens=1024,
            top_p=0.95,
        )
        GEMINI_AVAILABLE = True
        print("Gemini API configured successfully (model: gemini-2.0-flash, using google.genai)")
    else:
        print("Warning: GEMINI_API_KEY not set — using rule-based engine only")
except ImportError:
    print("Warning: google-genai not installed — using rule-based engine only")
except Exception as e:
    print(f"Warning: Gemini setup error: {e} — using rule-based engine only")


# ── Harmful Query Detection ────────────────────────────────────────────────────
HARMFUL_KEYWORDS = [
    "hide evidence", "destroy evidence", "burn evidence", "delete evidence",
    "escape police", "run from police", "avoid arrest", "flee from law",
    "bribe police", "pay bribe", "corruption help", "fake alibi",
    "threaten witness", "kill witness", "murder", "how to kill",
    "plant evidence", "frame someone", "fake case against"
]

HARMFUL_RESPONSE = (
    "🚫 **I cannot assist with this request.**\n\n"
    "This platform is designed to help citizens understand their **legal rights**. "
    "It does not support any request that involves illegal acts.\n\n"
    "⚖️ Such actions are criminal offences under the Indian Penal Code.\n\n"
    "If you are in genuine legal trouble, please contact:\n"
    "- 📞 NALSA (Free Legal Aid): **15100**\n"
    "- 📞 Police Helpline: **100**"
)


def is_harmful(query):
    q = query.lower()
    return any(kw in q for kw in HARMFUL_KEYWORDS)


# ── Gemini AI Chat ─────────────────────────────────────────────────────────────
def _gemini_chat(query, history=None):
    """Send query to Gemini API with conversation history."""
    if not GEMINI_AVAILABLE or not gemini_client:
        return None

    try:
        # Build conversation history for context
        gemini_history = []
        if history:
            for msg in history[-20:]:  # Last 10 exchanges
                role = "user" if msg.get("role") == "user" else "model"
                gemini_history.append(types.Content(role=role, parts=[types.Part.from_text(text=msg.get("text", ""))]))

        # Start chat with history - attempt primary model
        try:
            chat = gemini_client.chats.create(
                model="gemini-2.0-flash",
                config=gemini_config,
                history=gemini_history
            )
            response = chat.send_message(query)
        except Exception as api_err:
            if "429" in str(api_err) or "RESOURCE_EXHAUSTED" in str(api_err):
                return {"error": "quota_exceeded"}
            raise api_err

        if response and response.text:
            # Extract legal sections from the response
            sections = _extract_legal_sections(response.text)
            return {
                "intent": "ai_response",
                "response": response.text,
                "legal_sections": sections,
                "severity": "info",
                "blocked": False,
                "source": "gemini",
            }
    except Exception as e:
        print(f"Warning: Gemini API error: {e}")
        return None

    return None


# ── Main Chat Entry Point ─────────────────────────────────────────────────────
def process_chat_query(query, language="auto", history=None):
    """Main chatbot function — Gemini AI primary, rule-based fallback."""
    # Step 1: Block harmful queries (always, before any AI call)
    if is_harmful(query):
        return {
            "intent": "harmful",
            "response": HARMFUL_RESPONSE,
            "legal_sections": [],
            "severity": "danger",
            "blocked": True,
        }

    # Step 2: Try Gemini AI (primary)
    quota_exceeded = False
    if GEMINI_AVAILABLE:
        ai_result = _gemini_chat(query, history)
        if ai_result:
            if ai_result.get("error") == "quota_exceeded":
                quota_exceeded = True
            else:
                return ai_result

    # Step 3: Fall back to rule-based engine
    result = _rule_based_response(query)
    
    if quota_exceeded:
        if result["intent"] == "unknown":
            # Rule engine doesn't know the answer
            result["response"] = "⚠️ **Google Gemini API Quota Exceeded**\n\nThe AI model has reached its free-tier rate limit. Please wait a short while before trying again, or upgrade your API key.\n\n*Note: Our built-in rule engine is still active. You can ask about basic topics like FIRs, Bail, and Arrest Rights.*"
            result["severity"] = "warning"
        else:
            # Rule engine knows the answer! Prepend warning.
            result["response"] = "⚠️ *Note: AI Quota Exceeded. Answering from built-in legal rules:*\n\n" + result["response"]

    return result


def _extract_legal_sections(text):
    """Extract legal section references from response text."""
    patterns = [
        r"(?:Section|Sec\.?|S\.?)\s*\d+[A-Za-z]?\s*(?:of\s+)?(?:CrPC|IPC|CPC|IT Act|Constitution)",
        r"Article\s+\d+[A-Za-z]?\s*(?:\(\d+\))?",
        r"(?:IPC|CrPC|CPC)\s+(?:Section|Sec\.?)\s*\d+[A-Za-z]?",
        r"(?:POCSO|DV|IT)\s+Act\s*(?:\d{4})?",
        r"धारा\s+\d+",
        r"अनुच्छेद\s+\d+",
        r"कलम\s+\d+",
    ]
    found = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found.extend(matches)
    seen = set()
    unique = []
    for s in found:
        s_clean = s.strip()
        if s_clean.lower() not in seen:
            seen.add(s_clean.lower())
            unique.append(s_clean)
    return unique[:10]


# ── Rule-Based Fallback ────────────────────────────────────────────────────────
INTENT_PATTERNS = {
    "fir_filing": {
        "keywords": ["fir", "first information report", "file complaint", "police complaint", "register case", "file fir", "दर्ज"],
        "response": (
            "📋 **How to File an FIR in India**\n\n"
            "Under **Section 154 CrPC**, every police station MUST register your FIR — it is your right!\n\n"
            "**Steps to File an FIR:**\n"
            "1. Visit the nearest police station with jurisdiction over the crime area.\n"
            "2. Narrate the incident clearly to the duty officer.\n"
            "3. The officer must write it down and read it back to you.\n"
            "4. Sign the FIR and demand a FREE copy.\n\n"
            "📞 Police: **100** | Women: **1091**"
        ),
        "legal_sections": ["Section 154 CrPC", "Section 156(3) CrPC"],
        "severity": "info"
    },
    "arrest_rights": {
        "keywords": ["arrest", "arrested", "police detained", "custody", "taken by police", "गिरफ्तार", "हिरासत"],
        "response": (
            "⚖️ **Your Rights During Arrest**\n\n"
            "1. **Right to know the reason** (Article 22).\n"
            "2. **Right to remain silent**.\n"
            "3. **Right to a lawyer**.\n"
            "4. **Produced before Magistrate** within 24 hours (Section 57 CrPC).\n"
            "5. **Right to inform family**.\n\n"
            "📞 NALSA Free Legal Aid: **15100**"
        ),
        "legal_sections": ["Article 22 Constitution", "Section 57 CrPC"],
        "severity": "warning"
    },
    "bail": {
        "keywords": ["bail", "bailable", "non bailable", "anticipatory bail", "जमानत", "surety"],
        "response": (
            "🔓 **Understanding Bail in India**\n\n"
            "- **Regular Bail (Section 437/439 CrPC)**: Applied for after arrest.\n"
            "- **Anticipatory Bail (Section 438 CrPC)**: Applied for before arrest when there is apprehension of arrest.\n"
            "- **Bailable Offence (Section 436 CrPC)**: Bail is a matter of right.\n\n"
            "📞 NALSA Free Legal Aid: **15100**"
        ),
        "legal_sections": ["Section 437 CrPC", "Section 438 CrPC", "Section 436 CrPC"],
        "severity": "info"
    },
    "cyber_crime": {
        "keywords": ["cyber", "online fraud", "scam", "phishing", "hacked", "internet", "साइबर", "धोखाधड़ी", "otp"],
        "response": (
            "💻 **Reporting Cyber Crime & Online Fraud**\n\n"
            "If you are a victim of financial fraud, hacking, or online harassment:\n"
            "1. **Immediately call 1930** (National Cyber Crime Helpline).\n"
            "2. Register a complaint at **cybercrime.gov.in**.\n"
            "3. Inform your bank immediately to block affected cards/accounts.\n\n"
            "Laws applicable include the **Information Technology (IT) Act, 2000** (e.g., Section 66C, 66D)."
        ),
        "legal_sections": ["IT Act 2000"],
        "severity": "warning"
    },
    "domestic_violence": {
        "keywords": ["domestic violence", "husband beating", "dowry", "harassment", "घरेलू हिंसा", "दहेज", "wife", "women safety"],
        "response": (
            "👩 **Protection from Domestic Violence**\n\n"
            "You have the right to live a life free from violence. Protection is available under:\n"
            "- **Protection of Women from Domestic Violence Act (PWDVA), 2005**\n"
            "- **Section 498A IPC** (Cruelty by husband or relatives)\n\n"
            "**Immediate Steps:**\n"
            "1. Call the Women Helpline: **1091** or **181**.\n"
            "2. You can file a complaint with the nearest police station or Protection Officer.\n\n"
            "📞 Emergency Police: **100** or **112**"
        ),
        "legal_sections": ["DV Act 2005", "Section 498A IPC"],
        "severity": "danger"
    },
    "free_legal_aid": {
        "keywords": ["free lawyer", "legal aid", "can't afford lawyer", "nalsa", "मुफ्त वकील", "कानूनी सहायता", "poor"],
        "response": (
            "🏛️ **Free Legal Aid Services (NALSA)**\n\n"
            "Under **Article 39A** of the Constitution and the **Legal Services Authorities Act**, free legal aid is provided to:\n"
            "- Women and children\n"
            "- Members of SC/ST\n"
            "- Victims of human trafficking or disaster\n"
            "- Persons with low income (varies by state, generally < ₹3,00,000 p.a.)\n\n"
            "**How to apply:**\n"
            "Call the NALSA Helpline at **15100** or visit your district court's legal services clinic."
        ),
        "legal_sections": ["Article 39A Constitution", "Legal Services Authorities Act"],
        "severity": "info"
    },
    "consumer_rights": {
        "keywords": ["consumer", "defective", "refund", "shop", "e-commerce", "उपभोक्ता", "खराब", "गारंटी"],
        "response": (
            "🛒 **Consumer Protection Rights**\n\n"
            "Under the **Consumer Protection Act, 2019**, you are protected against defective goods and deficient services.\n\n"
            "**How to file a complaint:**\n"
            "1. Call the National Consumer Helpline (NCH): **1915** or **1800-11-4000**.\n"
            "2. Register online at **edaakhil.nic.in** or the NCH App.\n"
            "3. Issue a legal notice to the seller before approaching the Consumer Court."
        ),
        "legal_sections": ["Consumer Protection Act 2019"],
        "severity": "info"
    },
    "hindi_help": {
        "keywords": ["मुझे कानूनी सहायता चाहिए", "hindi", "हिंदी"],
        "response": (
            "🙏 **नमस्ते! लीगल एड AI असिस्टेंट में आपका स्वागत है।**\n\n"
            "मैं आपको एफआईआर (FIR), जमानत (Bail), गिरफ्तारी के अधिकार, और मुफ्त कानूनी सहायता (NALSA) जैसी सामान्य कानूनी जानकारी दे सकता हूँ। आप अपना सवाल हिंदी में पूछ सकते हैं।\n\n"
            "📞 **आपातकालीन हेल्पलाइन:**\n"
            "- पुलिस: **100**\n"
            "- महिला हेल्पलाइन: **1091**\n"
            "- मुफ्त कानूनी सहायता: **15100**"
        ),
        "legal_sections": [],
        "severity": "info"
    },
    "marathi_help": {
        "keywords": ["मला कायदेशीर मदत हवी आहे", "marathi", "मराठी"],
        "response": (
            "🙏 **नमस्कार! लीगल एड AI असिस्टंट मध्ये आपले स्वागत आहे।**\n\n"
            "मी तुम्हाला एफआयआर (FIR), जामीन (Bail), अटकेचे अधिकार आणि मोफत कायदेशीर मदत यांसारखी सामान्य कायदेशीर माहिती देऊ शकतो. तुम्ही तुमचा प्रश्न मराठीत विचारू शकता.\n\n"
            "📞 **इमर्जन्सी हेल्पलाइन:**\n"
            "- पोलीस: **100**\n"
            "- महिला हेल्पलाइन: **1091**\n"
            "- मोफत कायदेशीर मदत (NALSA): **15100**"
        ),
        "legal_sections": [],
        "severity": "info"
    },
}

GREETINGS = ["hello", "hi", "namaste", "namaskar", "नमस्ते", "hey", "good morning", "good evening"]

GREETING_RESPONSE = (
    "🙏 **Namaste! Welcome to the Legal Aid AI Assistant.**\n\n"
    "I can help you with **any question** in any language!\n\n"
    "📞 Emergency? Call **100** (Police) | **15100** (Free Legal Aid)"
)

DEFAULT_RESPONSE = (
    "🤔 **I can help with common legal topics.**\n\n"
    "I can help with topics like FIR, arrest rights, bail, and legal aid.\n\n"
    "📞 For immediate help: **100** (Police) | **15100** (Free Legal Aid)"
)


def _rule_based_response(query):
    q_lower = query.lower()
    if any(g in q_lower for g in GREETINGS):
        return {"intent": "greeting", "response": GREETING_RESPONSE, "legal_sections": [], "severity": "info", "blocked": False}
    best_intent = None
    best_score = 0
    for intent, data in INTENT_PATTERNS.items():
        score = sum(1 for kw in data["keywords"] if kw in q_lower)
        if score > best_score:
            best_score = score
            best_intent = intent
    if best_intent and best_score > 0:
        data = INTENT_PATTERNS[best_intent]
        return {"intent": best_intent, "response": data["response"], "legal_sections": data["legal_sections"], "severity": data["severity"], "blocked": False}
    return {"intent": "unknown", "response": DEFAULT_RESPONSE, "legal_sections": [], "severity": "info", "blocked": False}


# ── Case Analyzer (unchanged) ─────────────────────────────────────────────────
CASE_PATTERNS = {
    "Theft / Robbery": {"keywords": ["steal", "stolen", "theft", "rob", "चोरी"], "legal_area": "Criminal Law — IPC", "sections": ["IPC Section 379"], "advice": "File an FIR immediately."},
    "Domestic Violence": {"keywords": ["husband", "wife", "beat", "torture", "घरेलू हिंसा"], "legal_area": "Family Law", "sections": ["IPC Section 498A", "DV Act 2005"], "advice": "Contact Women Helpline 181."},
    "Cyber Crime": {"keywords": ["online fraud", "hack", "phishing", "scam"], "legal_area": "Cyber Law", "sections": ["IT Act 2000"], "advice": "Call 1930 immediately."},
}

def analyze_case(description):
    desc_lower = description.lower()
    best_type = None
    best_score = 0
    for case_type, data in CASE_PATTERNS.items():
        score = sum(1 for kw in data["keywords"] if kw in desc_lower)
        if score > best_score: best_score = score; best_type = case_type
    severity = "High" if any(w in desc_lower for w in ["murder", "rape", "kill"]) else "Low"
    if best_type:
        data = CASE_PATTERNS[best_type]
        return {"case_type": best_type, "legal_area": data["legal_area"], "relevant_sections": data["sections"], "keywords": [], "severity": severity, "advice": data["advice"], "word_count": len(description.split())}
    return {"case_type": "General Legal Matter", "legal_area": "Needs Review", "relevant_sections": [], "keywords": [], "severity": severity, "advice": "Contact NALSA at 15100.", "word_count": len(description.split())}


def _clean_json_response(text):
    """Clean markdown code blocks and extra text from JSON response."""
    text = re.sub(r"```json\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"```\s*", "", text)
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return text[start:end+1]
    return text.strip()


# ── IPC Section Database for Bail Classification ──────────────────────────────
# Non-bailable offences (serious crimes — bail is at court's discretion)
NON_BAILABLE_SECTIONS = {
    '302': 'Murder — Punishable with death or life imprisonment',
    '304': 'Culpable homicide not amounting to murder',
    '307': 'Attempt to murder',
    '376': 'Rape',
    '395': 'Dacoity',
    '396': 'Dacoity with murder',
    '397': 'Robbery/Dacoity with attempt to cause death',
    '398': 'Attempt to commit robbery/dacoity when armed',
    '364': 'Kidnapping for ransom',
    '364A': 'Kidnapping for ransom',
    '392': 'Punishment for robbery',
    '394': 'Voluntarily causing hurt in committing robbery',
    '399': 'Making preparation to commit dacoity',
    '400': 'Punishment for belonging to a gang of dacoits',
    '489A': 'Counterfeiting currency notes',
    '489B': 'Using forged currency',
    '489C': 'Possession of forged currency',
    '120B': 'Criminal conspiracy (if for serious offence)',
    '121': 'Waging war against the Government of India',
    '124A': 'Sedition',
    '326': 'Voluntarily causing grievous hurt by dangerous weapons',
    '304B': 'Dowry death',
}

# Bailable offences (bail is a matter of right)
BAILABLE_SECTIONS = {
    '379': 'Theft',
    '380': 'Theft in dwelling house',
    '403': 'Dishonest misappropriation of property',
    '406': 'Criminal breach of trust',
    '417': 'Cheating',
    '420': 'Cheating and dishonestly inducing delivery of property',
    '468': 'Forgery for purpose of cheating',
    '471': 'Using as genuine a forged document',
    '494': 'Bigamy',
    '498A': 'Husband or relative subjecting woman to cruelty',
    '500': 'Defamation',
    '504': 'Intentional insult with intent to provoke breach of peace',
    '506': 'Criminal intimidation',
    '509': 'Word, gesture or act intended to insult modesty of a woman',
    '323': 'Voluntarily causing hurt',
    '341': 'Wrongful restraint',
    '352': 'Assault (not on grave provocation)',
    '447': 'Criminal trespass',
    '448': 'House-trespass',
    '354': 'Assault on woman with intent to outrage her modesty',
}

# Keywords indicating violent / serious crimes
SERIOUS_KEYWORDS = [
    'murder', 'kill', 'rape', 'sexual assault', 'dacoity', 'kidnap',
    'ransom', 'terrorism', 'waging war', 'sedition', 'arms', 'explosive',
    'acid attack', 'dowry death', 'हत्या', 'बलात्कार', 'अपहरण'
]

PROPERTY_KEYWORDS = [
    'theft', 'stolen', 'cheating', 'fraud', 'money', 'property',
    'land dispute', 'financial', 'misappropriation', 'breach of trust',
    'चोरी', 'धोखा', 'जालसाज़ी'
]


def _rule_based_bail_analysis(case_data):
    """Comprehensive rule-based bail eligibility analysis using IPC knowledge."""
    import json as _json

    summary_text = (case_data.get('summary') or '').lower()
    sections_text = (case_data.get('sections') or '').upper()
    nature_text = (case_data.get('nature') or '').lower()
    evidence = (case_data.get('evidence') or 'moderate').lower()
    record = (case_data.get('record') or 'no').lower()
    arrest_status = (case_data.get('arrest_status') or 'not arrested').lower()

    # ── 1. Parse Section Numbers ──────────────────────────────────────────
    section_nums = re.findall(r'\d+[A-Za-z]?', sections_text)
    
    found_non_bailable = {}
    found_bailable = {}
    for sec in section_nums:
        sec_clean = sec.upper()
        if sec_clean in NON_BAILABLE_SECTIONS:
            found_non_bailable[sec_clean] = NON_BAILABLE_SECTIONS[sec_clean]
        elif sec_clean in BAILABLE_SECTIONS:
            found_bailable[sec_clean] = BAILABLE_SECTIONS[sec_clean]

    # ── 2. Keyword Severity Check ─────────────────────────────────────────
    is_serious = any(kw in summary_text or kw in nature_text for kw in SERIOUS_KEYWORDS)
    is_property = any(kw in summary_text or kw in nature_text for kw in PROPERTY_KEYWORDS)

    # ── 3. Calculate Risk Score (0-100) ───────────────────────────────────
    risk_score = 30  # baseline

    if found_non_bailable:
        risk_score += 35
    if is_serious:
        risk_score += 20
    if found_bailable and not found_non_bailable:
        risk_score -= 25
    if is_property and not is_serious:
        risk_score -= 10

    # Evidence factor
    if evidence == 'strong':
        risk_score += 15
    elif evidence == 'weak':
        risk_score -= 10

    # Prior record factor
    if record == 'yes':
        risk_score += 15

    # Arrest status factor
    if arrest_status == 'arrested':
        risk_score += 5
    elif 'interim' in arrest_status:
        risk_score += 10

    risk_score = max(5, min(95, risk_score))

    # ── 4. Determine Bail Status ──────────────────────────────────────────
    if found_non_bailable:
        if risk_score >= 70:
            bail_status = "Difficult — Non-bailable offence, court discretion required"
        else:
            bail_status = "Possible with strong legal representation — Non-bailable offence"
    elif found_bailable:
        bail_status = "Bailable as a matter of right under Section 436 CrPC"
    elif is_serious:
        bail_status = "Likely non-bailable — Serious offence detected in case summary"
    elif is_property:
        bail_status = "High chance of bail — Property/financial offence, generally bailable"
    else:
        bail_status = "Needs case-specific legal review"

    # Arrest-status-based recommendation
    if 'not arrested' in arrest_status and found_non_bailable:
        bail_status = "Anticipatory Bail recommended under Section 438 CrPC"
    elif 'interim' in arrest_status:
        bail_status = "Interim Bail / Transit Anticipatory Bail recommended"

    # ── 5. Risk Level ─────────────────────────────────────────────────────
    if risk_score >= 65:
        risk_level = "High"
    elif risk_score >= 35:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    # ── 6. Build Sections String ──────────────────────────────────────────
    sections_parts = []
    if found_non_bailable:
        sections_parts.append("Non-Bailable: " + ", ".join(
            f"IPC {s} ({d})" for s, d in found_non_bailable.items()
        ))
    if found_bailable:
        sections_parts.append("Bailable: " + ", ".join(
            f"IPC {s} ({d})" for s, d in found_bailable.items()
        ))

    # Always add relevant CrPC bail sections
    crpc_sections = []
    if found_bailable and not found_non_bailable:
        crpc_sections.append("Section 436 CrPC (Bail in bailable offences)")
    if found_non_bailable:
        crpc_sections.append("Section 437 CrPC (Bail in non-bailable offences)")
    if 'not arrested' in arrest_status:
        crpc_sections.append("Section 438 CrPC (Anticipatory Bail)")
    crpc_sections.append("Section 439 CrPC (Special powers of High Court/Sessions Court)")
    sections_parts.append("Bail Provisions: " + ", ".join(crpc_sections))

    sections_str = " | ".join(sections_parts) if sections_parts else f"Sections {sections_text} — Refer to CrPC Sections 436-439 for bail provisions."

    # ── 7. Build Summary ──────────────────────────────────────────────────
    severity_word = "serious" if is_serious or found_non_bailable else "moderate" if risk_score > 40 else "low-severity"
    summary = (
        f"This is a {severity_word} case"
        + (f" involving IPC Sections {', '.join(section_nums)}" if section_nums else "")
        + f". Nature: {nature_text.title() if nature_text else 'Not specified'}."
        + f" Evidence strength is assessed as {evidence}."
        + (f" Accused has prior criminal record, which significantly impacts bail chances." if record == 'yes' else " No prior criminal record, which is favorable for bail.")
        + f" Current status: {arrest_status.title()}."
    )

    # ── 8. Build Action Steps ─────────────────────────────────────────────
    actions = []
    if 'not arrested' in arrest_status and (found_non_bailable or is_serious):
        actions.append("<li><strong>Immediate Step:</strong> File an Anticipatory Bail application under Section 438 CrPC immediately before the concerned Sessions Court or High Court.</li>")
        actions.append("<li><strong>Legal Counsel:</strong> Engage an experienced criminal defense lawyer without delay.</li>")
        actions.append("<li><strong>Documentation:</strong> Prepare surety documents, identity proof, and address proof in advance.</li>")
        actions.append("<li><strong>Caution:</strong> Do not tamper with any evidence or contact witnesses.</li>")
    elif 'arrested' in arrest_status:
        actions.append("<li><strong>Immediate Step:</strong> Apply for Regular Bail under Section 437/439 CrPC before the Magistrate or Sessions Court.</li>")
        actions.append("<li><strong>Appeal:</strong> If denied, file an appeal to the High Court under Section 439 CrPC.</li>")
        actions.append("<li><strong>Visitation:</strong> Ensure a family member or advocate visits the accused within 24 hours.</li>")
        actions.append("<li><strong>Medical:</strong> Request a medical examination under Section 54 CrPC if there are signs of injury.</li>")
    elif 'interim' in arrest_status:
        actions.append("<li><strong>Immediate Step:</strong> Apply for Transit/Interim Anticipatory Bail immediately to prevent immediate arrest.</li>")
        actions.append("<li><strong>Preparation:</strong> Simultaneously prepare a comprehensive Anticipatory Bail application.</li>")
        actions.append("<li><strong>Documentation:</strong> Keep all supporting documents ready — employment proof, address proof, medical certificates if applicable.</li>")
    else:
        actions.append("<li><strong>Counsel:</strong> Consult a lawyer to evaluate the strength of the case against you.</li>")
        actions.append("<li><strong>Right to Bail:</strong> If bailable, assert your right to bail under Section 436 CrPC immediately at the police station.</li>")
        actions.append("<li><strong>Cooperation:</strong> Cooperate fully with the investigation while exercising your legal rights.</li>")

    actions.append(f"<li style='list-style-type: none; margin-top: 10px; font-weight: bold;'>📞 Contact NALSA (Free Legal Aid): 15100 | Police Helpline: 100 | Emergency: 112</li>")
    action_str = "<ul style='padding-left: 1.2rem; margin-bottom: 0;'>" + "".join(actions) + "</ul>"

    return {
        "summary": summary,
        "sections": sections_str,
        "status": bail_status,
        "risk": risk_level,
        "action": action_str,
        "disclaimer": "This analysis is for legal awareness only and does NOT constitute professional legal advice. Bail outcomes depend on multiple factors including specific court, judge, prosecution arguments, and case circumstances. Always consult a qualified advocate for your specific case."
    }


# ── Bail Eligibility Analyzer (Rule-based) ────────────────────────────────────
def analyze_bail(case_data):
    """
    Analyzes bail eligibility using comprehensive rule-based legal engine.
    The rule engine has a full IPC database and provides instant, reliable results.
    """
    print("Running bail analysis via rule-based legal engine")
    return _rule_based_bail_analysis(case_data)
