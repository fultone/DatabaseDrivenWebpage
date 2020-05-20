'''
    datasource.py
    Web Project Pair E, October 2017
'''
import psycopg2
import getpass

class DataSource:
    ''' 
        The DataSource class takes in keyword (searchCategory) and search query 
        parameters and uses them to search the UFO database for relevant UFO 
        sightings. The sightings which match the given search are returned. 
    '''
    def __init__(self, searchCategory, query):
        self.searchCategory = searchCategory
        self.connection = None
        self.query = query
        self.searchResults = []
    
    ''' 
        Opens connection with the UFO SQL table via the user 'fultone'.
        Throws 'Connection error' exception if the connection fails.
    '''
    def connectToDatabase(self):
        database = 'fultone'
        user = 'fultone'
        password = "tiger546orange"
        try:
            self.connection = psycopg2.connect(database=database, user=user, \
                                               password=password, host="localhost")
        except Exception as e:
            print ('Connection error: ', e)
            exit()
    
    ''' Closes connection with the UFO SQL table. '''
    def closeConnection(self):
        self.connection.close()

    ''' 
        Connects to the UFO database and calls a SQL query to search the database 
        with the given parameters. Adds all found search results to a list 
        'searchResults.' If no results are found, throws a 'No Results Found' 
        exception. Closes connection with UFO database and returns searchResults.
    '''
    def searchDatabase(self):
        self.connectToDatabase()
        try:
            cursor = self.connection.cursor()
            query = self.createSQLQuery()
            cursor.execute(query)
            for row in cursor.fetchall():
                self.searchResults.append(row)
        except Exception as e:
            print ('No results found', e)
            self.closeConnection()
            exit()
        self.closeConnection()
        return self.searchResults
    
    '''
        Creates and returns a SQL query based on the search filter selected by the
        user.
    '''
    def createSQLQuery(self):
        query = "SELECT datesighted, city, statesighted, duration, shape, summary " \
                "FROM ufo WHERE "
        if(self.searchCategory=="datesighted"):
            query += self.searchCategory + " LIKE '" + self.query + "%'"
        elif(self.searchCategory=="keyword"):
            query += "summary LIKE '%" + self.query + "%' OR datesighted LIKE '%" + \
            self.query +  "%' OR city LIKE '%" + self.query + \
            "%' OR statesighted LIKE '%" + self.query + "%' OR duration LIKE '%" + \
            self.query + "%' OR shape LIKE '%" + self.query + "%'"
        else:
            query += self.searchCategory + "='" + self.query + "'"
        return query