
#******************************************************************************#
# User class:
class user:
	
	def __init__(self, sumer=0., car=0, ident=[], rate=[], time=[] ):
		self.sum = sumer # Sum of the rate for all the movies.
		self.car = car   # Number of movies.
		self.id = ident  # Identifier for each movie.
		self.rate = rate # Score for each movie.
		self.time = time # Time of the score: From Coordinated Universal Time (UTC) of January 1, 1970.
		

