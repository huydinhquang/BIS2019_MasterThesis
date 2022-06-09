import Controllers.Common as common
import Controllers.Constants as cons

def add_channel(my_col, new_channel):
    current_date = common.get_current_date()
    new_channel_json = {cons.CONS_CHANNEL: new_channel,
                        cons.CONS_CREATED_DATE: current_date, cons.CONS_MODIFIED_DATE: current_date}
    output = my_col.insert_one(new_channel_json)
    if output:
        print('channel_id: ' + str(output))
    return output.inserted_id
