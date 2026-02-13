from flask import Blueprint, request, url_for, redirect, flash, render_template
from epl.extensions import db
from epl.models import Club, Player

players_bp = Blueprint('players', __name__, template_folder='templates')

@players_bp.route('/')
def index():
    players = db.session.scalars(db.select(Player)).all()
    return render_template(
        'players/index.html',
        title='Players Page',
        players=players
    )

@players_bp.route('/players/new', methods=['GET', 'POST'])
def new_player():
    clubs = db.session.scalars(db.select(Club)).all()

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        nationality = request.form['nationality']

        goal = int(request.form.get('goals', 0))

        if position == "Goalkeeper":
            clean_sheets = request.form.get('clean_sheets')
            clean_sheets = int(clean_sheets) if clean_sheets else 0
        else:
            clean_sheets = None

        squad_no = request.form.get('squad_no')
        squad_no = int(squad_no) if squad_no else None

        img = request.form['img']
        club_id = int(request.form['club_id'])

        player = Player(
            name=name,
            position=position,
            nationality=nationality,
            goal=goal,
            clean_sheets=clean_sheets,
            squad_no=squad_no,
            img=img,
            club_id=club_id
        )

        db.session.add(player)
        db.session.commit()

        flash('Add new player successfully', 'success')
        return redirect(url_for('players.index'))

    return render_template(
        'players/new_player.html',
        title='New Player Page',
        clubs=clubs
    )

@players_bp.route('/players/search', methods=['GET', 'POST'])
def search_player():
    players = []

    if request.method == 'POST':
        player_name = request.form['player_name']
        players = db.session.scalars(
            db.select(Player).where(Player.name.like(f'%{player_name}%'))
        ).all()

    return render_template(
        'players/search_player.html',
        title='Search Player Page',
        players=players
    )

@players_bp.route('/<int:id>/info')
def info_player(id):
    player = db.session.get(Player, id)

    return render_template(
        'players/info_player.html',
        title='Info Player Page',
        player=player
    )

@players_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_player(id):
    player = db.session.get(Player, id)
    clubs = db.session.scalars(db.select(Club)).all()

    if request.method == 'POST':
        player.name = request.form['name']
        player.nationality = request.form['nationality']

        player.goal = int(request.form.get('goals', 0))

        if player.position == "Goalkeeper":
            clean_sheets = request.form.get('clean_sheets')
            player.clean_sheets = int(clean_sheets) if clean_sheets else 0
        else:
            player.clean_sheets = None

        squad_no = request.form.get('squad_no')
        player.squad_no = int(squad_no) if squad_no else None

        player.img = request.form['img']
        player.club_id = int(request.form['club_id'])

        db.session.commit()

        flash('Update player successfully', 'success')
        return redirect(url_for('players.index'))

    return render_template(
        'players/update_player.html',
        title='Update Player Page',
        player=player,
        clubs=clubs
    )