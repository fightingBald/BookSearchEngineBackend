
# Import the Elasticsearch DSL (Domain Specific Language) classes that
# we will use to construct the search query
from elasticsearch_dsl.query import Q
from elasticsearch_dsl import connections
from elasticsearch_dsl import Search



def create_connection_to_index_books():
    connections.create_connection(hosts=['elasticsearch:9200']) #TODO change to the service name in docker-compose.yml
    s = Search(using='default', index='books')
    return s


def search_by_keyword(keyword):
    s = create_connection_to_index_books()
    # Create the query
    query = Q(
        "multi_match",
        query=keyword,
        fields=["title", "author", "bookshelf", "text"],
        type="cross_fields",
        operator="and"
    )
    # Execute the search
    response = s.query(query).execute()  # Execute the search
    # Return the results
    return response


#each book object's text field contains a large amount of text,
# it may be computationally expensive to perform a regex search on the
# entire text field for each book.
#ndexing a subset of the text field, for example, the first few hundred or thousand words,
# rather than the entire text field.
def search_by_regex(regex):
    s = create_connection_to_index_books()
    #index the first 1000 words of the text field for each book and then use the search_by_regex(regex) function to search on that indexed subset.
    # Create the query
    query = Q(
        "regexp",
        text={
            "value": regex,
            "flags": "ALL",
            "max_determinized_states": 10000,
            "rewrite": "constant_score"
        }
    )
    # Execute the search
    response = s.query(query).execute() #Execute the search
    # Return the results
    return response





def search_by_suggestion(book_id):
    s = create_connection_to_index_books()
    # Create the query
    query = Q(
        "more_like_this",
        fields=["text"],
        like= {"_id" : book_id},
        min_term_freq=1,
        max_query_terms=12,
    )
    # Execute the search
    response = s.query(query).execute()[1:6] #Execute the search
    # Return the results
    return response



















