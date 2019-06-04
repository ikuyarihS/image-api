from sanic import Sanic, response

from blur_detection_core import blur_check_link
from custom_exceptions import ImageInvalidError, UrlInvalidError

app = Sanic(__name__)


@app.route('/check', methods=['POST'])
async def image_check_api(request):
    if not request.json or 'url' not in request.json:
        return response.text('Error - no url', status=400)

    status = 'OK'
    try:
        score = blur_check_link(request.json['url'])
    except (UrlInvalidError, ImageInvalidError) as e:
        status = str(e)
        score = -1

    return response.json({'score': score, 'status': status})


if __name__ == '__main__':
    app.run()
