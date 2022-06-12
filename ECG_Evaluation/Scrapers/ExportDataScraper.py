import Controllers.Constants as cons
from Controllers.FilesModel import Files
import Scraper as scraper

def find_channel_list(my_col, query_data):
    match_query = {
        cons.CONS_ID_SHORT: query_data[cons.CONS_ID_SHORT]
    }

    lookup_query = {
        cons.CONS_QUERY_FROM: query_data[cons.CONS_QUERY_FROM],
        cons.CONS_QUERY_LOCALFIELD: query_data[cons.CONS_QUERY_LOCALFIELD],
        cons.CONS_QUERY_FOREIGNFIELD: query_data[cons.CONS_QUERY_FOREIGNFIELD],
        cons.CONS_QUERY_AS: query_data[cons.CONS_QUERY_AS]
    }

    query_data = {
        cons.CONS_QUERY_MATCH_QUERY:match_query,
        cons.CONS_QUERY_LOOKUP_QUERY:lookup_query
    }
    output = scraper.find_with_aggregate(my_col,query_data)
    
    return output

def retrieve_ecg_files(db, list_selected_ecg_id):
    data = scraper.find_by_query(
        db.fs.files, cons.CONS_QUERYIN_STR, cons.FILE_ECG_ID, list_selected_ecg_id)
    fs = scraper.connect_gridfs(db)
    files = []
    for item in data:
        files.append(Files(
            file_id=item[cons.ECG_ID_SHORT],
            file_name=item[cons.ECG_FILE_NAME],
            file_name_ext=item[cons.FILE_ECG_FILE_NAME_EXT],
            output_data=fs.get(item[cons.FILE_ID_SHORT]).read(),
            ecg_id=item[cons.FILE_ECG_ID],
            channel=item[cons.ECG_CHANNEL]))
    return files
