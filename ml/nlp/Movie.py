class Movie:
    def __init__(self, details:dict):
        self.details = {}
        self.id = self.details.get('id')
        self.reviews = []

    # def __str__(self):
    #     return f"{self.title} ({self.year}), directed by {self.director}"
    