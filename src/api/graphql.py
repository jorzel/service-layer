import graphene


class Query(graphene.ObjectType):
    up = graphene.Boolean()

    def resolve_up(root, info):
        return True


schema = graphene.Schema(query=Query)
