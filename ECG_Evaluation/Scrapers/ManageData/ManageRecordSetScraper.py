import Controllers.Common as common
import Controllers.Constants as cons
import Scraper as scraper

def find_record_list(my_col, query_data):
    lookup_query = {
        cons.CONS_QUERY_FROM: query_data[cons.CONS_QUERY_FROM],
        cons.CONS_QUERY_LOCALFIELD: query_data[cons.CONS_QUERY_LOCALFIELD],
        cons.CONS_QUERY_FOREIGNFIELD: query_data[cons.CONS_QUERY_FOREIGNFIELD],
        cons.CONS_QUERY_AS: query_data[cons.CONS_QUERY_AS]
    }

    query_data = {
        cons.CONS_QUERY_LOOKUP_QUERY:lookup_query
    }
    output = scraper.find_with_aggregate(my_col,query_data)
    
    return output
