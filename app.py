import os
import tempfile
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import instaloader
from methods import *
from config import config

app = Flask(__name__)

# Global variable to store the temp image list
image_paths     = []
temp_dir        = tempfile.TemporaryDirectory()
TEMP_PATH       = temp_dir.name

@app.route('/', methods=['GET', 'POST'])
def index():
    global image_paths
    image_paths = []
    if request.method == 'POST':
        config.username     = request.form['username']
        config.post_limit   = int(request.form['posts'])

        # 🧹 Clear the temp folder
        for file in os.listdir(TEMP_PATH):
            os.remove(os.path.join(TEMP_PATH, file))

        loader = instaloader.Instaloader(
            dirname_pattern=temp_dir.name,
            download_pictures=True,
            download_videos=False,
            save_metadata=False,
            download_video_thumbnails=False,
            download_comments=False,
            download_geotags=False,
            quiet=True
        )

        try:    loader.load_session_from_file("gskumardot")
        except: return "Session load failed. Login manually first using instaloader CLI."

        try:    download_profile_posts(loader, config)
        except Exception as e:
            return f"Error: {e}"

        # Get only image files (ignore videos, JSONs, etc.)
        for file in os.listdir(temp_dir.name):
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(file)

        return redirect(url_for('show_images'))

    return render_template('index.html')

@app.route('/images')
def show_images():
    return render_template('gallery.html', images=image_paths)

@app.route('/temp/<filename>')
def serve_temp_file(filename):
    return send_from_directory(temp_dir.name, filename)

if __name__ == '__main__':
    app.run(debug=True)
