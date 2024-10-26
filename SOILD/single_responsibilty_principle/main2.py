from datetime import datetime, timedelta

class Movie:
    def __init__(self, title: str, director: str, release_year: int):
        self.title = title
        self.director = director
        self.release_year = release_year

class RentedMovie:
    def __init__(self, movie: Movie, rented_date: datetime):
        self.movie = movie
        self.rented_date = rented_date
        self.max_rent_days = 10  # Allowed days before late fee is applied

class RentalFeeCalculator:
    BASE_FEE = 100
    LATE_FEE_PER_DAY = 20

    def calculate_fee(self, rented_movie: RentedMovie) -> int:
        today = datetime.today()
        due_date = rented_movie.rented_date + timedelta(days=rented_movie.max_rent_days)
        if today > due_date:
            late_days = (today - due_date).days
            return self.BASE_FEE + late_days * self.LATE_FEE_PER_DAY
        return self.BASE_FEE

class RentalSystem:
    def __init__(self):
        self.available_movies = {}
        self.rented_movies = {}
        self.fee_calculator = RentalFeeCalculator()
    
    def add_movie(self, movie: Movie):
        self.available_movies[movie.title] = movie
    
    def rent_movie(self, title: str) -> bool:
        if title in self.available_movies:
            movie = self.available_movies.pop(title)
            rented_movie = RentedMovie(movie=movie, rented_date=datetime.today())
            self.rented_movies[title] = rented_movie
            return True
        return False
    
    def return_movie(self, title: str) -> int:
        if title in self.rented_movies:
            rented_movie = self.rented_movies.pop(title)
            return self.fee_calculator.calculate_fee(rented_movie)
        return -1