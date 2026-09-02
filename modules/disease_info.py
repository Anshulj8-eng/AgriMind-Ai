
def normalize_disease_name(disease):

    if disease is None:
        return ""

    disease = str(disease).strip()

# Remove accidental spaces
    disease = disease.replace(" ", "_")

    return disease

DISEASE_INFO = {

# =========================================================
# APPLE DISEASES
# =========================================================

"Apple___Apple_scab": {
    "symptoms": "Olive-green or dark brown spots appear on leaves and fruits. Leaves may curl, turn yellow and fall early.",
    "cause": "Caused by the fungus Venturia inaequalis, especially during cool and wet weather.",
    "prevention": "Remove fallen infected leaves, improve air circulation, avoid excessive moisture and use disease-resistant varieties.",
    "management": "Prune infected parts and apply locally recommended fungicides according to agricultural guidelines."
},

"Apple___Black_rot": {
    "symptoms": "Purple or brown leaf spots appear. Fruits may develop dark rotten areas and shrivel.",
    "cause": "Caused by the fungus Botryosphaeria obtusa.",
    "prevention": "Remove infected fruits and branches, maintain orchard sanitation and avoid plant injuries.",
    "management": "Prune infected branches and use approved fungicide treatment when necessary."
},

"Apple___Cedar_apple_rust": {
    "symptoms": "Bright yellow or orange spots develop on leaves and fruits.",
    "cause": "Caused by the fungus Gymnosporangium species.",
    "prevention": "Remove nearby alternate host plants where possible and improve orchard monitoring.",
    "management": "Use resistant varieties and apply recommended fungicides during high-risk periods."
},

"Apple___healthy": {
    "symptoms": "No major disease symptoms detected. Leaves and plant structure appear healthy.",
    "cause": "No disease detected by the AI model.",
    "prevention": "Continue regular monitoring, balanced nutrition and proper irrigation.",
    "management": "Maintain good agricultural practices and inspect plants regularly."
},


# =========================================================
# BLUEBERRY
# =========================================================

"Blueberry___healthy": {
    "symptoms": "No visible disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain proper soil acidity, irrigation and regular crop monitoring.",
    "management": "Continue normal crop care and balanced fertilization."
},


# =========================================================
# CHERRY
# =========================================================

"Cherry_(including_sour)___Powdery_mildew": {
    "symptoms": "White powder-like fungal growth appears on leaves and young shoots. Leaves may curl or become distorted.",
    "cause": "Caused by powdery mildew fungi under warm and humid conditions.",
    "prevention": "Maintain proper spacing, improve air circulation and avoid excessive nitrogen fertilizer.",
    "management": "Remove heavily infected plant parts and apply recommended fungicide treatment."
},

"Cherry_(including_sour)___healthy": {
    "symptoms": "No significant disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Continue proper watering, pruning and nutrient management.",
    "management": "Regular monitoring is recommended."
},


# =========================================================
# CORN / MAIZE
# =========================================================

"Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
    "symptoms": "Rectangular gray or tan lesions appear on leaves and may expand over time.",
    "cause": "Caused by the fungus Cercospora zeae-maydis.",
    "prevention": "Use crop rotation, resistant hybrids and remove infected crop residues.",
    "management": "Monitor the crop and apply recommended fungicides when disease pressure is high."
},

"Corn_(maize)___Common_rust_": {
    "symptoms": "Small reddish-brown or orange pustules appear on both leaf surfaces.",
    "cause": "Caused by Puccinia sorghi fungus.",
    "prevention": "Use resistant maize varieties and monitor fields regularly.",
    "management": "Apply agricultural fungicides if infection becomes severe."
},

"Corn_(maize)___Northern_Leaf_Blight": {
    "symptoms": "Large gray-green or tan elongated lesions develop on leaves.",
    "cause": "Caused by the fungus Exserohilum turcicum.",
    "prevention": "Use resistant varieties, rotate crops and remove infected crop residues.",
    "management": "Use recommended fungicides and maintain good field sanitation."
},

"Corn_(maize)___healthy": {
    "symptoms": "No major disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain proper irrigation and nutrient management.",
    "management": "Continue regular field inspection."
},


# =========================================================
# GRAPE
# =========================================================

"Grape___Black_rot": {
    "symptoms": "Brown circular spots appear on leaves. Fruits may develop dark spots and eventually shrivel.",
    "cause": "Caused by the fungus Guignardia bidwellii.",
    "prevention": "Remove infected fruits, prune vines properly and improve air circulation.",
    "management": "Use approved fungicides and remove infected plant material."
},

"Grape___Esca_(Black_Measles)": {
    "symptoms": "Leaves may show yellow and brown striping. Fruits can develop dark spots.",
    "cause": "Associated with fungal pathogens affecting grapevine wood.",
    "prevention": "Avoid unnecessary vine injuries and remove severely infected plants.",
    "management": "Prune infected wood and follow local vineyard disease management practices."
},

"Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
    "symptoms": "Dark brown or black spots develop on grape leaves and may cause leaf drying.",
    "cause": "Caused by fungal infection.",
    "prevention": "Maintain vineyard sanitation and avoid excessive leaf moisture.",
    "management": "Remove infected leaves and apply recommended fungicides."
},

"Grape___healthy": {
    "symptoms": "No visible disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain pruning, irrigation and nutrient balance.",
    "management": "Continue regular vineyard monitoring."
},


# =========================================================
# ORANGE
# =========================================================

"Orange___Haunglongbing_(Citrus_greening)": {
    "symptoms": "Leaves may become yellow unevenly, fruits can become small, misshapen and bitter.",
    "cause": "Associated with bacteria spread mainly by citrus psyllid insects.",
    "prevention": "Use disease-free planting material and control insect vectors.",
    "management": "Remove severely infected trees and follow local agricultural authority recommendations."
},


# =========================================================
# PEACH
# =========================================================

"Peach___Bacterial_spot": {
    "symptoms": "Dark spots appear on leaves and fruits. Leaves may develop holes after infected tissue falls out.",
    "cause": "Caused by Xanthomonas bacteria.",
    "prevention": "Use healthy planting material and avoid working with plants when foliage is wet.",
    "management": "Remove infected plant material and follow approved bacterial disease management practices."
},

"Peach___healthy": {
    "symptoms": "No significant disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain proper irrigation and orchard sanitation.",
    "management": "Continue regular monitoring."
},


# =========================================================
# PEPPER
# =========================================================

"Pepper,_bell___Bacterial_spot": {
    "symptoms": "Small dark spots appear on leaves and fruits. Leaves may turn yellow and drop.",
    "cause": "Caused by Xanthomonas bacterial infection.",
    "prevention": "Use disease-free seeds, avoid overhead irrigation and practice crop rotation.",
    "management": "Remove infected plants and follow recommended bacterial disease control methods."
},

"Pepper,_bell___healthy": {
    "symptoms": "No visible disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain balanced nutrition and regular irrigation.",
    "management": "Continue routine crop monitoring."
},


# =========================================================
# POTATO
# =========================================================

"Potato___Early_blight": {
    "symptoms": "Brown spots with concentric rings appear on older leaves. Leaves may yellow and dry.",
    "cause": "Caused by the fungus Alternaria solani.",
    "prevention": "Use crop rotation, remove infected leaves and maintain balanced plant nutrition.",
    "management": "Apply recommended fungicides and remove heavily infected foliage."
},

"Potato___Late_blight": {
    "symptoms": "Dark brown water-soaked lesions appear on leaves. White fungal growth may appear underneath leaves.",
    "cause": "Caused by Phytophthora infestans.",
    "prevention": "Avoid prolonged leaf wetness, use healthy seed potatoes and monitor fields regularly.",
    "management": "Remove infected plants and apply locally recommended fungicide treatment."
},

"Potato___healthy": {
    "symptoms": "No major disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain proper irrigation and crop nutrition.",
    "management": "Continue regular crop inspection."
},


# =========================================================
# RASPBERRY
# =========================================================

"Raspberry___healthy": {
    "symptoms": "No visible disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain good drainage, pruning and proper plant spacing.",
    "management": "Continue regular monitoring."
},


# =========================================================
# SOYBEAN
# =========================================================

"Soybean___healthy": {
    "symptoms": "No significant disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Use crop rotation and proper nutrient management.",
    "management": "Maintain regular field monitoring."
},


# =========================================================
# SQUASH
# =========================================================

"Squash___Powdery_mildew": {
    "symptoms": "White powder-like patches appear on leaves and stems.",
    "cause": "Caused by powdery mildew fungi.",
    "prevention": "Provide proper spacing and airflow and avoid excessive nitrogen.",
    "management": "Remove heavily infected leaves and use approved fungicide treatment."
},


# =========================================================
# STRAWBERRY
# =========================================================

"Strawberry___Leaf_scorch": {
    "symptoms": "Dark purple or reddish spots appear on leaves. Severe infection causes leaf edges to dry.",
    "cause": "Caused by fungal infection.",
    "prevention": "Remove infected leaves, avoid excessive moisture and maintain plant spacing.",
    "management": "Improve field sanitation and apply recommended fungicides if required."
},

"Strawberry___healthy": {
    "symptoms": "No visible disease symptoms detected.",
    "cause": "Plant appears healthy.",
    "prevention": "Maintain proper watering and remove old damaged leaves.",
    "management": "Continue regular crop care."
},


# =========================================================
# TOMATO DISEASES
# =========================================================

"Tomato___Bacterial_spot": {
    "symptoms": "Small dark or brown spots appear on leaves, stems and fruits. Leaves may turn yellow.",
    "cause": "Caused by bacterial pathogens, often spreading through water, tools and infected seeds.",
    "prevention": "Use disease-free seeds, avoid overhead watering, disinfect tools and practice crop rotation.",
    "management": "Remove heavily infected plants and follow approved bacterial disease management recommendations."
},

"Tomato___Early_blight": {
    "symptoms": "Brown spots with concentric rings appear mainly on older leaves. Leaves may turn yellow and dry.",
    "cause": "Caused by the fungus Alternaria solani.",
    "prevention": "Practice crop rotation, remove infected leaves, maintain proper spacing and avoid excessive leaf moisture.",
    "management": "Remove infected foliage and apply locally recommended fungicides when necessary."
},

"Tomato___Late_blight": {
    "symptoms": "Large dark brown or black water-soaked spots appear on leaves. White fungal growth may occur underneath leaves.",
    "cause": "Caused by Phytophthora infestans and favored by cool, humid and wet conditions.",
    "prevention": "Avoid prolonged leaf wetness, ensure good airflow and inspect plants regularly.",
    "management": "Remove severely infected plant parts and use locally recommended fungicide treatment."
},

"Tomato___Leaf_Mold": {
    "symptoms": "Yellow patches appear on upper leaf surfaces while olive-green or gray mold develops underneath.",
    "cause": "Caused by Passalora fulva fungus, especially in humid environments.",
    "prevention": "Improve greenhouse ventilation, reduce humidity and avoid excessive leaf wetness.",
    "management": "Remove infected leaves and apply recommended fungicide treatment."
},

"Tomato___Septoria_leaf_spot": {
    "symptoms": "Numerous small circular spots with dark borders and light centers appear on lower leaves.",
    "cause": "Caused by the fungus Septoria lycopersici.",
    "prevention": "Remove infected leaves, avoid splashing soil onto plants and practice crop rotation.",
    "management": "Apply recommended fungicides and maintain proper field sanitation."
},

"Tomato___Spider_mites Two-spotted_spider_mite": {
    "symptoms": "Tiny yellow spots, leaf discoloration, webbing and eventual leaf drying may occur.",
    "cause": "Damage caused by two-spotted spider mites.",
    "prevention": "Monitor plants regularly and avoid excessively dry and dusty conditions.",
    "management": "Use appropriate biological or agricultural mite control methods."
},

"Tomato___Target_Spot": {
    "symptoms": "Brown circular spots with concentric patterns appear on leaves and fruits.",
    "cause": "Caused by fungal infection, commonly Corynespora cassiicola.",
    "prevention": "Improve air circulation, remove infected debris and avoid excessive moisture.",
    "management": "Remove infected leaves and apply recommended fungicide treatment."
},

"Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
    "symptoms": "Leaves become yellow, curl upward and become smaller. Plant growth may become stunted.",
    "cause": "Caused by Tomato Yellow Leaf Curl Virus, commonly transmitted by whiteflies.",
    "prevention": "Control whiteflies, use resistant varieties and remove infected plants.",
    "management": "There is no direct cure. Remove infected plants and control insect vectors."
},

"Tomato___Tomato_mosaic_virus": {
    "symptoms": "Mosaic patterns of light and dark green appear on leaves. Leaves may become distorted.",
    "cause": "Caused by Tomato Mosaic Virus.",
    "prevention": "Use disease-free seeds, disinfect tools and avoid handling plants after tobacco contact.",
    "management": "Remove infected plants and maintain strict sanitation."
},

"Tomato___healthy": {
    "symptoms": "No major disease symptoms detected. Leaves appear healthy.",
    "cause": "No disease detected by the AI model.",
    "prevention": "Continue proper irrigation, balanced fertilization and regular monitoring.",
    "management": "Maintain current good agricultural practices."
}

}

def get_disease_info(disease):

    # =====================================================
    # HANDLE EMPTY VALUE
    # =====================================================

    if disease is None:

        return {
            "symptoms": "No disease prediction available.",
            "cause": "The AI model did not return a valid disease name.",
            "prevention": "Upload a clear image of a single plant leaf.",
            "management": "Try another high-quality image."
        }


    # Convert to string
    disease = str(disease).strip()


    # =====================================================
    # EXACT MATCH
    # =====================================================

    if disease in DISEASE_INFO:

        return DISEASE_INFO[disease]


    # =====================================================
    # REMOVE EXTRA SPACES
    # =====================================================

    normalized_disease = disease.replace(
        " ",
        "_"
    )


    if normalized_disease in DISEASE_INFO:

        return DISEASE_INFO[
            normalized_disease
        ]


    # =====================================================
    # CASE INSENSITIVE MATCH
    # =====================================================

    disease_lower = disease.lower()


    for key, value in DISEASE_INFO.items():

        if disease_lower == key.lower():

            return value


    # =====================================================
    # REMOVE SPECIAL CHARACTERS
    # =====================================================

    disease_clean = (
        disease.lower()
        .replace(" ", "")
        .replace("_", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
        .replace(",", "")
    )


    for key, value in DISEASE_INFO.items():

        key_clean = (
            key.lower()
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace(",", "")
        )


        if disease_clean == key_clean:

            return value


    # =====================================================
    # PARTIAL MATCHING
    # =====================================================

    for key, value in DISEASE_INFO.items():

        key_lower = key.lower()


        if disease_lower in key_lower:

            return value


        if key_lower in disease_lower:

            return value


    # =====================================================
    # FALLBACK
    # =====================================================

    readable_disease = (
        disease
        .replace("___", " - ")
        .replace("_", " ")
    )


    return {

        "symptoms":
        "Detailed symptoms are currently not available for this disease.",

        "cause":
        f"The AI detected '{readable_disease}', but this disease "
        "is not yet present in the disease information database.",

        "prevention":
        "Maintain field hygiene, proper irrigation, crop monitoring "
        "and remove severely infected plant material.",

        "management":
        "Consult a local agricultural expert for confirmation and "
        "appropriate treatment recommendations."
    }