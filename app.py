from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector as mysql
import requests

app = Flask(__name__)
app.secret_key = "*n&(j%me18@gda^)^^!9unkelo8*gw**$d@uwmn4tcdlf7qk"

db = mysql.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="peliculasdb"
)

cursor = db.cursor()


@app.route('/', methods=['GET', 'POST'])
def index():
    movie = ""
    if request.method == "GET":
        try:
            movieid = request.args.get('get_movie_id')
            if movieid:
                response = requests.get(f"https://yts.mx/api/v2/movie_details.json?movie_id={movieid}")
                json = response.json()
                data = json.get('data')
                movie = data.get('movie')
        except Exception:
            pass
    error = ""
    if request.method == "POST":
        title = request.form['title']
        if title:
            poster = request.form['poster']
            trailer = request.form['trailer']
            year = request.form['year']
            language = request.form['language']
            rated = request.form['rated']
            runtime = request.form['runtime']
            description = request.form['description']

            sql = "INSERT INTO movies(title, poster, trailer, year, language, rated, runtime, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (title, poster, trailer, year, language, rated, runtime, description)
            cursor.execute(sql, val)
            db.commit()
            flash("La pelicula fue agregada correctamente")
            return redirect(url_for('movie_list'))
        else:
            error = "Este campo es requerido"

    return render_template('index.html', movie=movie, error=error)


@app.route('/movie_list')
def movie_list():
    sql = "SELECT * FROM movies ORDER BY id DESC"
    cursor.execute(sql)
    movies = cursor.fetchall()
    return render_template('movie_list.html', movies=movies)


@app.route('/delete/<int:id>')
def delete(id):
    sql = f"DELETE FROM movies WHERE id = {id}"
    cursor.execute(sql)
    flash('Pelicula Eliminada Correctamente')
    return redirect(url_for('movie_list'))


@app.route('/edit_movie/<int:id>')
def edit(id):
    query = f"SELECT * FROM movies WHERE id = {id}"
    cursor.execute(query)
    movie = cursor.fetchone()

    return render_template('movie_update.html', movie=movie)


@app.route('/update_movie', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        title = request.form['title']
        poster = request.form['poster']
        trailer = request.form['trailer']
        year = request.form['year']
        language = request.form['language']
        rated = request.form['rated']
        runtime = request.form['runtime']
        description = request.form['description']
        id = request.form['id']

        sql = f"UPDATE movies SET title = %s, poster = %s, trailer = %s, year = %s, language = %s, rated = %s, runtime = %s, description = %s WHERE id = {id}"
        val = (title, poster, trailer, year, language, rated, runtime, description)
        cursor.execute(sql, val)
        db.commit()

        flash('Pelicula Actualizada Correctamente')
        return redirect(url_for('movie_list'))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
