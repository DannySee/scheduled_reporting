import pandas as pd
import date_formats as dt


def create_file(filename, headers, content):

    df = pd.DataFrame(content, columns=headers)
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, sheet_name=dt.pretty('today'), index=False)

