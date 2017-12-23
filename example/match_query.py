from sunshine.query import QueryBuilders, match


query_body = QueryBuilders(match("type", "config"))
print(query_body)

