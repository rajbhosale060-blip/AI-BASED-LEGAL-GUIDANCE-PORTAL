"""
Multilingual Legal Module
Basic Hindi/Marathi keyword detection and regional response support
"""

HINDI_KEYWORDS = {
    "fir": ["एफआईआर", "दर्ज", "शिकायत", "रिपोर्ट"],
    "arrest": ["गिरफ्तार", "हिरासत", "पकड़", "हवालात"],
    "bail": ["जमानत", "ज़मानत", "bail"],
    "rights": ["अधिकार", "हक़", "हक"],
    "legal_aid": ["वकील", "मुफ्त", "निःशुल्क", "कानूनी"],
    "police": ["पुलिस", "थाना", "सिपाही"],
    "domestic_violence": ["घरेलू हिंसा", "पति", "मारपीट", "दहेज"],
    "women": ["महिला", "औरत", "बलात्कार", "छेड़छाड़"],
}

MARATHI_KEYWORDS = {
    "fir": ["तक्रार", "एफआयआर", "नोंदणी", "पोलीस तक्रार"],
    "arrest": ["अटक", "कोठडी", "हिरासत"],
    "bail": ["जामीन"],
    "rights": ["हक्क", "अधिकार"],
    "legal_aid": ["विनामूल्य", "वकील", "कायदेशीर"],
    "police": ["पोलीस", "ठाणे", "पोलीस स्टेशन"],
    "domestic_violence": ["घरगुती हिंसा", "हुंडा", "मारहाण"],
    "women": ["महिला", "स्त्री", "बलात्कार"],
}

HINDI_RESPONSES = {
    "greeting": "🙏 <strong>नमस्ते! कानूनी सहायता AI में आपका स्वागत है।</strong><br>मैं आपकी कानूनी जानकारी में मदद करूँगा। कृपया अपनी समस्या बताएं।",
    "fir": "📋 <strong>FIR (प्रथम सूचना रिपोर्ट) दर्ज कराने का अधिकार</strong><br>धारा 154 CrPC के तहत, पुलिस FIR दर्ज करने से मना नहीं कर सकती।<br>📞 पुलिस हेल्पलाइन: <b>100</b>",
    "bail": "🔓 <strong>जमानत (Bail) के प्रकार</strong><br>नियमित जमानत (धारा 437 CrPC), अग्रिम जमानत (धारा 438 CrPC)।<br>📞 निःशुल्क कानूनी सहायता: <b>15100</b>",
    "legal_aid": "🏛️ <strong>निःशुल्क कानूनी सहायता</strong><br>₹1,00,000 से कम वार्षिक आय वाले NALSA से निःशुल्क वकील पा सकते हैं।<br>📞 NALSA: <b>15100</b>",
    "rights": "🇮🇳 <strong>आपके मौलिक अधिकार</strong><br>अनुच्छेद 21 — जीवन और व्यक्तिगत स्वतंत्रता का अधिकार।<br>अनुच्छेद 22 — मनमाने गिरफ्तारी से सुरक्षा।",
}

MARATHI_RESPONSES = {
    "greeting": "🙏 <strong>नमस्कार! कायदेशीर सहाय AI मध्ये आपले स्वागत आहे।</strong><br>मी तुमच्या कायदेशीर प्रश्नांमध्ये मदत करेन.",
    "fir": "📋 <strong>FIR नोंदणी — तुमचा अधिकार</strong><br>कलम 154 CrPC नुसार पोलीस FIR नोंदवण्यास नकार देऊ शकत नाहीत।<br>📞 पोलीस हेल्पलाइन: <b>100</b>",
    "bail": "🔓 <strong>जामीन (Bail) माहिती</strong><br>कलम 437 CrPC — नियमित जामीन | कलम 438 CrPC — अग्रिम जामीन।<br>📞 विनामूल्य कायदेशीर मदत: <b>15100</b>",
    "legal_aid": "🏛️ <strong>विनामूल्य कायदेशीर सहाय</strong><br>वार्षिक उत्पन्न ₹1,00,000 पेक्षा कमी असल्यास NALSA कडून विनामूल्य वकील मिळतो।<br>📞 NALSA: <b>15100</b>",
    "rights": "🇮🇳 <strong>तुमचे मूलभूत हक्क</strong><br>अनुच्छेद 21 — जगण्याचा आणि व्यक्तिस्वातंत्र्याचा हक्क।<br>अनुच्छेद 22 — बेकायदेशीर अटकेपासून संरक्षण।",
}


def detect_language(query):
    """Detect if query is in Hindi, Marathi, or English."""
    for intent, kw_list in MARATHI_KEYWORDS.items():
        if any(kw in query for kw in kw_list):
            return "mr"
    for intent, kw_list in HINDI_KEYWORDS.items():
        if any(kw in query for kw in kw_list):
            return "hi"
    return "en"


def get_multilingual_response(intent, language):
    """Return response in detected language."""
    if language == "hi" and intent in HINDI_RESPONSES:
        return HINDI_RESPONSES[intent]
    if language == "mr" and intent in MARATHI_RESPONSES:
        return MARATHI_RESPONSES[intent]
    return None


def detect_multilingual_intent(query):
    """Map regional keywords to intent names."""
    query_lower = query.lower()
    mapping = {
        "fir": ["fir", "तक्रार", "दर्ज", "एफआईआर", "एफआयआर", "शिकायत"],
        "bail": ["जमानत", "जामीन"],
        "legal_aid": ["निःशुल्क", "विनामूल्य", "मुफ्त", "15100"],
        "rights": ["अधिकार", "हक्क", "हक़"],
        "police": ["पोलीस", "पुलिस", "ठाणे", "थाना"],
        "women": ["महिला", "औरत", "स्त्री"],
        "arrest": ["अटक", "गिरफ्तार", "हिरासत", "कोठडी"],
    }
    for intent, keywords in mapping.items():
        if any(kw in query_lower for kw in keywords):
            return intent
    return None
