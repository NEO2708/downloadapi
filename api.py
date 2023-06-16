from flask import Flask, request, jsonify
import instaloader
import youtube_dl
from flask_cors import CORS
from fastapi.responses import FileResponse
from pytube import YouTube


app = Flask(__name__)
cors = CORS(app)


@app.route('/', methods=['GET'])
def download_video():
    inputt = request.args['link']

    if(inputt != ""):
        video_url = inputt
        yt = YouTube(video_url)
        regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
        name = yt.title
        # regex = (r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$\n")
        print(video_url)

        ydl_opts = {}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                video_url, download=False)
        video_audio_streams = []
        for m in meta['formats']:
            file_size = m['filesize']
            if file_size is not None:
                file_size = f'{round(int(file_size) / 1000000,2)} mb'

            resolution = 'Audio'
            if m['height'] is not None:
                resolution = f"{m['height']}x{m['width']}"
            video_audio_streams.append({
                'resolution': resolution,
                'extension': m['ext'],
                'file_size': file_size,
                'video_url': m['url']
            })
        yt = YouTube(video_url)
        yd = yt.streams.get_by_resolution(resolution="360p")
        yd.download("/Users/rangolivision/Desktop/code/web-ytmp3-ins/ytd/360p/")
        # yd = yt.streams.get_by_itag(itag="135")
        # filesize = yd.filesize_mb
        # yd.download("/Users/rangolivision/Desktop/code/web-ytmp3-ins/ytd/480p/")
        yd = yt.streams.get_by_resolution(resolution="720p")
        filesize = yd.filesize_mb
        yd.download("/Users/rangolivision/Desktop/code/web-ytmp3-ins/ytd/720p/")
        yd = yt.streams.get_by_itag(itag="137")
        filesize = yd.filesize_mb
        yd.download(
            "/Users/rangolivision/Desktop/code/web-ytmp3-ins/ytd/1080p/")
        yd = yt.streams.get_audio_only()
        yd.download(
            "/Users/rangolivision/Desktop/code/web-ytmp3-ins/ytd/audio/")
        video_audio_streams = video_audio_streams[::-1]
    context = {

        'title': meta['title'],
        'description': meta['description'], 'likes': meta['like_count'],
        'dislikes': meta['dislike_count'], 'thumb': meta['thumbnails'][3]['url'],
        'duration': round(int(meta['duration'])/60, 2), 'views': f'{int(meta["view_count"]):,}'
    }

    return jsonify({'title': meta['title'], 'name': name,
                    'description': meta['description'], 'likes': meta['like_count'],
                    'dislikes': meta['dislike_count'], 'thumb': meta['thumbnails'][3]['url'],
                    'duration': round(int(meta['duration'])/60, 2), 'views': f'{int(meta["view_count"]):,}'
                    })


@app.route('/insta', methods=['GET'])
def download_post():
    L = instaloader.Instaloader()
    inputt = request.args['link']
    url = inputt
    post = instaloader.Post.from_shortcode(
        L.context, url.split("/")[-2])
    username = post.owner_username
    likes = post.likes
    isv = post.is_video

    # Download the post
    a = L.download_post(post, target="downloads")
    print(a)

    return jsonify({
        'usernmae': username,
        'likes': likes,
    })


if __name__ == '__main__':
    app.run()
