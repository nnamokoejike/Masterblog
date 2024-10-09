from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)


# Load blog posts from the JSON file
def load_posts():
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Index Route: Display all blog posts
@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)


if __name__ == '__main__':
    app.run(debug=True)
