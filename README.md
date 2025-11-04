# 🧠 Text Analysis (Gemini)

This project is a **Flask web application** integrated with **n8n workflow automation** and **Google Gemini API** to perform text summarization and sentiment analysis. The front-end allows users to input text and select the analysis mode, while the back-end securely communicates with the n8n workflow.

---

## 🚀 Features

* Clean and responsive UI (HTML + CSS)
* Flask backend for handling requests securely
* n8n workflow integration for Gemini API calls
* API Key authentication via headers (hidden from client)
* Supports **Summary** and **Sentiment Analysis** modes

---

## 🧩 Project Structure

```
project_root/
├── app.py
├── templates/
│   └── index.html
├── Text Analysis (Gemini) - with mode selection.json
├── .env
├── requirements.txt
└── README.md
```

---

## ⚙️ .env Configuration

Create a `.env` file in the project root and add:

```bash
N8N_WEBHOOK_URL=https://your-n8n-instance-url/webhook/text-analysis
API_KEY=your-secret-header-api-key
GEMINI_API_KEY=your-google-gemini-api-key
```


---

## 🧠 n8n Workflow Setup

### 1. Create a Webhook Node

* **Node Type:** Webhook
* **HTTP Method:** POST
* **Path:** `text-analysis`
* **Response Mode:** Response Node
* **Authentication:** Header Auth (set API Key in credentials)

### 2. Add HTTP Request Node (Gemini)

* **Method:** POST
* **URL:**

  ```
  https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={{$env.GEMINI_API_KEY}}
  ```
* **Body Type:** JSON
* **Body Content:**

  ```json
  {
    "contents": [
      {
        "role": "user",
        "parts": [
          {
            "text": "Perform a {{$json.body.mode}} of the following text:\n {{$json.body.text_to_analyze}}"
          }
        ]
      }
    ]
  }
  ```

### 3. Add a Set Node

* Keep only the key `final_result`
* Value:

  ```
  {{$json["candidates"]?.[0]?.content?.parts?.[0]?.text || $json["outputText"] || ''}}
  ```

### 4. Add Respond to Webhook Node

* Connect to the previous node.
* Sends the processed `final_result` back to Flask.

### 5. Save and Activate Workflow

---

## 💻 Flask Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the application

```bash
python app.py
```

### 3. Access locally

Visit [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🧪 Example API Request

**Endpoint:** `/analyze`

**Request:**

```json
{
  "text": "AI will revolutionize the world.",
  "mode": "sentiment analysis"
}
```

**Response:**

```json
{
  "final_result": "The sentiment is positive and optimistic."
}
```

