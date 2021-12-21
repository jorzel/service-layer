from flask import Flask, _app_ctx_stack
from flask_graphql import GraphQLView
from sqlalchemy.orm import scoped_session

from db import Session


def create_app():
    app = Flask(__name__)

    from api.graphql import schema
    from api.rest import main

    db_session = scoped_session(Session, scopefunc=_app_ctx_stack.__ident_func__)
    app.session = db_session
    app.register_blueprint(main)
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view(
            "graphql",
            schema=schema,
            graphiql=True,
            get_context=lambda: {"session": db_session},
        ),
    )
    return app
