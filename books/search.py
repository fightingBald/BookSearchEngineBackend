
# Import the Elasticsearch DSL (Domain Specific Language) classes that
# we will use to construct the search query
from elasticsearch_dsl.query import Q
from elasticsearch_dsl import connections
from elasticsearch_dsl import Search


# Search documents by keyword. On user input a string S, the application returns a list of  book documents which S appears in the his field 'title', 'author','bookshelf', 'text',`

def search_by_keyword(keyword):
    # Create the Elasticsearch client
    connections.create_connection(hosts=['elasticsearch:9200']) #TODO change to the service name in docker-compose.yml
    # Create the search object
    s = Search(using='default', index='books')
    # Create the query and returns the list of documents ordered by relevance, i.e., the score
    query = Q( "multi_match", query=keyword, fields=['title', 'author', 'bookshelf', 'text'], fuzziness='AUTO', operator='and', ) # Execute the search
    response = s.query(query ).execute() #Execute the search
    # Return the results
    return response

#— Explicit feature “Advanced search” : Search documents by RegEx. On user input a string RegEx, the application
#returns : either a list of text documents whose index table contains a string S matching RegEx as regular expression (refer to Lecture 1 of UE DAAR for a formal definition of regular expressions); or a list of text documents
#containing a string S matching RegEx as regular expression (Warning : this option may cause the application to
#slow down considerably).

def search_by_regex(regex):
    # Create the Elasticsearch client
    connections.create_connection(hosts=['elasticsearch:9200']) #TODO change to the service name in docker-compose.yml
    # Create the search object
    s = Search(using='default', index='books')
    # Create the query
    query = Q(
        "regexp",
        text=regex,
    )
    # Execute the search
    response = s.query(query).execute() #Execute the search
    # Return the results
    return response

def search_by_suggestion(keyword):
    # Create the Elasticsearch client
    connections.create_connection(hosts=['elasticsearch:9200']) #TODO change to the service name in docker-compose.yml
    # Create the search object
    s = Search(using='default', index='books')
    # Create the query
    query = Q(
        "multi_match",
        query=keyword,
        fields=['title', 'author', 'bookshelf', 'text'],
        fuzziness='AUTO',
        operator='and',
    )
    # Execute the search
    response = s.query(query).suggest('my-suggestion', keyword, term={'field': 'text'}).execute()#
    # Return the results
    return response






