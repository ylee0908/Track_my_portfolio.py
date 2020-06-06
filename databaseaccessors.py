
class DatabaseAccessors:
    @staticmethod
    def get_my_preferred_stocks():
        # Want to fetch a list of stocks that I care about, and my preferences for each
        # Returns dictionary of dictionaries

        information_from_database = [
            ('GOOG', 'Google', 1000, 2000, 1),
            ('MSFT', 'Microsoft', 150, 300, 2),
            ('AMZN', 'Amazon', 2500, 3000, 3),
            ('AAPL', 'Apple', 140, 250, 4),
            ('TSLA', 'Tesla', 500, 750, 5),
            ('IAG', 'British Airways', 220, 400, 6),
            ('NFLX', 'Netflix', 400, 500, 7)
        ]

        result = {}
        for info in information_from_database:
            result[info[0]] = {'nickname':  info[1],
                               'buyPrice':  info[2],
                               'sellPrice': info[3],
                               'priority':  info[4]}

        return result

