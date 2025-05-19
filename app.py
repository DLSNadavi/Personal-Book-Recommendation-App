import streamlit as st
import re
import random
from streamlit_lottie import st_lottie
import requests

# === Memory storage ===

if 'user_preferences' not in st.session_state:
    st.session_state['user_preferences'] = {}
if 'recommendations' not in st.session_state:
    st.session_state['recommendations'] = []
# Removed 'selected_book' session state as we no longer need it

# === Helper functions ===

def load_lottie_url(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None
    return None

def extract_title_author(book_string):
    """Extract title and author from a book string format 'Title by Author'"""
    parts = book_string.split(' by ', 1)
    if len(parts) == 2:
        return {'title': parts[0].strip(), 'author': parts[1].strip()}
    return {'title': book_string, 'author': 'Unknown'}

def get_recommendations(preferences):
    """
    Generate book recommendations based on genre preferences.
    Uses a hardcoded list of popular books for reliability.
    Returns a list of dictionaries with title and author.
    """
    genre_recommendations = {
        "fantasy": [
            "The Name of the Wind by Patrick Rothfuss",
            "A Game of Thrones by George R.R. Martin",
            "The Way of Kings by Brandon Sanderson",
            "The Fifth Season by N.K. Jemisin",
            "Mistborn: The Final Empire by Brandon Sanderson",
            "The Blade Itself by Joe Abercrombie",
            "Assassin's Apprentice by Robin Hobb",
            "The Night Circus by Erin Morgenstern",
            "Jonathan Strange & Mr Norrell by Susanna Clarke",
            "Uprooted by Naomi Novik",
            "The Lies of Locke Lamora by Scott Lynch",
            "The Hobbit by J.R.R. Tolkien",
            "The Priory of the Orange Tree by Samantha Shannon"
        ],
        "science fiction": [
            "Dune by Frank Herbert",
            "Foundation by Isaac Asimov",
            "Hyperion by Dan Simmons",
            "The Three-Body Problem by Liu Cixin",
            "Ancillary Justice by Ann Leckie",
            "Neuromancer by William Gibson",
            "The Left Hand of Darkness by Ursula K. Le Guin",
            "Snow Crash by Neal Stephenson",
            "Ender's Game by Orson Scott Card",
            "The Martian by Andy Weir",
            "Ready Player One by Ernest Cline",
            "Altered Carbon by Richard K. Morgan"
        ],
        "mystery": [
            "The Girl with the Dragon Tattoo by Stieg Larsson",
            "Gone Girl by Gillian Flynn",
            "The Da Vinci Code by Dan Brown",
            "In the Woods by Tana French",
            "Big Little Lies by Liane Moriarty",
            "The Silent Patient by Alex Michaelides",
            "The Hound of the Baskervilles by Arthur Conan Doyle",
            "The Woman in White by Wilkie Collins",
            "And Then There Were None by Agatha Christie",
            "The Maltese Falcon by Dashiell Hammett",
            "Sharp Objects by Gillian Flynn",
            "The Name of the Rose by Umberto Eco"
        ],
        "romance": [
            "Pride and Prejudice by Jane Austen",
            "Outlander by Diana Gabaldon",
            "The Notebook by Nicholas Sparks",
            "Me Before You by Jojo Moyes",
            "The Time Traveler's Wife by Audrey Niffenegger",
            "Jane Eyre by Charlotte Brontë",
            "The Rosie Project by Graeme Simsion",
            "The Fault in Our Stars by John Green",
            "Red, White & Royal Blue by Casey McQuiston",
            "Eleanor Oliphant Is Completely Fine by Gail Honeyman",
            "It Ends with Us by Colleen Hoover",
            "The Hating Game by Sally Thorne"
        ],
        "thriller": [
            "The Girl on the Train by Paula Hawkins",
            "The Silence of the Lambs by Thomas Harris",
            "Shutter Island by Dennis Lehane",
            "Before I Go to Sleep by S.J. Watson",
            "The Woman in the Window by A.J. Finn",
            "The Da Vinci Code by Dan Brown",
            "The Hunt for Red October by Tom Clancy",
            "The Bourne Identity by Robert Ludlum",
            "The Firm by John Grisham",
            "Gone Girl by Gillian Flynn",
            "The Secret History by Donna Tartt",
            "I Am Pilgrim by Terry Hayes"
        ],
        "horror": [
            "It by Stephen King",
            "The Shining by Stephen King",
            "Bird Box by Josh Malerman",
            "The Haunting of Hill House by Shirley Jackson",
            "Dracula by Bram Stoker",
            "Frankenstein by Mary Shelley",
            "The Exorcist by William Peter Blatty",
            "World War Z by Max Brooks",
            "Pet Sematary by Stephen King",
            "House of Leaves by Mark Z. Danielewski",
            "Mexican Gothic by Silvia Moreno-Garcia",
            "NOS4A2 by Joe Hill"
        ],
        "non-fiction": [
            "Sapiens: A Brief History of Humankind by Yuval Noah Harari",
            "Educated by Tara Westover",
            "Becoming by Michelle Obama",
            "The Immortal Life of Henrietta Lacks by Rebecca Skloot",
            "Thinking, Fast and Slow by Daniel Kahneman",
            "Born a Crime by Trevor Noah",
            "Quiet: The Power of Introverts by Susan Cain",
            "The Glass Castle by Jeannette Walls",
            "Outliers by Malcolm Gladwell",
            "Man's Search for Meaning by Viktor E. Frankl",
            "The Power of Habit by Charles Duhigg",
            "A Brief History of Time by Stephen Hawking"
        ],
        "historical fiction": [
            "All the Light We Cannot See by Anthony Doerr",
            "The Book Thief by Markus Zusak",
            "The Nightingale by Kristin Hannah",
            "Wolf Hall by Hilary Mantel",
            "The Pillars of the Earth by Ken Follett",
            "The Help by Kathryn Stockett",
            "A Gentleman in Moscow by Amor Towles",
            "The Other Boleyn Girl by Philippa Gregory",
            "Outlander by Diana Gabaldon",
            "The Tattooist of Auschwitz by Heather Morris",
            "Memoirs of a Geisha by Arthur Golden",
            "Circe by Madeline Miller"
        ]
    }

    # Extract genre from preferences string
    genre = None
    if 'genre' in preferences.lower():
        genre_match = re.search(r'genre:\s*([^,]+)', preferences.lower())
        if genre_match:
            genre = genre_match.group(1).strip().lower()

    # Find the closest matching genre
    matching_genre = None
    for key in genre_recommendations.keys():
        if genre and key in genre:
            matching_genre = key
            break

    # Get recommendations based on genre
    if matching_genre:
        recs = list(genre_recommendations[matching_genre])
        random.shuffle(recs)
        # Convert to list of dictionaries with title and author
        return [extract_title_author(recs[i]) for i in range(min(6, len(recs)))]
    else:
        # No default recommendations; return empty list
        return []

def update_preferences(new_preferences):
    """
    Update user preferences in session state
    """
    st.session_state['user_preferences'] = new_preferences
    
    # Generate new recommendations based on updated preferences
    st.session_state['recommendations'] = get_recommendations(new_preferences)

# Removed show_book_details function since we're removing the view details functionality

# === Main App ===

def main():
    # Set page config
    st.set_page_config(
        page_title="BookBuddy - Your Personal Book Recommender",
        page_icon="📚",
        layout="centered"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .book-card {
        background-color: #f5f5f5;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        transition: transform 0.3s;
    }
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .book-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .book-author {
        font-style: italic;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Load animation
    book_animation = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_1a8dx7zj.json")
    
    # Title and description
    st.title("📚 BookBuddy")
    st.subheader("Your Personal Book Recommendation App")
    
    # Display animation
    if book_animation:
        st_lottie(book_animation, height=200, key="book_anim")
    
    # Create two columns
    col1, col2 = st.columns([1, 2])
    
    # User preferences section (Left column)
    with col1:
        st.markdown("## 📝 Choose Genre")
        
        # User inputs for preferences
        genre_input = st.selectbox(
            "What genre do you enjoy?",
            options=[
                "Fantasy", 
                "Science Fiction", 
                "Mystery", 
                "Romance", 
                "Thriller", 
                "Horror", 
                "Non-Fiction", 
                "Historical Fiction"
            ]
        )
        
        if st.button("Get Recommendations", key="get_recs"):
            # Format preferences as a string - now only contains genre
            preferences_str = f"genre: {genre_input}"
            
            # Update preferences and get new recommendations
            update_preferences(preferences_str)
            st.success("Found books for you!")
    
    # Recommendations section (Right column)
    with col2:
        st.markdown("## 📔 Your Personalized Recommendations")
        
        if st.session_state['recommendations']:
            for i, book in enumerate(st.session_state['recommendations']):
                # Create unique key for each book card
                book_key = f"book_{i}"
                
                # Book card with simplified display - no interactive elements for details
                with st.container():
                    html_content = f"""
                    <div class="book-card" id="{book_key}">
                        <div class="book-title">{book['title']}</div>
                        <div class="book-author">by {book['author']}</div>
                    </div>
                    """
                    st.markdown(html_content, unsafe_allow_html=True)
                    
                    # Add some spacing between book entries
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            if 'user_preferences' in st.session_state and st.session_state['user_preferences']:
                st.info("We couldn't find books matching your preferences. Try a different genre!")
            else:
                st.info("Select your favorite genre to get personalized book recommendations!")
    
    # Footer
    st.markdown("---")
    
    # Help section
    with st.expander("ℹ️ How to use BookBuddy"):
        st.markdown("""
        1. **Select your favorite genre** from the dropdown menu
        2. **Click 'Get Recommendations'** to generate personalized book recommendations
        3. **Enjoy browsing through your personalized book list!**
        """)
    
    st.markdown("Made with ❤️ by DLSN | © 2025")

if __name__ == "__main__":
    main()