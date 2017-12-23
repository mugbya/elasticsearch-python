from sunshine.query import QueryBuilders, match_all, match


'''
construct simple query
'''

query_body = QueryBuilders(match_all())
print(query_body)



