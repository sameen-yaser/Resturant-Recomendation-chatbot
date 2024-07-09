import tkinter as tk
from tkinter import ttk
import pandas as pd
import spacy

# Load spaCy's English model
nlp = spacy.load("en_core_web_sm")

# Load your modified dataset
df = pd.read_csv('modified_swiggy.csv')

# Convert 'cost' column to string if it's not already
df['cost'] = df['cost'].astype(str)

def categorize_price_range(cost):
    cost = int(cost)
    if cost < 200:
        return 'Low'
    elif 200 <= cost < 400:
        return 'Medium'
    else:
        return 'High'

# Apply the categorization function to create a new 'price_category' column
df['price_category'] = df['cost'].apply(categorize_price_range)

def process_user_input(city, price_range, cuisine):
    # Filter restaurants based on the selected city and price range
    available_cuisines = df[(df['city'] == city)]['cuisine'].unique()

    # Check if the selected cuisine is valid
    if cuisine and cuisine not in available_cuisines:
        print(f"Invalid cuisine '{cuisine}'. Please choose from {', '.join(available_cuisines)} or leave it blank.")
        return "Invalid cuisine"

    # Filter restaurants based on the 'price_category', 'cuisine', and 'city' columns
    if price_range.lower() in ['low', 'medium', 'high']:
        if cuisine:
            recommended_restaurants = df[(df['price_category'] == price_range) & (df['city'] == city) & (df['cuisine'] == cuisine)]
        else:
            recommended_restaurants = df[(df['price_category'] == price_range) & (df['city'] == city)]

        # Display restaurant names and information with formatting
        if not recommended_restaurants.empty:
            result_str = f"Here are some recommended restaurants in {city} with {cuisine} cuisine:\n\n"
            for index, row in recommended_restaurants.iterrows():
                result_str += f"Name: {row['name']}\n"
                result_str += f"Cuisine: {row['cuisine']}\n"
                result_str += f"Address: {row['address']}\n"
                result_str += f"Rating: {row['rating']} (Based on {row['rating_count']} ratings)\n"
                result_str += "\n"  # Add a separator between restaurants

            return result_str
        else:
            return "Apologies, no matching restaurants found based on your preferences."
    else:
        return "Invalid price range. Please choose from 'Low', 'Medium', or 'High'."

def get_recommendations():
    # Fetch user inputs from entry widgets
    city = city_entry.get()
    price_range = price_entry.get()
    cuisine = cuisine_entry.get()

    # Process user input (replace this with your chatbot logic)
    recommendations = process_user_input(city, price_range, cuisine)

    # Display recommendations in the text widget with enhanced styling
    result_text.config(state=tk.NORMAL, font=('Times New Roman', 12), background='#FFB6C1', foreground='black')  # Modify font and colors
    result_text.delete("1.0", tk.END)  # Clear previous text
    result_text.insert(tk.END, recommendations)
    result_text.config(state=tk.DISABLED)  # Disable editing

# GUI setup
root = tk.Tk()
root.title("Restaurant Recommendation Chatbot")
root.configure(bg='#FFB6C1')  # Set background color to light pink

# Labels for user input
tk.Label(root, text="Which city are you in?", bg='#FFB6C1').grid(row=0, column=0, pady=5, sticky=tk.W)
tk.Label(root, text="What's your preferred price range?", bg='#FFB6C1').grid(row=1, column=0, pady=5, sticky=tk.W)
tk.Label(root, text="What type of cuisine are you interested in?", bg='#FFB6C1').grid(row=2, column=0, pady=5, sticky=tk.W)

# Entry widgets for user input
city_entry = tk.Entry(root, width=30)
price_entry = tk.Entry(root, width=30)
cuisine_entry = tk.Entry(root, width=30)

# Button to trigger recommendations
submit_button = tk.Button(root, text="Get Recommendations", command=get_recommendations, bg='#4CAF50', fg='white')

# Text widget to display recommendations
result_text = tk.Text(root, width=50, height=10, state=tk.DISABLED, bg='#FFB6C1')

# Layout
city_entry.grid(row=0, column=1, pady=5)
price_entry.grid(row=1, column=1, pady=5)
cuisine_entry.grid(row=2, column=1, pady=5)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)
result_text.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.W)

# Run the Tkinter main loop
root.mainloop()
