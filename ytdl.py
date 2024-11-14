from flask import Flask, request, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def index():
    return '''
        <h1>Download YouTube Songs</h1>
        <form action="/download" method="post">
            <label for="url">YouTube URL:</label>
            <input type="text" id="url" name="url">
            <input type="submit" value="Download">
        </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    cookies = request.cookies.get('yt_cookies')

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookiefile': cookies  # Use cookies from the visitor
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    app.run(host='0.0.0.0', port=5000, debug=True)

