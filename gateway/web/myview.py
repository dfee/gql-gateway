from graphql_server.flask import GraphQLView
from dataclasses import dataclass

class MyView(GraphQLView):
    # def get_context(self):
    #     context = (
    #         copy.copy(self.context)
    #         if self.context and isinstance(self.context, MutableMapping)
    #         else {}
    #     )
    #     if isinstance(context, MutableMapping) and "request" not in context:
    #         context.update({"request": request})
    #     return context

    def get_context(self):