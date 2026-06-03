"""
Maharashtra Police Directory
District-wise SP offices, police stations, and contact info
"""

DISTRICTS = {
    "Mumbai City": {
        "division": "Mumbai",
        "sp_office": "Commissioner of Police, Mumbai",
        "sp_address": "Crawford Market, Mumbai - 400001",
        "sp_phone": "022-22620111",
        "helpline": "100",
        "stations": [
            {"name": "Azad Maidan", "phone": "022-22621855", "area": "Fort, CST"},
            {"name": "Colaba", "phone": "022-22151581", "area": "Colaba, Nariman Point"},
            {"name": "Cuffe Parade", "phone": "022-22183131", "area": "Cuffe Parade"},
            {"name": "MRA Marg", "phone": "022-22621111", "area": "Marine Lines, Grant Road"},
        ]
    },
    "Mumbai Suburban": {
        "division": "Mumbai",
        "sp_office": "Commissioner of Police, Mumbai (Suburban)",
        "sp_address": "Bandra (East), Mumbai - 400051",
        "sp_phone": "022-26590200",
        "helpline": "100",
        "stations": [
            {"name": "Bandra", "phone": "022-26435900", "area": "Bandra East/West"},
            {"name": "Andheri", "phone": "022-26204411", "area": "Andheri, Juhu"},
            {"name": "Borivali", "phone": "022-28942911", "area": "Borivali, Kandivali"},
            {"name": "Kurla", "phone": "022-25010101", "area": "Kurla, Chembur"},
        ]
    },
    "Thane": {
        "division": "Konkan",
        "sp_office": "Superintendent of Police, Thane",
        "sp_address": "SP Office, Thane - 400601",
        "sp_phone": "022-25330090",
        "helpline": "100",
        "stations": [
            {"name": "Thane City", "phone": "022-25344141", "area": "Thane City"},
            {"name": "Kalyan", "phone": "0251-2311000", "area": "Kalyan, Dombivli"},
            {"name": "Bhiwandi", "phone": "02522-241100", "area": "Bhiwandi"},
            {"name": "Ulhasnagar", "phone": "0251-2730100", "area": "Ulhasnagar"},
        ]
    },
    "Palghar": {
        "division": "Konkan",
        "sp_office": "Superintendent of Police, Palghar",
        "sp_address": "SP Office, Palghar - 401404",
        "sp_phone": "02525-252300",
        "helpline": "100",
        "stations": [
            {"name": "Palghar", "phone": "02525-252233", "area": "Palghar Town"},
            {"name": "Vasai", "phone": "0250-2337100", "area": "Vasai, Virar"},
            {"name": "Boisar", "phone": "02525-272100", "area": "Boisar, Tarapur"},
        ]
    },
    "Raigad": {
        "division": "Konkan",
        "sp_office": "Superintendent of Police, Raigad",
        "sp_address": "SP Office, Alibag - 402201",
        "sp_phone": "02141-222233",
        "helpline": "100",
        "stations": [
            {"name": "Alibag", "phone": "02141-222100", "area": "Alibag"},
            {"name": "Panvel", "phone": "022-27456600", "area": "Panvel, Navi Mumbai"},
            {"name": "Pen", "phone": "02143-255100", "area": "Pen"},
        ]
    },
    "Ratnagiri": {
        "division": "Konkan",
        "sp_office": "Superintendent of Police, Ratnagiri",
        "sp_address": "SP Office, Ratnagiri - 415612",
        "sp_phone": "02352-222222",
        "helpline": "100",
        "stations": [
            {"name": "Ratnagiri City", "phone": "02352-222100", "area": "Ratnagiri City"},
            {"name": "Chiplun", "phone": "02355-252100", "area": "Chiplun"},
            {"name": "Khed", "phone": "02356-222100", "area": "Khed"},
        ]
    },
    "Sindhudurg": {
        "division": "Konkan",
        "sp_office": "Superintendent of Police, Sindhudurg",
        "sp_address": "SP Office, Oros - 416812",
        "sp_phone": "02362-228500",
        "helpline": "100",
        "stations": [
            {"name": "Kudal", "phone": "02362-222100", "area": "Kudal"},
            {"name": "Sawantwadi", "phone": "02363-272100", "area": "Sawantwadi"},
            {"name": "Malvan", "phone": "02365-252100", "area": "Malvan"},
        ]
    },
    "Nashik": {
        "division": "Nashik",
        "sp_office": "Commissioner / SP, Nashik",
        "sp_address": "SP Office, Nashik - 422001",
        "sp_phone": "0253-2576000",
        "helpline": "100",
        "stations": [
            {"name": "Nashik Road", "phone": "0253-2465100", "area": "Nashik Road"},
            {"name": "Gangapur Road", "phone": "0253-2310100", "area": "Gangapur"},
            {"name": "Deolali Camp", "phone": "0253-2490100", "area": "Deolali"},
            {"name": "Malegaon", "phone": "02554-252100", "area": "Malegaon"},
        ]
    },
    "Dhule": {
        "division": "Nashik",
        "sp_office": "Superintendent of Police, Dhule",
        "sp_address": "SP Office, Dhule - 424001",
        "sp_phone": "02562-233300",
        "helpline": "100",
        "stations": [
            {"name": "Dhule City", "phone": "02562-233100", "area": "Dhule City"},
            {"name": "Shirpur", "phone": "02563-272100", "area": "Shirpur"},
        ]
    },
    "Nandurbar": {
        "division": "Nashik",
        "sp_office": "Superintendent of Police, Nandurbar",
        "sp_address": "SP Office, Nandurbar - 425412",
        "sp_phone": "02564-210100",
        "helpline": "100",
        "stations": [
            {"name": "Nandurbar", "phone": "02564-210200", "area": "Nandurbar Town"},
            {"name": "Shahada", "phone": "02565-222100", "area": "Shahada"},
            {"name": "Taloda", "phone": "02566-242100", "area": "Taloda"},
        ]
    },
    "Jalgaon": {
        "division": "Nashik",
        "sp_office": "Superintendent of Police, Jalgaon",
        "sp_address": "SP Office, Jalgaon - 425001",
        "sp_phone": "0257-2221100",
        "helpline": "100",
        "stations": [
            {"name": "Jalgaon City", "phone": "0257-2221200", "area": "Jalgaon City"},
            {"name": "Bhusawal", "phone": "02582-222100", "area": "Bhusawal"},
            {"name": "Chalisgaon", "phone": "02589-222100", "area": "Chalisgaon"},
        ]
    },
    "Ahmednagar": {
        "division": "Nashik",
        "sp_office": "Superintendent of Police, Ahmednagar",
        "sp_address": "SP Office, Ahmednagar - 414001",
        "sp_phone": "0241-2777100",
        "helpline": "100",
        "stations": [
            {"name": "Ahmednagar City", "phone": "0241-2777200", "area": "Ahmednagar City"},
            {"name": "Sangamner", "phone": "02425-222100", "area": "Sangamner"},
            {"name": "Kopargaon", "phone": "02423-222100", "area": "Kopargaon"},
            {"name": "Shrirampur", "phone": "02422-222100", "area": "Shrirampur"},
        ]
    },
    "Pune": {
        "division": "Pune",
        "sp_office": "Commissioner of Police, Pune",
        "sp_address": "Police Commissioner Office, Shivajinagar, Pune - 411005",
        "sp_phone": "020-26122880",
        "helpline": "100",
        "stations": [
            {"name": "Shivajinagar", "phone": "020-25536262", "area": "Shivajinagar, FC Road"},
            {"name": "Deccan", "phone": "020-25656100", "area": "Deccan Gymkhana"},
            {"name": "Hadapsar", "phone": "020-26970100", "area": "Hadapsar, Magarpatta"},
            {"name": "Hinjawadi", "phone": "020-27575100", "area": "Hinjawadi IT Park"},
        ]
    },
    "Satara": {
        "division": "Pune",
        "sp_office": "Superintendent of Police, Satara",
        "sp_address": "SP Office, Satara - 415001",
        "sp_phone": "02162-230100",
        "helpline": "100",
        "stations": [
            {"name": "Satara City", "phone": "02162-230200", "area": "Satara City"},
            {"name": "Karad", "phone": "02164-222100", "area": "Karad"},
            {"name": "Wai", "phone": "02167-222100", "area": "Wai"},
        ]
    },
    "Sangli": {
        "division": "Pune",
        "sp_office": "Superintendent of Police, Sangli",
        "sp_address": "SP Office, Sangli - 416416",
        "sp_phone": "0233-2601100",
        "helpline": "100",
        "stations": [
            {"name": "Sangli City", "phone": "0233-2601200", "area": "Sangli City"},
            {"name": "Miraj", "phone": "0233-2222100", "area": "Miraj"},
            {"name": "Islampur", "phone": "02342-222100", "area": "Islampur"},
        ]
    },
    "Solapur": {
        "division": "Pune",
        "sp_office": "Commissioner / SP, Solapur",
        "sp_address": "SP Office, Solapur - 413001",
        "sp_phone": "0217-2726100",
        "helpline": "100",
        "stations": [
            {"name": "Solapur City", "phone": "0217-2726200", "area": "Solapur City"},
            {"name": "Pandharpur", "phone": "02186-222100", "area": "Pandharpur"},
            {"name": "Barshi", "phone": "02184-222100", "area": "Barshi"},
        ]
    },
    "Kolhapur": {
        "division": "Pune",
        "sp_office": "Commissioner / SP, Kolhapur",
        "sp_address": "SP Office, Kolhapur - 416001",
        "sp_phone": "0231-2540100",
        "helpline": "100",
        "stations": [
            {"name": "Kolhapur City", "phone": "0231-2540200", "area": "Kolhapur City"},
            {"name": "Ichalkaranji", "phone": "0230-2421100", "area": "Ichalkaranji"},
            {"name": "Kagal", "phone": "02325-222100", "area": "Kagal"},
        ]
    },
    "Aurangabad": {
        "division": "Aurangabad",
        "sp_office": "Commissioner of Police, Aurangabad",
        "sp_address": "Police Commissioner Office, Aurangabad - 431001",
        "sp_phone": "0240-2324444",
        "helpline": "100",
        "stations": [
            {"name": "Aurangabad City", "phone": "0240-2324100", "area": "Aurangabad City"},
            {"name": "CIDCO", "phone": "0240-2484100", "area": "CIDCO, N-8"},
            {"name": "Begumpura", "phone": "0240-2334100", "area": "Begumpura"},
        ]
    },
    "Jalna": {
        "division": "Aurangabad",
        "sp_office": "Superintendent of Police, Jalna",
        "sp_address": "SP Office, Jalna - 431203",
        "sp_phone": "02482-222100",
        "helpline": "100",
        "stations": [
            {"name": "Jalna City", "phone": "02482-222200", "area": "Jalna City"},
            {"name": "Ambad", "phone": "02483-222100", "area": "Ambad"},
        ]
    },
    "Beed": {
        "division": "Aurangabad",
        "sp_office": "Superintendent of Police, Beed",
        "sp_address": "SP Office, Beed - 431122",
        "sp_phone": "02442-222100",
        "helpline": "100",
        "stations": [
            {"name": "Beed City", "phone": "02442-222200", "area": "Beed City"},
            {"name": "Ambejogai", "phone": "02446-252100", "area": "Ambejogai"},
            {"name": "Georai", "phone": "02443-252100", "area": "Georai"},
        ]
    },
    "Osmanabad": {
        "division": "Aurangabad",
        "sp_office": "Superintendent of Police, Osmanabad",
        "sp_address": "SP Office, Osmanabad - 413501",
        "sp_phone": "02472-222100",
        "helpline": "100",
        "stations": [
            {"name": "Osmanabad City", "phone": "02472-222200", "area": "Osmanabad City"},
            {"name": "Tuljapur", "phone": "02471-222100", "area": "Tuljapur"},
        ]
    },
    "Latur": {
        "division": "Aurangabad",
        "sp_office": "Superintendent of Police, Latur",
        "sp_address": "SP Office, Latur - 413512",
        "sp_phone": "02382-222100",
        "helpline": "100",
        "stations": [
            {"name": "Latur City", "phone": "02382-222200", "area": "Latur City"},
            {"name": "Udgir", "phone": "02385-252100", "area": "Udgir"},
            {"name": "Nilanga", "phone": "02381-222100", "area": "Nilanga"},
        ]
    },
    "Nanded": {
        "division": "Aurangabad",
        "sp_office": "Commissioner / SP, Nanded",
        "sp_address": "SP Office, Nanded - 431601",
        "sp_phone": "02462-236100",
        "helpline": "100",
        "stations": [
            {"name": "Nanded City", "phone": "02462-236200", "area": "Nanded City"},
            {"name": "Deglur", "phone": "02463-222100", "area": "Deglur"},
            {"name": "Kinwat", "phone": "02465-222100", "area": "Kinwat"},
        ]
    },
    "Hingoli": {
        "division": "Aurangabad",
        "sp_office": "Superintendent of Police, Hingoli",
        "sp_address": "SP Office, Hingoli - 431513",
        "sp_phone": "02456-222100",
        "helpline": "100",
        "stations": [
            {"name": "Hingoli City", "phone": "02456-222200", "area": "Hingoli City"},
            {"name": "Basmath", "phone": "02457-222100", "area": "Basmath"},
        ]
    },
    "Parbhani": {
        "division": "Aurangabad",
        "sp_office": "Superintendent of Police, Parbhani",
        "sp_address": "SP Office, Parbhani - 431401",
        "sp_phone": "02452-222100",
        "helpline": "100",
        "stations": [
            {"name": "Parbhani City", "phone": "02452-222200", "area": "Parbhani City"},
            {"name": "Pathri", "phone": "02453-222100", "area": "Pathri"},
            {"name": "Manwath", "phone": "02454-222100", "area": "Manwath"},
        ]
    },
    "Buldhana": {
        "division": "Amravati",
        "sp_office": "Superintendent of Police, Buldhana",
        "sp_address": "SP Office, Buldhana - 443001",
        "sp_phone": "07262-222100",
        "helpline": "100",
        "stations": [
            {"name": "Buldhana City", "phone": "07262-222200", "area": "Buldhana City"},
            {"name": "Khamgaon", "phone": "07263-252100", "area": "Khamgaon"},
            {"name": "Malkapur", "phone": "07264-222100", "area": "Malkapur"},
        ]
    },
    "Akola": {
        "division": "Amravati",
        "sp_office": "Superintendent of Police, Akola",
        "sp_address": "SP Office, Akola - 444001",
        "sp_phone": "0724-2430100",
        "helpline": "100",
        "stations": [
            {"name": "Akola City", "phone": "0724-2430200", "area": "Akola City"},
            {"name": "Akot", "phone": "07258-222100", "area": "Akot"},
            {"name": "Balapur", "phone": "07255-222100", "area": "Balapur"},
        ]
    },
    "Washim": {
        "division": "Amravati",
        "sp_office": "Superintendent of Police, Washim",
        "sp_address": "SP Office, Washim - 444505",
        "sp_phone": "07252-232100",
        "helpline": "100",
        "stations": [
            {"name": "Washim City", "phone": "07252-232200", "area": "Washim City"},
            {"name": "Mangrulpir", "phone": "07259-222100", "area": "Mangrulpir"},
        ]
    },
    "Amravati": {
        "division": "Amravati",
        "sp_office": "Commissioner / SP, Amravati",
        "sp_address": "SP Office, Amravati - 444601",
        "sp_phone": "0721-2661100",
        "helpline": "100",
        "stations": [
            {"name": "Amravati City", "phone": "0721-2661200", "area": "Amravati City"},
            {"name": "Achalpur", "phone": "07220-222100", "area": "Achalpur"},
            {"name": "Daryapur", "phone": "07221-222100", "area": "Daryapur"},
        ]
    },
    "Yavatmal": {
        "division": "Amravati",
        "sp_office": "Superintendent of Police, Yavatmal",
        "sp_address": "SP Office, Yavatmal - 445001",
        "sp_phone": "07232-242100",
        "helpline": "100",
        "stations": [
            {"name": "Yavatmal City", "phone": "07232-242200", "area": "Yavatmal City"},
            {"name": "Wani", "phone": "07233-222100", "area": "Wani"},
            {"name": "Pusad", "phone": "07231-222100", "area": "Pusad"},
        ]
    },
    "Nagpur": {
        "division": "Nagpur",
        "sp_office": "Commissioner of Police, Nagpur",
        "sp_address": "Police Commissioner Office, Civil Lines, Nagpur - 440001",
        "sp_phone": "0712-2565100",
        "helpline": "100",
        "stations": [
            {"name": "Sitabuldi", "phone": "0712-2524100", "area": "Sitabuldi, Itwari"},
            {"name": "Sadar", "phone": "0712-2533100", "area": "Sadar, Civil Lines"},
            {"name": "Lakadganj", "phone": "0712-2726100", "area": "Lakadganj"},
            {"name": "Kalamna", "phone": "0712-2690100", "area": "Kalamna, Kamptee"},
        ]
    },
    "Wardha": {
        "division": "Nagpur",
        "sp_office": "Superintendent of Police, Wardha",
        "sp_address": "SP Office, Wardha - 442001",
        "sp_phone": "07152-242100",
        "helpline": "100",
        "stations": [
            {"name": "Wardha City", "phone": "07152-242200", "area": "Wardha City"},
            {"name": "Hinganghat", "phone": "07153-222100", "area": "Hinganghat"},
        ]
    },
    "Chandrapur": {
        "division": "Nagpur",
        "sp_office": "Superintendent of Police, Chandrapur",
        "sp_address": "SP Office, Chandrapur - 442401",
        "sp_phone": "07172-252100",
        "helpline": "100",
        "stations": [
            {"name": "Chandrapur City", "phone": "07172-252200", "area": "Chandrapur City"},
            {"name": "Ballarpur", "phone": "07177-222100", "area": "Ballarpur"},
            {"name": "Gadchiroli", "phone": "07132-222100", "area": "Gadchiroli border"},
        ]
    },
    "Gadchiroli": {
        "division": "Nagpur",
        "sp_office": "Superintendent of Police, Gadchiroli",
        "sp_address": "SP Office, Gadchiroli - 442605",
        "sp_phone": "07132-222333",
        "helpline": "100",
        "stations": [
            {"name": "Gadchiroli City", "phone": "07132-222100", "area": "Gadchiroli City"},
            {"name": "Sironcha", "phone": "07134-222100", "area": "Sironcha"},
            {"name": "Aheri", "phone": "07133-222100", "area": "Aheri"},
        ]
    },
    "Gondia": {
        "division": "Nagpur",
        "sp_office": "Superintendent of Police, Gondia",
        "sp_address": "SP Office, Gondia - 441601",
        "sp_phone": "07182-222100",
        "helpline": "100",
        "stations": [
            {"name": "Gondia City", "phone": "07182-222200", "area": "Gondia City"},
            {"name": "Tirora", "phone": "07186-222100", "area": "Tirora"},
        ]
    },
    "Bhandara": {
        "division": "Nagpur",
        "sp_office": "Superintendent of Police, Bhandara",
        "sp_address": "SP Office, Bhandara - 441904",
        "sp_phone": "07184-252100",
        "helpline": "100",
        "stations": [
            {"name": "Bhandara City", "phone": "07184-252200", "area": "Bhandara City"},
            {"name": "Tumsar", "phone": "07185-222100", "area": "Tumsar"},
        ]
    }
}


def get_all_districts():
    """Return list of all district names."""
    return sorted(DISTRICTS.keys())


def get_district_info(district_name):
    """Return full info for a district."""
    if district_name in DISTRICTS:
        info = DISTRICTS[district_name].copy()
        info['district'] = district_name
        return {"success": True, "data": info}
    return {"success": False, "message": "District not found"}
