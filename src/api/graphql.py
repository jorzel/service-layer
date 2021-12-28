import graphene
from graphene.relay.node import from_global_id

from service import book_restaurant_table, get_restaurants, sign_in, sign_up

from .auth import sign_in_required


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


class SignUp(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserNode)

    def mutate(self, info, email: str, password: str):
        session = info.context["session"]
        user = sign_up(session, email, password)
        return SignUp(user=user)


class SignIn(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    def mutate(self, info, email: str, password: str):
        session = info.context["session"]
        token = sign_in(session, email, password)
        return SignIn(token=token)


class BookRestaurantTable(graphene.Mutation):
    class Arguments:
        restaurant_gid = graphene.ID(required=True)
        persons = graphene.Int(required=True)

    is_booked = graphene.Boolean()

    @sign_in_required()
    def mutate(self, info, restaurant_gid: str, persons: int, **kwargs):
        session = info.context["session"]
        current_user = kwargs["current_user"]
        _, restaurant_id = from_global_id(restaurant_gid)
        _ = book_restaurant_table(session, restaurant_id, current_user.email, persons)
        return BookRestaurantTable(is_booked=True)


class Mutation(graphene.ObjectType):
    book_restaurant_table = BookRestaurantTable.Field()
    sign_in = SignIn.Field()
    sign_up = SignUp.Field()


class Query(graphene.ObjectType):
    up = graphene.Boolean()
    restaurants = graphene.relay.ConnectionField(
        RestaurantConnection, q=graphene.String()
    )
    me = graphene.Field(UserNode)

    def resolve_up(root, info, **kwargs):
        return True

    @sign_in_required()
    def resolve_restaurants(root, info, **kwargs):
        query = get_restaurants(
            info.context["session"], search=kwargs.get("q"), limit=kwargs.get("first")
        )
        return [RestaurantNode(id=r.id, name=r.name) for r in query]

    @sign_in_required()
    def resolve_me(root, info, **kwargs):
        return kwargs["current_user"]


schema = graphene.Schema(
    query=Query, mutation=Mutation, types=[UserNode, RestaurantNode]
)
