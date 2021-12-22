import graphene
from graphene.relay.node import from_global_id

from service import book_restaurant_table, get_restaurants


class UserNode(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    email = graphene.String()


class RestaurantNode(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    name = graphene.String()


class RestaurantConnection(graphene.Connection):
    class Meta:
        node = RestaurantNode


class TableBookingNode(graphene.ObjectType):
    class Meta:
        interfaces = (graphene.relay.Node,)

    persons = graphene.Int()


class TableBookingConnection(graphene.Connection):
    class Meta:
        node = TableBookingNode


class BookRestaurantTable(graphene.Mutation):
    class Arguments:
        restaurant_gid = graphene.ID(required=True)
        persons = graphene.Int(required=True)
        user_email = graphene.String(required=True)

    is_booked = graphene.Boolean()

    def mutate(self, info, restaurant_gid: str, persons: int, user_email: str):
        session = info.context["session"]
        _, restaurant_id = from_global_id(restaurant_gid)
        _ = book_restaurant_table(session, restaurant_id, user_email, persons)
        return BookRestaurantTable(is_booked=True)


class Mutation(graphene.ObjectType):
    book_restaurant_table = BookRestaurantTable.Field()


class Query(graphene.ObjectType):
    up = graphene.Boolean()
    restaurants = graphene.relay.ConnectionField(
        RestaurantConnection, q=graphene.String()
    )

    def resolve_up(root, info, **kwargs):
        return True

    def resolve_restaurants(root, info, **kwargs):
        query = get_restaurants(
            info.context["session"], search=kwargs.get("q"), limit=kwargs.get("first")
        )
        return [RestaurantNode(id=r.id, name=r.name) for r in query]


schema = graphene.Schema(
    query=Query, mutation=Mutation, types=[UserNode, RestaurantNode]
)
