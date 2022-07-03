import Controllers.Constants as cons
from Controllers.FilesModel import Files
import Scraper as scraper
import Controllers.Helper as helper

def find_channel_list(record_set_col, query_data):
    match_query = {
        cons.CONS_ID_SHORT: query_data[cons.CONS_ID_SHORT]
    }
    
    # Retrieve 'from' key to build the lookup query based on the collection name
    # Ex: ['ecg', 'exportingRegion']
    for x in query_data[cons.CONS_QUERY_FROM]:
        if x == cons.CONS_ECG:
            lookup_query = {
                cons.CONS_QUERY_FROM: x,
                cons.CONS_QUERY_LOCALFIELD: query_data[cons.CONS_QUERY_LOCALFIELD],
                cons.CONS_QUERY_FOREIGNFIELD: query_data[cons.CONS_QUERY_FOREIGNFIELD],
                cons.CONS_QUERY_AS: x
            }
        else:
            lookup_level_2_query = {
                cons.CONS_QUERY_FROM: x,
                cons.CONS_QUERY_LET: {
                    cons.CONS_EXPORTING_REGION_RECORD_SET_ID: f'${cons.CONS_ID_SHORT}',
                    cons.CONS_EXPORTING_REGION_ECG_ID: f'${lookup_query[cons.CONS_QUERY_AS]}.{cons.CONS_ID_SHORT}',
                },
                cons.CONS_QUERY_PIPELINE: [
                    {cons.CONS_QUERY_MATCH_QUERY: {
                        cons.CONS_QUERY_EXPR_QUERY: {
                            cons.CONS_QUERY_AND_QUERY: [
                                {cons.CONS_QUERY_EQ_QUERY: [
                                    f'${cons.CONS_EXPORTING_REGION_ECG_ID}', 
                                    f"$${cons.CONS_EXPORTING_REGION_ECG_ID}"]},
                                {cons.CONS_QUERY_EQ_QUERY: [
                                    f'${cons.CONS_EXPORTING_REGION_RECORD_SET_ID}', 
                                    f"$${cons.CONS_EXPORTING_REGION_RECORD_SET_ID}"]}
                            ]
                        }
                    }
                    }
                ],
                cons.CONS_QUERY_AS: x
            }

    unwind_query = {
        cons.CONS_QUERY_PATH: f'${lookup_query[cons.CONS_QUERY_AS]}',
        cons.CONS_QUERY_PRESERVE: True
    }

    group_query = {
        cons.CONS_ID_SHORT: f'${cons.CONS_ID_SHORT}',
        cons.CONS_ECG: { 
                cons.CONS_QUERY_PUSH_QUERY: {
                cons.CONS_ECG: f'${lookup_query[cons.CONS_QUERY_AS]}',
                cons.CONS_EXPORTING_REGION: f'${lookup_level_2_query[cons.CONS_QUERY_AS]}'
            }
        }
    }
    
    query_data = [
        {cons.CONS_QUERY_MATCH_QUERY: match_query},
        {cons.CONS_QUERY_LOOKUP_QUERY: lookup_query},
        {cons.CONS_QUERY_UNWIND_QUERY: unwind_query},
        {cons.CONS_QUERY_LOOKUP_QUERY: lookup_level_2_query},
        {cons.CONS_QUERY_GROUP_QUERY: group_query}
    ]
    output = scraper.find_nested_with_aggregate(record_set_col,query_data)
    
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
