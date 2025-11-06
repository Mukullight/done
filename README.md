# 📊 Aider Polyglot Dashboard


---

## 🚀 Features

- 📈 Interactive charts for model performance and trading analytics  
- 🧩 Modular Dash page system (`dashboard/pages/`)  
- 🎨 Custom HTML embeds (supports static visualizations in `/graphs/`)  
- 💡 Dark theme with Bootstrap styling  
- ⚙️ Easily extensible architecture for adding new metrics and pages  

---

## 🗂️ Project Structure

```
dashboard/
│
├── main.py # App entry point
├── utils.py # Global constants (e.g. TITLE)
├── pages/ # Dash multipage components
│ ├── index.py # Landing page
│ ├── pricing.py # Example pricing visualization
│ └── aider_polyglot_dashboard.py # Model benchmark viewer
│
├── graphs/ # HTML/Plotly visualizations embedded in pages
│ ├── aider_polyglot_dashboard.html
│ └── ...
│
└── assets/ 
```


---

## 🧩 Installation

Make sure you have **Python 3.9+** installed.

```bash
# Clone the repository
git clone https://github.com/yourusername/aider_polyglot_dashboard.git
cd aider_polyglot_dashboard

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows

# Install dependencies
pip install -r requirements.txt


```

## docker file 

```bash

## 🐳 Run with Docker

You can build and run the dashboard using Docker for a fully isolated environment.

### 1️⃣ Build the Docker Image

docker build -t aider-polyglot-dashboard .

### Run the container

docker run -p 8050:8050 aider-polyglot-dashboard

```

🪪 License

This project is licensed under the MIT License see the LICENSE

👤 Author

Mukul Namagiri

📧 mukulnamagiri1@gmail.com

