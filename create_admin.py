import sys
from getpass import getpass
from webapp import create_app
from webapp.extensions import db
from webapp.user.model import User

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')

    if db.session.scalar(
        db.select(db.func.count()).select_from(User).filter_by(username=username)
    ):
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')

    if not password == password2:
        sys.exit(0)
        
    new_user = User(username=username, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print('User with id {} added'.format(new_user.id))


