import csv
import random

random.seed(42)

OUTPUT_FILE = "agriculture_symptoms.csv"

# ============================================================
# AGRICULTURE DISEASE DATA
# 20 diseases × 100 samples = 2,000 samples
# ============================================================

diseases = {

    "Aphid Infestation": {
        "symptoms": [
            "small green insects on young leaves",
            "tiny insects clustered around shoots",
            "curled young leaves",
            "sticky honeydew on foliage",
            "yellowing leaves",
            "ants around the plant",
            "soft bodied insects under leaves",
            "distorted new growth",
            "sticky residue on stems",
            "small insects sucking plant sap"
        ],
        "parts": ["leaves", "young shoots", "stems", "buds"],
        "effects": [
            "plant growth has slowed",
            "new leaves look distorted",
            "the affected foliage is becoming weak",
            "the plant is losing its normal green color",
            "young shoots are not developing normally"
        ]
    },

    "Bacterial Leaf Spot": {
        "symptoms": [
            "small water soaked spots on leaves",
            "dark brown spots on foliage",
            "black lesions on leaves",
            "yellow halos around leaf spots",
            "irregular spots spreading across leaves",
            "tiny dark lesions on young leaves",
            "brown patches surrounded by yellow tissue",
            "leaf spots becoming larger",
            "wet looking lesions on foliage",
            "multiple dark spots on leaves"
        ],
        "parts": ["leaves", "young foliage", "leaf margins", "lower leaves"],
        "effects": [
            "the damaged areas are expanding",
            "infected leaves are drying",
            "leaf tissue is dying around the spots",
            "the plant looks weaker than normal",
            "affected leaves are starting to fall"
        ]
    },

    "Bacterial Wilt": {
        "symptoms": [
            "sudden wilting of the plant",
            "green leaves drooping rapidly",
            "whole plant losing firmness",
            "wilting during the daytime",
            "stem discoloration",
            "rapid plant collapse",
            "branches becoming limp",
            "leaves wilting without obvious dryness",
            "vascular discoloration inside stems",
            "plant remaining wilted after watering"
        ],
        "parts": ["whole plant", "leaves", "stems", "branches"],
        "effects": [
            "the plant does not recover after watering",
            "wilting is spreading quickly",
            "the crop is losing vigor",
            "affected plants may die suddenly",
            "the plant becomes severely weak"
        ]
    },

    "Damping Off": {
        "symptoms": [
            "seedlings collapsing",
            "soft stems near the soil",
            "rotting seedling bases",
            "young plants falling over",
            "dark lesions near the soil line",
            "water soaked seedling stems",
            "seedlings dying soon after emergence",
            "weak stems in young plants",
            "brown tissue around seedling bases",
            "young seedlings suddenly dying"
        ],
        "parts": ["seedlings", "young stems", "seedling roots", "plant base"],
        "effects": [
            "the seedlings cannot stand upright",
            "young plants are dying in patches",
            "growth has stopped",
            "the nursery has many collapsed seedlings",
            "affected seedlings are becoming weak"
        ]
    },

    "Downy Mildew": {
        "symptoms": [
            "yellow patches on leaves",
            "gray fungal growth under leaves",
            "fuzzy growth beneath foliage",
            "pale yellow leaf lesions",
            "angular yellow spots",
            "grayish coating on leaf undersides",
            "yellow areas between leaf veins",
            "moist fungal growth",
            "irregular pale patches",
            "yellowing foliage with gray growth"
        ],
        "parts": ["leaves", "leaf undersides", "young foliage", "lower leaves"],
        "effects": [
            "affected leaves are becoming weak",
            "yellow patches are spreading",
            "infected foliage is drying",
            "plant growth is slowing",
            "leaves are losing their healthy appearance"
        ]
    },

    "Fruit Borer": {
        "symptoms": [
            "holes in fruits",
            "caterpillar inside the fruit",
            "dark entry holes",
            "fruit pulp being eaten",
            "early fruit dropping",
            "insect larvae inside fruits",
            "frass near fruit openings",
            "rotting around insect holes",
            "damaged young fruits",
            "webbing near fruit holes"
        ],
        "parts": ["fruits", "young fruits", "fruit surface", "fruit pulp"],
        "effects": [
            "fruits are becoming damaged",
            "marketable fruit quality is decreasing",
            "affected fruits are rotting",
            "many young fruits are falling",
            "fruit production is being reduced"
        ]
    },

    "Fungal Wilt": {
        "symptoms": [
            "leaves wilting gradually",
            "yellowing foliage",
            "brown discoloration inside stems",
            "plant becoming weak",
            "one side of the plant wilting",
            "lower leaves turning yellow",
            "slow plant decline",
            "drooping leaves",
            "stem tissue becoming brown",
            "persistent wilting"
        ],
        "parts": ["leaves", "stems", "roots", "branches"],
        "effects": [
            "the plant is losing vigor",
            "wilting is becoming more severe",
            "growth is stunted",
            "affected branches are dying",
            "the plant is slowly declining"
        ]
    },

    "Fusarium Wilt": {
        "symptoms": [
            "yellowing of older leaves",
            "one sided wilting",
            "brown vascular tissue",
            "gradual plant wilting",
            "lower leaves becoming yellow",
            "persistent daytime wilt",
            "stem discoloration",
            "leaf curling with wilt",
            "slow decline of the plant",
            "brown streaks inside stems"
        ],
        "parts": ["lower leaves", "stems", "vascular tissue", "whole plant"],
        "effects": [
            "wilting continues even after irrigation",
            "plant growth becomes stunted",
            "affected branches become weak",
            "the plant gradually loses vigor",
            "older leaves begin to die"
        ]
    },

    "Late Blight": {
        "symptoms": [
            "large dark lesions on leaves",
            "water soaked leaf patches",
            "brown lesions spreading quickly",
            "dark spots on stems",
            "white fungal growth during humid weather",
            "rapid leaf browning",
            "blackened foliage",
            "dark patches with pale edges",
            "rotting leaves",
            "brown lesions after wet weather"
        ],
        "parts": ["leaves", "stems", "fruits", "lower foliage"],
        "effects": [
            "the disease is spreading rapidly",
            "leaves are dying quickly",
            "the crop is losing foliage",
            "fruit quality is decreasing",
            "infected plant parts are turning dark"
        ]
    },

    "Leaf Blight": {
        "symptoms": [
            "brown spots on leaves",
            "dark lesions on foliage",
            "leaf edges turning brown",
            "large brown patches",
            "dry patches spreading",
            "blackish marks on leaves",
            "dead tissue on foliage",
            "irregular brown lesions",
            "leaves becoming brittle",
            "drying leaf tips"
        ],
        "parts": ["leaves", "leaf tips", "lower foliage", "leaf margins"],
        "effects": [
            "the damaged area is increasing",
            "leaves are drying",
            "photosynthesis appears reduced",
            "infected foliage is becoming brittle",
            "the crop looks unhealthy"
        ]
    },

    "Leaf Curl": {
        "symptoms": [
            "leaves curling upward",
            "young leaves becoming curled",
            "distorted foliage",
            "leaves rolling inward",
            "twisted shoots",
            "curled leaf margins",
            "narrow distorted leaves",
            "leaves folding along the edges",
            "abnormally curled plant tips",
            "new growth becoming twisted"
        ],
        "parts": ["young leaves", "new shoots", "leaf margins", "plant tips"],
        "effects": [
            "new growth is becoming abnormal",
            "leaves are not expanding normally",
            "plant development is slowing",
            "affected shoots look distorted",
            "the crop is losing healthy foliage"
        ]
    },

    "Mosaic Virus": {
        "symptoms": [
            "mosaic pattern on leaves",
            "light and dark green patches",
            "yellow green leaf markings",
            "mottled foliage",
            "irregular leaf discoloration",
            "distorted leaves",
            "patchy yellow patterns",
            "vein clearing",
            "uneven green coloration",
            "mosaic markings on young leaves"
        ],
        "parts": ["leaves", "young foliage", "new shoots", "plant tips"],
        "effects": [
            "leaf development is abnormal",
            "plant growth is stunted",
            "new leaves are distorted",
            "the crop has uneven coloration",
            "overall plant vigor is reduced"
        ]
    },

    "Nutrient Deficiency": {
        "symptoms": [
            "yellow leaves",
            "pale green foliage",
            "slow plant growth",
            "yellowing between leaf veins",
            "weak stems",
            "stunted plants",
            "older leaves turning yellow",
            "young leaves remaining pale",
            "poor leaf development",
            "uniform leaf discoloration"
        ],
        "parts": ["leaves", "older foliage", "young leaves", "stems"],
        "effects": [
            "plant growth is slower than expected",
            "the crop looks pale",
            "plants remain smaller than normal",
            "leaf development is poor",
            "overall plant vigor is reduced"
        ]
    },

    "Powdery Mildew": {
        "symptoms": [
            "white powder on leaves",
            "white fungal coating",
            "powdery patches on foliage",
            "white growth on stems",
            "dusty layer on leaves",
            "white spots spreading across leaves",
            "powder like substance on foliage",
            "white fungal patches on upper leaves",
            "whitish coating on young shoots",
            "flour like growth on leaves"
        ],
        "parts": ["leaves", "young shoots", "stems", "upper foliage"],
        "effects": [
            "affected leaves are becoming weak",
            "leaf growth is slowing",
            "infected foliage is losing its normal color",
            "new shoots are becoming affected",
            "the white coating is spreading"
        ]
    },

    "Root Rot": {
        "symptoms": [
            "roots turning brown",
            "soft rotten roots",
            "black roots",
            "plant wilting despite watering",
            "bad smell from roots",
            "mushy root tissue",
            "poor root development",
            "roots decaying near soil",
            "dark damaged roots",
            "plant easily pulling from soil"
        ],
        "parts": ["roots", "root tips", "plant base", "underground roots"],
        "effects": [
            "the plant cannot absorb enough water",
            "wilting is becoming severe",
            "plant growth is weak",
            "the crop is losing vigor",
            "affected plants may die"
        ]
    },

    "Rust": {
        "symptoms": [
            "orange spots on leaves",
            "rust colored pustules",
            "reddish brown spots",
            "orange powder under leaves",
            "brown rust marks",
            "yellow orange pustules",
            "rusty patches on foliage",
            "small orange fungal spots",
            "reddish lesions",
            "rust colored dust"
        ],
        "parts": ["leaves", "leaf undersides", "lower foliage", "leaf surfaces"],
        "effects": [
            "infected leaves are becoming weak",
            "rust spots are spreading",
            "foliage is losing its healthy appearance",
            "affected leaves may dry",
            "plant vigor is decreasing"
        ]
    },

    "Sooty Mold": {
        "symptoms": [
            "black coating on leaves",
            "dark fungal layer on foliage",
            "black soot like material",
            "sticky leaves covered with dark mold",
            "black patches on leaf surfaces",
            "dark coating around honeydew",
            "black growth on stems",
            "sooty appearance on foliage",
            "gray black film on leaves",
            "dark mold covering plant surfaces"
        ],
        "parts": ["leaves", "stems", "upper foliage", "plant surfaces"],
        "effects": [
            "leaves receive less sunlight",
            "foliage looks black and dirty",
            "plant growth may become weaker",
            "the coating is spreading",
            "affected leaves have reduced photosynthesis"
        ]
    },

    "Stem Borer": {
        "symptoms": [
            "holes in stems",
            "insect tunnels inside stems",
            "wilting central shoots",
            "dead central shoot",
            "sawdust near stem holes",
            "larvae inside stems",
            "hollow stems",
            "broken stems around bore holes",
            "yellowing above damaged stems",
            "frass coming from stem openings"
        ],
        "parts": ["stems", "central shoots", "main branches", "plant stalks"],
        "effects": [
            "the central shoot is dying",
            "plant growth is interrupted",
            "stems become weak",
            "branches may break easily",
            "the affected plant loses vigor"
        ]
    },

    "Thrips Infestation": {
        "symptoms": [
            "silver streaks on leaves",
            "tiny insects on flowers",
            "scarring on young leaves",
            "leaf curling with insects",
            "brown feeding marks",
            "silvery patches on foliage",
            "damaged flower petals",
            "black specks on leaves",
            "distorted new growth",
            "rough feeding scars"
        ],
        "parts": ["leaves", "flowers", "young shoots", "buds"],
        "effects": [
            "new growth is becoming distorted",
            "flowers are damaged",
            "leaf surfaces have scars",
            "plant growth is slowing",
            "affected foliage is becoming weak"
        ]
    },

    "Whitefly Infestation": {
        "symptoms": [
            "tiny white insects flying around leaves",
            "white insects under leaves",
            "leaf yellowing with whiteflies",
            "sticky leaves",
            "small white flies rising when disturbed",
            "white insects clustered beneath foliage",
            "whitefly nymphs on leaf undersides",
            "sticky honeydew from insects",
            "cloud of white insects",
            "small white insects on plant leaves"
        ],
        "parts": ["leaves", "leaf undersides", "young foliage", "stems"],
        "effects": [
            "leaves are becoming yellow",
            "the plant is losing vigor",
            "sticky honeydew is appearing",
            "new growth is becoming weak",
            "insect numbers are increasing"
        ]
    }
}


# ============================================================
# SENTENCE PATTERNS
# ============================================================

patterns = [
    "The crop shows {symptom}.",
    "I noticed {symptom} in the field.",
    "Several plants have {symptom}.",
    "The farmer reports {symptom}.",
    "During inspection, I found {symptom}.",
    "The plants are showing {symptom}.",
    "There are clear signs of {symptom}.",
    "The affected crop has {symptom}.",
    "Recently the plants developed {symptom}.",
    "I can see {symptom} on the crop.",
    "The field currently has plants with {symptom}.",
    "The leaves or stems show {symptom}.",
    "The crop appears to have {symptom}.",
    "A noticeable problem is {symptom}.",
    "The plants have started showing {symptom}.",
    "After checking the field, I observed {symptom}.",
    "Many plants in the field show {symptom}.",
    "The crop condition includes {symptom}.",
    "The farmer noticed {symptom} yesterday.",
    "There is an increasing problem with {symptom}.",
    "The affected plants are showing {symptom}.",
    "Field inspection revealed {symptom}.",
    "The crop is developing {symptom}.",
    "The main symptom is {symptom}.",
    "The plants currently have {symptom}."
]


# ============================================================
# CREATE 100 UNIQUE SAMPLES PER DISEASE
# ============================================================

all_rows = []

for disease, info in diseases.items():

    disease_rows = set()

    while len(disease_rows) < 100:

        symptom = random.choice(info["symptoms"])
        part = random.choice(info["parts"])
        effect = random.choice(info["effects"])

        pattern = random.choice(patterns)

        sentence = pattern.format(symptom=symptom)

        # Add additional context to make sentences more varied
        variations = [
            sentence,
            sentence[:-1] + f" The affected {part} look unhealthy.",
            sentence[:-1] + f" Plant growth is affected.",
            sentence[:-1] + f" The problem is becoming more noticeable.",
            sentence[:-1] + f" The plant is losing vigor.",
            sentence[:-1] + f" {effect.capitalize()}.",
            sentence[:-1] + f" The problem is visible on the {part}.",
            sentence[:-1] + f" The affected {part} are showing damage.",
            sentence[:-1] + f" Farmers are concerned about the crop condition.",
            sentence[:-1] + f" The symptoms are visible across several plants."
        ]

        text = random.choice(variations)

        disease_rows.add(text)

    for text in disease_rows:
        all_rows.append([disease, text])


# ============================================================
# SHUFFLE DATASET
# ============================================================

random.shuffle(all_rows)


# ============================================================
# VERIFY DATASET
# ============================================================

print("=" * 65)
print("AGRICULTURE SYMPTOMS DATASET GENERATOR")
print("=" * 65)

print("\nTotal diseases:", len(diseases))
print("Samples per disease: 100")
print("Total samples:", len(all_rows))

print("\nDisease distribution:")
counts = {}

for label, text in all_rows:
    counts[label] = counts.get(label, 0) + 1

for label in sorted(counts):
    print(f"{label:25s}: {counts[label]}")


# ============================================================
# SAVE CSV
# ============================================================

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow(["label", "text"])

    writer.writerows(all_rows)


print("\n" + "=" * 65)
print("DATASET CREATED SUCCESSFULLY")
print("=" * 65)

print(f"\nFile: {OUTPUT_FILE}")
print(f"Rows: {len(all_rows)}")
print("Columns: label, text")

print("\nFirst 10 samples:")

for row in all_rows[:10]:
    print(row)

print("\nYou can now use this file for NLP model training.")