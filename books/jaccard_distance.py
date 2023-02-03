import networkx as nx
from itertools import combinations


class JaccardGraph:

    def __init__(self, books):
        self.graph = nx.Graph()
        self.load_books(books)
        self.create_edges()

    def jaccard_similarity(self, text1, text2):
        text1_set = set(text1.lower().split())
        text2_set = set(text2.lower().split())
        intersection = text1_set.intersection(text2_set)
        union = text1_set.union(text2_set)
        return len(intersection) / len(union)

    def load_books(self, books):
        self.books = books
        for _, book in self.books.iterrows():
            self.graph.add_node(book['ID'], title=book['Title'],
                                author=book['Author'], link=book['Link'],
                                bookshelf=book['Bookshelf'], text=book['Text'])

    def create_edges(self):
        for book1, book2 in combinations(self.books.itertuples(), 2):
            book1_text = book1[6].lower()
            book2_text = book2[6].lower()
            similarity = self.jaccard_similarity(book1_text, book2_text)
            if similarity > 0:
                self.graph.add_edge(book1[0], book2[0], weight=similarity)

    def get_top5_similar_books(self, book_id):
        return sorted(self.graph[book_id].items(), key=lambda x: x[1]['weight'], reverse=True)[:5]

    def get_top5_similar_books_by_title(self, book_title):
        book_id = self.books[self.books['Title'] == book_title]['ID'].values[0]
        return self.get_top5_similar_books(book_id)


