from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Pitch,User
from .forms import PitchForm
from flask_login import login_required
from .forms import PitchForm,UpdateProfile
from .. import db,photos
from ..email import mail_message



# Pitch = pitch.Pitch

@main.route('/')
def index():

   
    title = 'Home - Welcome to The best Pitch IP'
    return render_template('index.html', title = title )
@main.route('/pitches/<int:id>')
def pitches(pitche_id):

    '''
    View movie page function that returns the movie details page and its data
    '''
    return render_template('movie.html',id = movie_id)
# @main.route('/movie/<int:id>')
# def movie(id):

#     '''
#     View movie page function that returns the movie details page and its data
#     '''
#     movie = get_movie(id)
#     title = f'{movie.title}'
#     reviews = Review.get_reviews(movie.id)

#     return render_template('movie.html',title = title)

@main.route('/category/pitch/new/<int:id>', methods = ['GET','POST'])
@login_required
def new_pitch(id):
    form = PitchForm()
    category = PitchCategory.query.filter_by(id=id).first()
    
    # pitche= get_pitche(id)

    if form.validate_on_submit():
        title = form.title.data
        pitch = form.pitch.data
        new_pitch = Pitch(category.id,title,category.poster,pitch)
        new_pitch.save_pitch()
        return redirect(url_for('category',id = category.id ))

    title = f'{category.title} pitch'
    return render_template('new_pitch.html',title = title, pitch_form=form, category=category)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None: 
        abort(404)
  
    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update/',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))





    