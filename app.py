from flask import Flask, render_template, jsonify, request, url_for, redirect
import json

app = Flask(__name__)


# Load blog posts from the JSON file
def load_posts():
    try:
        with open('blog_posts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_posts(posts):
    with open('blog_posts.json', 'w') as file:
        json.dump(posts, file)


# Index Route: Display all blog posts
@app.route('/')
def index():
    blog_posts = load_posts()  # Fetch the blog posts from the JSON file
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')

        # Load the existing blog posts
        blog_posts = load_posts()

        # Generate a unique ID for the new post
        new_id = max([post['id'] for post in blog_posts]) + 1 if blog_posts else 1

        # Create a new blog post dictionary
        new_post = {
            'id': new_id,
            'author': author,
            'title': title,
            'content': content
        }

        # Append the new post to the list
        blog_posts.append(new_post)

        # Save the updated list to the JSON file
        save_posts(blog_posts)

        # Redirect to the index page
        return redirect(url_for('index'))
    # If it's a Get request, render the form
    return render_template('add.html')


# View Single Post Route
@app.route('/post/<int:post_id>')
def view_post(post_id):
    blog_posts = load_posts()
    # Find the post by ID
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post:
        return render_template('post.html', post=post)
    else:
        return 'post not found', 404


@app.route('/delete/<int:post_id>', methods=['post'])
def delete(post_id):
    # load existing posts
    blog_posts = load_posts()

    # Filter out the post to delete
    blog_posts = [post for post in blog_posts if post['id'] != post_id]

    # Save the updated list back to the JSON file
    save_posts(blog_posts)

    # Redirect to the home page
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    blog_posts = load_posts()

    # Find the post to update
    post = next((post for post in blog_posts if post['id'] == post_id), None)

    if post is None:
        return 'Post not found', 404

    if request.method == 'POST':
        # Update the post details with the form data
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')

        # Save the updated posts back to the JSON file
        save_posts(blog_posts)
        return redirect(url_for('index'))

    # Render the update form with the current post data
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
