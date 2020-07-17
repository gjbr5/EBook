import flask
import os
from natsort import natsorted
from comic import hitomi, manamoa, webtoon

app = flask.Flask(__name__)

comic_h = hitomi()
comic_m = manamoa()
comic_w = webtoon()

@app.route('/')
def root():
    return flask.render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    response = flask.render_template('auth.html')
    if flask.request.method == 'POST':
        username = flask.request.form['username']
        if username:
            response = flask.redirect(flask.url_for('root'))
            response.set_cookie('username', username)
    return response
        

@app.route('/<string:comic_type>/view/')
@app.route('/<string:comic_type>/list/')
@app.route('/<string:comic_type>/')
def comic(comic_type):
    if comic_type not in ['manga', 'manamoa', 'webtoon']:
        flask.abort(404)
    return flask.redirect(flask.url_for('comic_list', comic_type=comic_type, page=1))

@app.route('/<string:comic_type>/list/<int:page>')
def comic_list(comic_type, page):
    if comic_type == 'manga':
        username = flask.request.cookies.get("username")
        if not username:
            flask.abort(403)
        m = comic_h
        html = 'list_manga.html'
    elif comic_type == 'manamoa':
        m = comic_m
        html = 'list_cartoon.html'
    elif comic_type == 'webtoon':
        m = comic_w
        html = 'list_cartoon.html'
    else:
        flask.abort(404)
    page_list = m.get_page_list(page)
    db_offset = (page - 1) * 10
    comic_list = m.get_comic_list(offset=db_offset)
    return flask.render_template(html, comic_type=comic_type, comic_list=comic_list, page=page, page_list=page_list)

@app.route('/<string:comic_type>/thumbnail/<int:id>/')
def thumbnail(comic_type, id):
    if comic_type not in ['manga', 'manamoa', 'webtoon']:
        flask.abort(404)
    return app.send_static_file('thumbnail/' + comic_type + '/' + str(id) + '.jpg')

@app.route('/<string:comic_type>/view/<int:id>/')
def comic_detail(comic_type, id):
    if comic_type == 'manamoa':
        m = comic_m
    elif comic_type == 'webtoon':
        m = comic_w
    else:
        flask.abort(404)
    comic = m.get_comic_info(id)
    try:
        episodes = natsorted(os.listdir("static/comic/" + comic_type + "/" + str(id)))
        episodes = [tuple(episode.split(' - ')) for episode in episodes]
    except:
        flask.abort(404)
    return flask.render_template('detail.html', comic_type=comic_type, comic=comic, episodes=episodes)

@app.route('/<string:comic_type>/img/<int:id>/<string:img_name>')
@app.route('/<string:comic_type>/img/<int:id>/<int:episode>/<string:img_name>')
def comic_img(comic_type, id, img_name, episode=None):
    if comic_type != 'manga' and episode is None:
        flask.abort(500)
    if comic_type == 'manga':
        m = comic_h
    elif comic_type == 'manamoa':
        m = comic_m
    elif comic_type == 'webtoon':
        m = comic_w
    else:
        flask.abort(404)
    return app.send_static_file(m.get_img_path(id, img_name, episode))

@app.route('/manga/view/<int:id>/')
def view_manga(id):
    try:
        imgs = comic_h.get_comic_imgs(id)
    except:
        flask.abort(404)
    return flask.render_template('view_manga.html', id=id, imgs=imgs)

@app.route('/<string:comic_type>/view/<int:id>/<int:episode>/')
def view_cartoon(comic_type, id, episode):
    if comic_type == 'manamoa':
        m = comic_m
    elif comic_type == 'webtoon':
        m = comic_w
    else:
        flask.abort(404)
    try:
        episode_name, imgs, is_last = m.get_comic_imgs(id, episode)
    except:
        flask.abort(404)
    return flask.render_template('view_cartoon.html', comic_type=comic_type, id=str(id), episode=episode, episode_name=episode_name, imgs=imgs, is_last=is_last)

if __name__ == '__main__':
    app.run(host='0.0.0.0')