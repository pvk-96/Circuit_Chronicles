# 🏎️ About Circuit Chronicles

**Circuit Chronicles** is an advanced Formula 1 data analysis platform built for fans, engineers, students, and enthusiasts who want deeper insights into F1 sessions.

It uses the **FastF1 API** to load timing, telemetry, driver data, race sessions, and more — then visualizes everything through **Streamlit** with a sleek dark-blue theme inspired by modern F1 broadcast design.

---

# 🌟 Features

### 🔧 **Core Features**
- **Grand Prix Selector**  
  Easily browse events by season and choose any race weekend session.

- **Session Summary**  
  Displays podium results, finishing times, fastest laps, team names, and key session information.

- **Driver Highlight Panel**  
  Shows:
  - fastest lap  
  - average lap  
  - total laps  
  - full lap breakdown with sector times  

- **Telemetry Comparison**  
  Compare two drivers lap-by-lap using:
  - speed traces  
  - throttle & brake inputs  
  - gear usage  
  - distance-based graphs  

- **Lap Time Analysis**
  - Full lap charts  
  - Pit lap removal  
  - Pace trendline  
  - Supports all practice, quali, and race sessions  

- **Position Evolution Graph**
  - Visualizes race position lap-by-lap  
  - Useful for understanding race pace & strategy  

- **Battle Gap Graph**
  - Shows real-time lap gaps between two drivers  
  - Helps identify close fights and pace trends  

- **Overtake Detector**
  - Automatically detects overtakes  
  - Shows lap number, old position → new position  
  - Presents a clean list of passes during the race  

### 🎨 **Branding & UI**
- Fully customized black & electric-blue UI  
- Animated **F1 car loading screen**  
- Clean card-based layout  
- Custom Streamlit theme  
- Dark tables, glowing accents, modern visual identity  

---

# 📂 Project Structure

```

Circuit_Chronicles/
│
├── app.py                    # Main Streamlit app
├── assets/
│   ├── style.css             # Global UI theme
│   ├── logo.png              # App logo
│   └── ...
│
├── components/               # Modular UI components
│   ├── session_summary.py
│   ├── lap_analysis.py
│   ├── telemetry_compare.py
│   ├── driver_highlight.py
│   ├── lap_time_chart.py
│   ├── battle_gap.py
│   ├── overtake_detector.py
│   └── ...
│
├── utils/
│   ├── f1_loader.py          # Session + lap loading utilities
│   ├── cache.py              # FastF1 cache setup
│   ├── flags.py              # GP flag mapping
│   └── ...
│
├── requirements.txt
└── README.md

````

---

# 🛠️ Tech Stack

### **Frontend / UI**
- Streamlit  
- Custom CSS  
- Plotly  

### **Backend / Data**
- FastF1  
- Pandas  
- NumPy  

### **Branding**
- Custom animation loader  
- Electric blue/black visual theme  
- Modular components  

---

# 🔧 Installation

### 1️⃣ Clone the repo
```bash
git clone https://github.com/pvk-96/Circuit_Chronicles.git
cd Circuit_Chronicles
````

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux & macOS
# OR
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the App Locally

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

# 🙌 Credits

* **FastF1** for data access
* **Streamlit** for UI platform
* **PVK** — Creator of Circuit Chronicles
* Community contributors

---

# 📄 License

This project is licensed under the **MIT License.**
Free for personal and commercial use.

---

<p align="center">
  Made with ❤️, FastF1, and way too much coffee.
</p>
```

