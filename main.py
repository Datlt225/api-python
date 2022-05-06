import werkzeug
from flask import Flask, jsonify, request, g
import MySQLdb
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({
        'message': "Request không hợp lệ, vui lòng kiểm tra lại!"
    }), 500


@app.before_request
def before_request():
    g.conn = MySQLdb.connect(
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        database=os.getenv('database')
    )
    g.cursor = g.conn.cursor()


@app.after_request
def db_disconnect(response):
    g.cursor.close()
    g.conn.close()
    return response


@app.route('/')
def home():
    return jsonify({
        'message': "API Code By Banana"
    })


# API login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    g.cursor.execute("SELECT * FROM User WHERE Email=%s AND PassWord=%s", (email, password))
    row = g.cursor.fetchall()

    if row:
        return jsonify({
            'message': 'Đăng nhập thành công!'
        })
    else:
        return jsonify({
            'message': 'Tài khoản hoặc mật khẩu không đúng!'
        }), 401


# API register
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data['email']
        pass_word = data['password']
        name = data['name']

        if email and pass_word and name:
            # pass_word = bcrypt.hashpw(str.encode(pass_word), bcrypt.gensalt())
            g.cursor.execute("SELECT * FROM User WHERE Email = %s", (email,))
            row = g.cursor.fetchall()
            g.conn.commit()

            if row:
                resp = jsonify({
                    'message': 'Người dùng đã tồn tại'
                })
                resp.status_code = 400

                return resp
            else:
                g.cursor.execute("INSERT INTO User (Email, PassWord, Name) VALUES (%s, %s, %s)",
                                 (email, pass_word, name))
                g.conn.commit()

                return jsonify({
                    'message': 'Đăng ký thành công'
                })
        else:
            resp = jsonify({'message': 'Bad Request - invalid credendtials'})
            resp.status_code = 400

            return resp

    except Exception as ex:
        print(ex)
        resp = jsonify({
            'message': 'Bad Request - invalid credendtials'
        })
        resp.status_code = 400
        return resp


# API load banner
@app.route('/banner', methods=['GET'])
def banner_song():
    g.cursor.execute("SELECT Banner.ID_ads, Banner.Img_ads, Banner.Content, Banner.ID_song, Song.Name_song,"
                     "Song.Img_song FROM `Song` INNER JOIN Banner ON Banner.ID_song = Song.ID_song "
                     "WHERE Banner.ID_song = Song.ID_song")
    row = g.cursor.fetchall()
    data_return = []
    for i in row:
        data_return.append({
            'id': i[0],
            'image': i[1],
            'content': i[2],
            'id_song': i[3],
            'name_song': i[4],
            'img_song': i[5]
        })
    return jsonify(data_return)


# API Loading list by id banner
@app.route('/playlist_banner', methods=['POST'])
def playlist_banner():
    data = request.get_json()
    id_ads = data['ID_ads']

    g.cursor.execute('SELECT ID_song FROM Banner WHERE ID_ads = %s', (id_ads,))
    row_ads = g.cursor.fetchall()

    g.cursor.execute("SELECT * FROM Song WHERE ID_song = %s", (row_ads,))
    row_song = g.cursor.fetchall()

    data_return_platlist_ads = []

    for i in row_song:
        data_return_platlist_ads.append({
            'ID_song': i[0],
            'ID_album': i[1],
            'ID_category': i[2],
            'ID_playlist': i[3],
            'Name_song': i[4],
            'Img_song': i[5],
            'Singer': i[6],
            'Link_song': i[7]
        })
    return jsonify(data_return_platlist_ads)


# API loading album
@app.route('/album', methods=['Get'])
def album():
    g.cursor.execute("SELECT * FROM Album")

    row_album = g.cursor.fetchall()
    data_return_album = []

    for i in row_album:
        data_return_album.append({
            'ID_album': i[0],
            'Name_album': i[1],
            'Img_album': i[2],
        })
    return jsonify(data_return_album)


# API Loading list by id album
@app.route('/playlist_album', methods=['POST'])
def playlist_album():
    data = request.get_json()
    id_album = data['ID_album']

    g.cursor.execute('SELECT * FROM Song WHERE ID_album LIKE %s', ("%" + id_album + "%",))

    row_song = g.cursor.fetchall()
    data_return_playlist_album = []

    for i in row_song:
        data_return_playlist_album.append({
            'ID_song': i[0],
            'ID_album': i[1],
            'ID_category': i[2],
            'ID_playlist': i[3],
            'Name_song': i[4],
            'Img_song': i[5],
            'Singer': i[6],
            'Link_song': i[7]
        })
    return jsonify(data_return_playlist_album)


# API loading songs
@app.route('/song', methods=['GET'])
def song():
    g.cursor.execute("SELECT * FROM Song")
    row = g.cursor.fetchall()
    data_return = []
    for i in row:
        data_return.append({
            'ID_song': i[0],
            'ID_album': i[1],
            'ID_category': i[2],
            'ID_playlist': i[3],
            'Name_song': i[4],
            'Img_song': i[5],
            'Singer': i[6],
            'Link_song': i[7],
        })
    return jsonify(data_return)


# API searcing music
@app.route('/searching', methods=['POST'])
def searching():
    data = request.get_json()
    word = data['word']
    g.cursor.execute("SELECT * FROM Song WHERE Name_song LIKE %s", ("%" + word + "%",))
    row = g.cursor.fetchall()
    data_return_searching = []
    for i in row:
        data_return_searching.append({
            'ID_song': i[0],
            'ID_album': i[1],
            'ID_category': i[2],
            'ID_playlist': i[3],
            'Name_song': i[4],
            'Img_song': i[5],
            'Singer': i[6],
            'Link_song': i[7]
        })
    return jsonify(data_return_searching)


# API loading music list by banner
@app.route('/playlist', methods=['POST'])
def playlist():
    data = request.get_json()
    id_banner = data['ID_banner']
    g.cursor.execute("SELECT ID_song FROM Banner WHERE ID_ads LIKE %s", (id_banner,))
    row = g.cursor.fetchall()

    g.cursor.execute("SELECT * FROM Song WHERE ID_song LIKE %s", (row,))
    row_song = g.cursor.fetchall()

    data_return_playlist = []
    for i in row_song:
        data_return_playlist.append({
            'ID_song': i[0],
            'ID_album': i[1],
            'ID_category': i[2],
            'ID_playlist': i[3],
            'Name_song': i[4],
            'Img_song': i[5],
            'Singer': i[6],
            'Link_song': i[7]
        })
    return jsonify(data_return_playlist)


# API Loading favorite songs
@app.route('/fa_song', methods=['POST'])
def fasong():
    data = request.get_json()
    data_return_favorite_song = []
    id_user = data['ID_user']

    g.cursor.execute("SELECT ID_song FROM FavoriteSong WHERE ID_song = %s", (id_user,))
    get_id_song = g.cursor.fetchall()

    if get_id_song:
        g.cursor.execute("SELECT * FROM Song WHERE ID_song = %s", (get_id_song,))
        get_fa_song = g.cursor.fetchall()

        for i in get_fa_song:
            data_return_favorite_song.append({
                'ID_song': i[0],
                'ID_album': i[1],
                'ID_category': i[2],
                'ID_playlist': i[3],
                'Name_song': i[4],
                'Img_song': i[5],
                'Singer': i[6],
                'Link_song': i[7]
            })

    else:
        data_return_favorite_song.append({
            'message': 'Không có bài hát'
        })

    return jsonify(data_return_favorite_song)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
