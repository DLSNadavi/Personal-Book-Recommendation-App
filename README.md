# BookBuddy 📚

**Your Personal Book Recommendation App**

BookBuddy is a simple, interactive Streamlit web app that helps users discover book recommendations tailored to their favorite genres. Select a genre and instantly receive a curated list of popular titles and authors!

---

## 🚀 Features

- **Genre-Based Recommendations:** Choose from a variety of genres and get 6 personalized book suggestions.
- **Clean, Modern UI:** Stylish cards for easy browsing.
- **Lottie Animation:** Enjoy a welcoming animation on the homepage.
- **No Database Needed:** Uses a hardcoded list of popular titles for reliability and speed.
- **Session State:** Remembers your preferences and recommendations during your session.

---

## 🛠️ Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/bookbuddy.git
    cd bookbuddy
    ```

2. **Install dependencies:**
    ```bash
    pip install streamlit streamlit-lottie requests
    ```

---

## ▶️ Usage

1. **Run the app:**
    ```bash
    streamlit run app.py
    ```

2. **Open your browser** to the provided local URL (typically `http://localhost:8501`).

---

## 📒 How to Use

1. **Select your favorite genre** from the dropdown menu on the left.
2. **Click "Get Recommendations"** to generate personalized book recommendations.
3. **Browse your book list** and discover new reads!

---

## 📂 Project Structure

```
bookbuddy/
├── app.py              # Main Streamlit application file
├── README.md           # Project documentation
├── requirements.txt    # Python dependencies (optional)
└── demo_screenshot.png # Demo screenshot (optional)
```

---

## 🔗 Dependencies

- [Streamlit](https://streamlit.io/)  
- [streamlit-lottie](https://github.com/andfanilo/streamlit-lottie)  
- [requests](https://pypi.org/project/requests/)

Install all dependencies with:
```bash
pip install streamlit streamlit-lottie requests
```

---

## 📝 Customization

- **Genres & Books:**  
  Edit the `genre_recommendations` dictionary in `app.py` to add or change genres and recommended books.

- **Styling:**  
  Tweak the CSS in `app.py` within `st.markdown("""<style>...</style>""", unsafe_allow_html=True)` for custom styles.

---

## ❤️ Credits

Made with ❤️ by DLSN | © 2025

---
