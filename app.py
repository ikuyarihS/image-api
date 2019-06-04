import os

from jinja2 import Environment, PackageLoader, select_autoescape
from sanic import Sanic, request, response

from blur_detection_core import blur_check_file, blur_check_link
from custom_exceptions import (Base64ImageError, ImageInvalidError,
                               UrlInvalidError)

env = Environment(loader=PackageLoader('templates'),
                  autoescape=select_autoescape(['html', 'xml', 'tpl']),
                  enable_async=True)

UPLOAD_FOLDER = '/static/uploads/'


async def template(tpl, **kwargs):
    template = env.get_template(tpl)
    content = await template.render_async(kwargs)
    return response.html(content)

app = Sanic(__name__)
app.static('/static', './static')


@app.route("/")
async def test(req):
    return response.text("I\'m a teapot", status=418)


@app.route("/upload", methods=['GET', 'POST'])
async def upload(req):
    if req.method == 'POST':
        # check if there is a file in the request
        if 'file' not in req.files:
            return await template('upload.html', msg='No file selected')
        file = req.files['file'][0]
        # if no file is selected
        if file.name == '':
            return await template('upload.html', msg='No file selected')

        if file:
            with open(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.name), "wb") as f:
                f.write(file.body)
            # file.save(os.path.join(os.getcwd() + UPLOAD_FOLDER, file.filename))
            blur_score = blur_check_file(file)
            # extract the text and display it
            return await template('upload.html',
                                  msg='Successfully processed',
                                  blur_score=blur_score,
                                  img_src=UPLOAD_FOLDER + file.name)
    elif req.method == 'GET':
        return await template('upload.html')


@app.route('/check', methods=['POST'])
async def image_check_api(req: request.Request):
    """Method to handle POST request to host/check.

    Arguments:
        request {sanic.request.Request} -- Incoming request.
    """
    if not req.json or 'url' not in req.json:
        return response.text('Error - no url', status=400)

    message = 'Good image'
    try:
        score = blur_check_link(req.json['url'])
    except (UrlInvalidError, ImageInvalidError, Base64ImageError) as e:
        message = str(e)
        score = -1

    return response.json({'score': score, 'message': message})


if __name__ == '__main__':
    app.run()
