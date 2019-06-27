# from flask_script import Manager
#
# from application import create_app
#
# PORT = 80
# app = create_app()
# manager = Manager(app)
#
#
# @manager.command
# def run():
#     """Run app."""
#     app.run(port=PORT)
#
#
# if __name__ == "__main__":
#     manager.run()


from flask_script import Manager
from flask_script.commands import ShowUrls

from application import create_app
from commands import GEventServer, ProfileServer

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='mode', required=False)

manager.add_command("showurls", ShowUrls())
manager.add_command("gevent", GEventServer())
manager.add_command("profile", ProfileServer())

if __name__ == "__main__":
    manager.run()
