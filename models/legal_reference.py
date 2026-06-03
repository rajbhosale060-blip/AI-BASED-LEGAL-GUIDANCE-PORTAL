"""
Legal Reference Database
Structured Indian laws, acts, and constitutional rights
"""

LEGAL_ACTS = [
    {
        "id": 1,
        "act": "Indian Penal Code (IPC), 1860",
        "category": "Criminal Law",
        "key_sections": "Sections 302, 376, 420, 498A, 307",
        "description": "Primary criminal law of India covering offences against persons, property, and the state.",
        "relevance": "Theft, murder, fraud, domestic violence, rape",
        "citizen_tip": "Under IPC you have the right to know the section you are charged under.",
        "tags": ["criminal", "ipc", "penal", "offence"]
    },
    {
        "id": 2,
        "act": "Code of Criminal Procedure (CrPC), 1973",
        "category": "Criminal Procedure",
        "key_sections": "Sections 41, 50, 154, 161, 167, 436, 437",
        "description": "Governs procedures for investigation, inquiry, trial, and sentencing in criminal cases.",
        "relevance": "FIR filing, arrest, bail, police powers, trial procedure",
        "citizen_tip": "Section 154 CrPC guarantees your right to file an FIR. Police CANNOT refuse.",
        "tags": ["crpc", "fir", "arrest", "bail", "procedure"]
    },
    {
        "id": 3,
        "act": "Constitution of India, 1950",
        "category": "Fundamental Rights",
        "key_sections": "Articles 14, 19, 20, 21, 22, 32, 39A",
        "description": "Supreme law of India. Guarantees Fundamental Rights including equality, liberty, and right to life.",
        "relevance": "Right to equality, freedom of speech, protection against arbitrary arrest",
        "citizen_tip": "Article 21 gives you the right to life and liberty. No one can deprive you without due process.",
        "tags": ["constitution", "fundamental rights", "article 21", "liberty"]
    },
    {
        "id": 4,
        "act": "Protection of Women from Domestic Violence Act, 2005",
        "category": "Women's Rights",
        "key_sections": "Sections 3, 12, 17, 18, 19, 20, 23",
        "description": "Provides protection to women from domestic violence including physical, emotional, sexual, and economic abuse.",
        "relevance": "Domestic violence, protection orders, right to reside in matrimonial home",
        "citizen_tip": "You can file a complaint with a Protection Officer or Magistrate. Shelter homes are available.",
        "tags": ["domestic violence", "women", "protection", "dv act"]
    },
    {
        "id": 5,
        "act": "Information Technology Act, 2000 (IT Act)",
        "category": "Cyber Law",
        "key_sections": "Sections 43, 66, 66A, 66C, 66D, 67, 72",
        "description": "Regulates cyber crimes including hacking, identity theft, online fraud, and data breaches.",
        "relevance": "Cyber crime, online harassment, hacking, data theft",
        "citizen_tip": "File a complaint at cybercrime.gov.in or your nearest cyber crime police station.",
        "tags": ["cyber", "it act", "hacking", "online fraud", "cybercrime"]
    },
    {
        "id": 6,
        "act": "Right to Information Act (RTI), 2005",
        "category": "Citizen Rights",
        "key_sections": "Sections 3, 4, 6, 7, 8, 19",
        "description": "Empowers citizens to request information from public authorities within 30 days.",
        "relevance": "Government transparency, public information, accountability",
        "citizen_tip": "Any citizen can file RTI for Rs.10. Online RTI: rtionline.gov.in",
        "tags": ["rti", "information", "transparency", "government"]
    },
    {
        "id": 7,
        "act": "POCSO Act, 2012",
        "category": "Child Protection",
        "key_sections": "Sections 4, 6, 7, 8, 19, 20, 21",
        "description": "Protection of Children from Sexual Offences. Strict punishment for sexual crimes against children.",
        "relevance": "Child sexual abuse, exploitation, trafficking",
        "citizen_tip": "POCSO is a mandatory reporting law. Any person aware of abuse MUST report to police.",
        "tags": ["pocso", "child", "sexual offence", "protection", "minor"]
    },
    {
        "id": 8,
        "act": "Legal Services Authorities Act, 1987 (NALSA)",
        "category": "Legal Aid",
        "key_sections": "Sections 12, 13, 14, 15, 18, 19, 20, 21, 22",
        "description": "Provides free legal services to economically weak, marginalized, and vulnerable citizens.",
        "relevance": "Free legal aid, lok adalat, legal awareness",
        "citizen_tip": "If your annual income is below Rs.1 lakh, you are entitled to FREE legal aid from NALSA.",
        "tags": ["nalsa", "legal aid", "free", "lok adalat"]
    },
    {
        "id": 9,
        "act": "Scheduled Castes and Scheduled Tribes (Prevention of Atrocities) Act, 1989",
        "category": "Anti-Discrimination",
        "key_sections": "Sections 3, 4, 14, 14A, 17, 18A",
        "description": "Prevents atrocities and discrimination against SC/ST communities. Special courts for fast trial.",
        "relevance": "Caste-based discrimination, atrocities, harassment",
        "citizen_tip": "Cases under SC/ST Act must be investigated by DSP-rank officer and tried in Special Courts.",
        "tags": ["sc st", "atrocities", "dalit", "discrimination", "caste"]
    },
    {
        "id": 10,
        "act": "Dowry Prohibition Act, 1961",
        "category": "Women's Rights",
        "key_sections": "Sections 3, 4, 6, 8",
        "description": "Prohibits giving or taking dowry at the time of marriage. Punishable with imprisonment.",
        "relevance": "Dowry demands, harassment for dowry",
        "citizen_tip": "IPC 498A also covers dowry cruelty. File complaint at nearest police station or women's cell.",
        "tags": ["dowry", "women", "marriage", "harassment"]
    },
    {
        "id": 11,
        "act": "Juvenile Justice Act, 2015",
        "category": "Child Rights",
        "key_sections": "Sections 2, 3, 7, 15, 19, 39, 75, 76",
        "description": "Provides care, protection, and rehabilitation for children in conflict with law and children in need.",
        "relevance": "Juvenile offenders, child care, adoption, orphans",
        "citizen_tip": "Children below 18 cannot be tried as adults except for heinous offences under special circumstances.",
        "tags": ["juvenile", "child", "jj act", "care protection"]
    },
    {
        "id": 12,
        "act": "Motor Vehicles Act, 1988",
        "category": "Traffic & Road Safety",
        "key_sections": "Sections 134, 161, 162, 163A, 166",
        "description": "Regulates road transport, licensing, insurance, and compensation for accident victims.",
        "relevance": "Road accidents, insurance claims, drunk driving, compensation",
        "citizen_tip": "Accident victims or their families can claim compensation from Motor Accident Claims Tribunal (MACT).",
        "tags": ["motor vehicle", "accident", "compensation", "road", "insurance"]
    },
    {
        "id": 13,
        "act": "Consumer Protection Act, 2019",
        "category": "Consumer Rights",
        "key_sections": "Sections 2, 17, 34, 35, 47, 58",
        "description": "Protects consumers from unfair trade practices, defective goods, and deficient services.",
        "relevance": "Product defects, online fraud, medical negligence, service issues",
        "citizen_tip": "File online complaint at consumerhelpline.gov.in or nearest District Consumer Forum.",
        "tags": ["consumer", "fraud", "defect", "complaint", "rights"]
    },
    {
        "id": 14,
        "act": "Prevention of Corruption Act, 1988",
        "category": "Anti-Corruption",
        "key_sections": "Sections 7, 8, 11, 13, 17A",
        "description": "Punishes public servants for taking bribes and corrupt practices.",
        "relevance": "Bribery, corruption by government officials",
        "citizen_tip": "Report corruption at ACB (Anti-Corruption Bureau) or use the Vigilance portal. Bribe-givers are also protected.",
        "tags": ["corruption", "bribery", "public servant", "acb"]
    },
    {
        "id": 15,
        "act": "Right of Children to Free and Compulsory Education Act (RTE), 2009",
        "category": "Child Rights",
        "key_sections": "Sections 3, 4, 12, 13, 17, 21",
        "description": "Guarantees free and compulsory education to children aged 6-14 years.",
        "relevance": "School admission, free education, private school quota",
        "citizen_tip": "25% seats in private schools must be reserved for economically weaker sections under RTE.",
        "tags": ["rte", "education", "child", "school", "free"]
    }
]


def get_legal_acts():
    """Return all legal acts."""
    return LEGAL_ACTS


def search_legal_acts(query):
    """Search legal acts by keyword."""
    if not query:
        return LEGAL_ACTS
    query_lower = query.lower()
    results = []
    for act in LEGAL_ACTS:
        if (query_lower in act['act'].lower() or
                query_lower in act['description'].lower() or
                query_lower in act['relevance'].lower() or
                query_lower in act['category'].lower() or
                any(query_lower in tag for tag in act['tags'])):
            results.append(act)
    return results
