from flask import Blueprint, render_template, redirect, url_for, request, flash
from epl.extensions import db
from epl.models import Player, Club

player_bp = Blueprint('player', __name__, template_folder='templates') 

@player_bp.route('/')
def index():
  players = db.session.scalars(db.select(Player)).all()
  return render_template('players/index.html',
                         title='Players Page',
                         players=players)

@player_bp.route('/new', methods=['GET', 'POST'])
def new_player():
  clubs = db.session.scalars(db.select(Club)).all()
  if request.method == 'POST':
    name = request.form['name']
    position = request.form['position']
    nationality = request.form['nationality']
    goals = int(request.form['goals'])
    squad_no = int(request.form['squad_no'])
    img = request.form['img']
    club_id = int(request.form['club_id'])

    player = Player(name=name, position=position, nationality=nationality,
                    goals=goals, squad_no=squad_no, img=img, club_id=club_id)
    db.session.add(player)
    db.session.commit()
    flash('add new player successfully', 'success')
    return redirect(url_for('player.index'))

  return render_template('players/new_player.html',
                         title='New Player Page',
                         clubs=clubs)

@player_bp.route('/players/search', methods=['POST'])
def search_player():
  if request.method == 'POST':
    player_name = request.form['player_name']
    players = db.session.scalars(db.select(Player).where(Player.name.like(f'%{player_name}%'))).all()
    return render_template('players/search_player.html',
                           title='Search Player Page',
                           players=players)
  
@player_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def info_player(id):
    player = db.session.get(Player, id)
    clubs = db.session.scalars(db.select(Club)).all()

    if request.method == 'POST':
        player.name = request.form['name']
        player.position = request.form['position']
        player.nationality = request.form['nationality']
        player.goals = int(request.form['goals'])
        player.squad_no = int(request.form['squad_no'])
        player.img = request.form['img']
        player.club_id = int(request.form['club_id'])

        db.session.commit()
        flash('Update player successfully', 'success')
        return redirect(url_for('player.index'))

    return render_template(
        'players/info_player.html',
        title='Info Player Page',
        player=player,
        clubs=clubs
    )
