import graphene

from models import Restaurant


class RestaurantNode(graphene.ObjectType):
    class Meta:
        interaces = (graphene.relay.Node,)

    name = graphene.String()


class RestaurantConnection(graphene.Connection):
    class Meta:
        node = RestaurantNode


class Query(graphene.ObjectType):
    up = graphene.Boolean()
    restaurants = graphene.relay.ConnectionField(RestaurantConnection)

    def resolve_up(root, info, **kwargs):
        return True

    def resolve_restaurants(root, info, **kwargs):
        session = info.context["session"]
        return session.query(Restaurant).all()


schema = graphene.Schema(query=Query)
