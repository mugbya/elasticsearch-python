'''
elasticsearch query body api
'''


class QueryBuilders(object):

    def __init__(self, qb):
        self.query = {
            "size": 10,
            "query": qb
        }

    def size(self, num):
        self.query.update({'size': num})
        return self

    def __repr__(self):
        return str(self.query).replace("'", '"')


def match_all():
    return MatchAllBuilder()


def match(name, value, operator=None):
    return MatchBuilder(name, value, operator=operator)


def bool_query():
    return BoolQueryBuilder()


def term_query(name, value):
    return TermQueryBuilder(name, value)


def query_string(name, value):
    return QueryStringBuilders(name, value)


def nested_query(path, qb):
    return NestedQueryBuilders(path, qb)


class MatchAllBuilder(QueryBuilders):
    def __init__(self):
        self.query = {
            "match_all":{}
        }


class MatchBuilder(QueryBuilders):
    def __init__(self, name, value, operator=None):
        self.query = {
            "match": {
                name: {
                    "query": value,
                    "operator": operator
                }
            }
        }


class BoolQueryBuilder(QueryBuilders):
    def __init__(self):
        self.mustClauses = []
        self.mustNotClauses = []
        self.filterClauses = []
        self.shouldClauses = []
        self.query = {
            "bool": {
                "must": self.mustClauses,
                "must_not": self.mustNotClauses,
                "should": self.shouldClauses,
                "filter": self.filterClauses
            }
        }

    def should(self, query_builder: QueryBuilders):
        if not query_builder:
            raise SyntaxError('inner bool query clause cannot be null')
        self.shouldClauses.append(query_builder)
        return self

    def must(self, query_builder: QueryBuilders):
        if not query_builder:
            raise SyntaxError('inner bool query clause cannot be null')
        self.mustClauses.append(query_builder)
        return self

    def must_not(self, query_builder: QueryBuilders):
        if not query_builder:
            raise SyntaxError('inner bool query clause cannot be null')
        self.mustNotClauses.append(query_builder)
        return self


class TermQueryBuilder(QueryBuilders):
    def __init__(self, name, value):
        self.query = {
            "term": {
                name: {
                    "value": value
                }
            }
        }


class QueryStringBuilders(QueryBuilders):
    def __init__(self, name, value):
        self.query = {
            "query_string": {
                "default_field": name,
                "query": value
            }
        }


class NestedQueryBuilders(QueryBuilders):
    def __init__(self, path, qb):
        self.query = {
            "nested": {
                "path": path,
                "query": qb
            }
        }


def multi_query_string(field, keyword):
    bq = bool_query()
    if "&" in keyword:
        for _ in keyword.split("&"):
            bq.must(query_string(field, '*' + _.strip() + '*'))
    elif "|" in keyword:
        for _ in keyword.split("|"):
            bq.should(query_string(field, '*' + _.strip() + '*'))
    return bq

if __name__ == "__main__":
    prod_code = 'JDB'
    key = "下了"
    value = '下了 | 下款'

    # bq = bool_query()
    # bq.must(term_query('prod_code', prod_code)) \
    #     .must(bool_query()
    #           .should(query_string('rp_content', '*' + key + '*'))
    #           .should(nested_query('rp_data', query_string('rp_data.rp_content', '*' + key + '*')))
    #           )

    bq = bool_query()
    bq.must(term_query('prod_code', prod_code)) \
        .must(bool_query()
              .should(multi_query_string('rp_content', value))
              .should(nested_query('rp_data', multi_query_string('rp_data.rp_content', value)))
              )

    print(bq)
    print(QueryBuilders(bq).size(1000))
    # print(str(query(bq)).replace('\'', '"'))
    # print(query(bq))
