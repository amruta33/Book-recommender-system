from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the necessary pickle files (assuming you have them)
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    return render_template('recommend.html', data=data)

# Route to handle book details
@app.route('/book/<book_name>')
def book_detail(book_name):
    # Fetch the book data from the books DataFrame
    book_data = books[books['Book-Title'] == book_name]
    
    # If no book is found with that title, return a 404 page
    if book_data.empty:
        return "Book not found", 404

    # Extract relevant details
    book_data = book_data.iloc[0]  # Assuming there's only one match for the book title
    return render_template('book_detail.html',
                           title=book_data['Book-Title'],
                           author=book_data['Book-Author'],
                           yearofpub=book_data['Year-Of-Publication'],
                           publisher=book_data['Publisher'],
                           
                           
                           image=book_data['Image-URL-M'])  

if __name__ == '__main__':
    app.run(debug=True)
