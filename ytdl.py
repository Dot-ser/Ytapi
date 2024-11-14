import aiohttp
from aiohttp import web
import yt_dlp

async def download_song(request):
    data = await request.json()
    url = data.get('url')
    
    if not url:
        return web.json_response({'error': 'URL is required'}, status=400)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return web.json_response({'status': 'Download successful'})
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)

app = web.Application()
app.router.add_post('/download', download_song)

if __name__ == '__main__':
    web.run_app(app, port=8080)
