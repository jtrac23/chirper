import web
from Models import RegisterModel, LoginModel, Posts
web.config.debug = False

# pathing for the different pages '/page_name', 'Class'
urls = (
    '/', 'Home',
    '/register', 'Register',
    '/postregistration', 'PostRegistration',
    '/login', 'Login',
    '/logout', 'Logout',
    '/check-login', 'CheckLogin',
    '/post-activity', 'PostActivity',
    '/profile/(.*)/info', 'UserInfo',
    '/settings', 'UserSettings',
    '/update-settings', 'UpdateSettings',
    '/profile/(.*)', 'UserProfile'
)

app = web.application(urls, globals()) # app declaration
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer={'user': None}) # session declaration

session_data = session._initializer  # initializes the session data

# render declaration tells python were are the webpages are at and what page to render them in with session data
render = web.template.render("Views/Templates", base="MainLayout", globals={"session": session_data, "current_user": session_data['user']})


# Classes / Routes


class Home: # renders the home page and starts session
    def GET(self):
        # forces a static user remove when finished
        data = type('obj', (object,), {"username": "jordo", "password": "12345"})

        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect: # starts session
            session_data['user'] = isCorrect

        post_model = Posts.Posts()
        posts = post_model.get_all_posts()

        return render.home(posts)


class Register: # renders the register module
    def GET(self):
        return render.Register()


class Login: # renders the Login module
    def GET(self):
        return render.Login()


class PostRegistration: # inserts user data into MongoDB
    def POST(self):
        data = web.input()

        reg_model = RegisterModel.RegisterModel()
        reg_model.insert_user(data)
        return data.username


class CheckLogin: # check to see if the user logging in exists
    def POST(self):
        data = web.input()
        login = LoginModel.LoginModel()
        login.check_user(data)
        iscorrect = login.check_user(data)

        if iscorrect:
            session_data['user'] = iscorrect
            return "isCorrect"



        return "error"


class PostActivity: # inserts the blog post into MonogDB
    def POST(self):
        data = web.input()
        data.username = session_data['user']['name']
        print (data)
        post_model = Posts.Posts()
        post_model.insert_post(data)
        return "success"


class UserProfile:
    def GET(self, user):
        data = type('obj', (object,), {"username": "jordo", "password": "12345"})

        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect: # starts session
            session_data['user'] = isCorrect

        post_model = Posts.Posts()
        posts = post_model.get_user_posts(user)

        return render.Profile(posts)


class UserInfo:
    def GET(self, user):
        data = type('obj', (object,), {"username": "jordo", "password": "12345"})

        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect: # starts session
            session_data['user'] = isCorrect

        user_info = login.get_profile(user)

        return render.Info(user_info)


class UserSettings:
    def GET(self):
        data = type('obj', (object,), {"username": "jordo", "password": "12345"})

        login = LoginModel.LoginModel()
        isCorrect = login.check_user(data)

        if isCorrect:  # starts session
            session_data['user'] = isCorrect

        return render.Settings()


class UpdateSettings:
    def POST(self):
        data = web.input()
        data.username = session_data['user']['username']

        settings_model = LoginModel.LoginModel()
        if settings_model.update_info(data):
            return "success"
        else:
            return "Fatal error"


class Logout:  # initiates the logout, ending the session
    def GET(self):
        session['user'] = None
        session_data['user'] = None
        session.kill()
        return "Success"

if __name__ == "__main__":
    app.run()  # starts the web app
