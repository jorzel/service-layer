import graphene
from graphene.relay.node import from_global_id

from models import Restaurant, User


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
        user = session.query(User).filter_by(email=user_email).first()
        restaurant = session.query(Restaurant).get(restaurant_id)
        table_booking = restaurant.book_table(persons, user)
        session.add(table_booking)
        session.commit()
        return BookRestaurantTable(is_booked=True)


class Mutation(graphene.ObjectType):
    book_restaurant_table = BookRestaurantTable.Field()


class Query(graphene.ObjectType):
    up = graphene.Boolean()
    restaurants = graphene.relay.ConnectionField(RestaurantConnection)

    def resolve_up(root, info, **kwargs):
        return True

    def resolve_restaurants(root, info, **kwargs):
        session = info.context["session"]
        return [
            RestaurantNode(id=r.name, name=r.name) for r in session.query(Restaurant)
        ]


schema = graphene.Schema(
    query=Query, mutation=Mutation, types=[UserNode, RestaurantNode]
)
