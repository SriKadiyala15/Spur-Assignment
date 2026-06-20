# AI Support Agent

An AI-powered customer support chatbot built using **React + FastAPI + Gemini AI** that helps users get instant answers to common ecommerce-related questions such as shipping, returns, refunds, and support availability.

---

## Features

* Real-time AI-powered chatbot
* Smart responses using Google Gemini API
* Handles ecommerce FAQs
* Chat history support using session-based conversations
* Stores conversations in SQLite database
* Responsive frontend with clean chat UI
* Backend deployed on Render
* Frontend deployed on Vercel

---

## Tech Stack

### Frontend

* React.js
* Vite
* Axios
* CSS

### Backend

* FastAPI
* Python
* SQLAlchemy
* SQLite
* Uvicorn

### AI Integration

* Google Gemini API

### Deployment

* Frontend: Vercel : https://spur-assignment-gilt.vercel.app/
* Backend: Render : https://spur-assignment-v9of.onrender.com/

---

## Project Structure

```bash
Spur-Assignment/
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   └── package.json
│
└── backend/
    ├── main.py
    ├── ai_service.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    ├── requirements.txt
    └── .env
```

---

## Supported FAQs

* Shipping Policy
* Return Policy
* Refund Policy
* Support Timings
* USA Shipping Availability

---

## Future Improvements

* User authentication
* Multi-language support
* Live agent handoff
* Better UI animations
* Advanced conversation memory

