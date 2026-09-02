# 🌾 AgriMind AI - Smart Agriculture Intelligence Platform

<div align="center">

![AgriMind AI](https://img.shields.io/badge/AgriMind-AI%20Agriculture-success?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20Application-red?style=for-the-badge&logo=streamlit)
![Machine Learning](https://img.shields.io/badge/AI-Machine%20Learning-orange?style=for-the-badge)
![NLP](https://img.shields.io/badge/NLP-Sentence%20Transformers-purple?style=for-the-badge)

### An AI-Powered Smart Agriculture Platform for Crop Disease Detection, Yield Prediction, Weather Analysis and Farmer Assistance

</div>

---

# 📌 About The Project

**AgriMind AI** is an AI-powered Smart Agriculture Intelligence Platform designed to help farmers and agriculture enthusiasts make better and data-driven decisions.

The platform combines multiple Artificial Intelligence technologies such as Machine Learning, Natural Language Processing, Computer Vision, Semantic Search, and Weather APIs into a single interactive web application.

AgriMind AI can help users detect plant diseases from leaf images, predict crop yield based on agricultural parameters, analyze crop symptoms using Natural Language Processing, provide weather information, and answer agriculture-related questions through an intelligent AI chatbot.

The project focuses on making modern AI technology simple and accessible for farmers and agricultural users through an easy-to-use web interface.

---

# 🚀 Key Features

## 🌿 Crop Disease Detection

The system allows users to upload an image of a plant or leaf.

The AI model analyzes the image and predicts the possible disease affecting the crop.

### Features:

- Upload plant leaf images.
- AI-based disease detection.
- Crop disease classification.
- Disease prediction with confidence score.
- Identification of healthy and diseased leaves.
- Automatic disease information display.
- Prevention and treatment suggestions.

Example supported predictions include:

- Tomato Early Blight
- Tomato Late Blight
- Healthy Tomato Leaf
- Other supported crop diseases.

---

## 🦠 Disease Information System

After detecting a crop disease, the platform provides detailed information about the detected disease.

The information includes:

- Disease name.
- Disease description.
- Causes of the disease.
- Common symptoms.
- Prevention methods.
- Recommended treatment.
- Agricultural management practices.

This feature helps users understand not only the detected disease but also how to prevent and manage it.

---

## 🌾 Crop Yield Prediction

The Crop Yield Prediction module uses Machine Learning algorithms to estimate crop production.

The prediction is based on multiple agricultural and environmental parameters.

### Input Parameters Include:

- Crop Type
- Region
- Season
- Soil pH
- Soil Moisture
- Average Temperature
- Total Rainfall
- Fertilizer Amount
- Pesticide Usage
- Sunlight Hours
- Nitrogen Content
- Phosphorus Content
- Potassium Content
- Irrigation Frequency
- Harvest Year
- Harvest Month

### Output:

- Predicted Crop Yield
- Yield estimation in tons per hectare

This module helps farmers understand the possible productivity of their crops based on environmental and agricultural conditions.

---

# 🧠 Agriculture Symptom Analysis

AgriMind AI includes an intelligent Natural Language Processing system that analyzes agricultural problems described by users.

Users can enter symptoms in natural language such as:

> "My tomato leaves are turning yellow and have brown spots."

The NLP system analyzes the sentence and predicts the possible agricultural problem.

### Features:

- Natural language symptom input.
- Semantic text analysis.
- Agriculture problem classification.
- AI-based symptom prediction.
- Confidence score.
- Intelligent disease identification.

The system uses Sentence Transformers to understand the meaning of user queries instead of relying only on keyword matching.

---

# 🤖 AI Agriculture Chatbot

AgriMind AI includes an intelligent agriculture chatbot that can answer user questions related to farming and crop management.

The chatbot can assist users with questions about:

- Crop diseases.
- Plant care.
- Fertilizers.
- Irrigation.
- Soil management.
- Pest control.
- Crop production.
- General agriculture practices.

The chatbot provides an interactive conversational experience directly inside the AgriMind AI platform.

---

# 🌦️ Weather Information

The platform provides weather-related information that can help farmers understand environmental conditions.

Weather information can include:

- Current temperature.
- Weather conditions.
- Location information.
- Coordinates.
- Weather descriptions.

This information can help farmers make better decisions regarding irrigation, crop care, and farming activities.

---

# 🧠 Technologies Used

## Programming Language

- Python

## Web Framework

- Streamlit

## Machine Learning

- Scikit-learn
- Joblib
- NumPy
- Pandas

## Natural Language Processing

- Sentence Transformers
- all-MiniLM-L6-v2
- Semantic Similarity
- Text Classification

## Data Visualization

- Matplotlib
- Seaborn

## APIs and Services

- Weather API
- Geolocation Services
- AI/LLM Integration

---

# 🏗️ Project Architecture

```text
AgriMind AI
│
├── app.py
│
├── modules
│   ├── disease_detection.py
│   ├── disease_info.py
│   ├── yield_prediction.py
│   ├── agriculture_nlp.py
│   ├── chatbot.py
│   └── weather.py
│
├── models
│   ├── agriculture_classifier.pkl
│   ├── yield_prediction_model.pkl
│   └── other trained models
│
├── datasets
│   ├── agriculture_symptoms.csv
│   └── crop yield dataset
│
├── assets
│   └── images and UI resources
│
├── requirements.txt
│
└── README.md
