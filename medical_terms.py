import csv
import pandas as pd


def read_tsv(file_path):
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as tsv_file:
            reader = csv.DictReader(tsv_file, delimiter='\t')
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data

def read_two_column_file(file_path):
    data = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            for line in file:
                parts = line.split(' ', 1)  # Split on the first space
                if len(parts) == 2:
                    data.append({'term': parts[0], 'meaning':parts[1].strip(), 'remark':''})  # Strip any trailing whitespace from the second column
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return data


file_path = './gebruikte_termen.csv'
tsv_data = read_tsv(file_path)
for row in tsv_data:
    print(row)

file_path = './gebruikte_termen2.csv'
file_data = read_two_column_file(file_path)
for row in file_data:
    print(row)

file_data.extend(tsv_data)

file_data = sorted(file_data, key=lambda x: x['term'], reverse=False)

for d in file_data:
    d |= {'status':'enable','case':True}


df = pd.DataFrame.from_dict(file_data)

df.to_csv('terms.csv',index=None)
abbreviations_df = pd.read_csv('./terms.csv',index_col=None)
abbreviations_df = df.loc[df['status']=='enable']
abbreviations_df.shape


def replace_abbreviations_in_column(df, abbreviations_df):

    for index, row in abbreviations_df.iterrows():
        abbreviation = row['term']
        replacement = row['meaning']
        ignore_case = row.get('ignore_case', False)

        # Create regex pattern based on case sensitivity
        flags = re.IGNORECASE if ignore_case else 0
        pattern = r'\b{}\b'.format(re.escape(abbreviation))

        # Replace abbreviations in the column using lambda function
        df['text'] = df['text'].apply(lambda text: re.sub(pattern, replacement, text, flags=flags))

    return df


df_text = pd.DataFrame(['this is a text', 'this is another text'], columns=['text'])
df_text.head()

replace_abbreviations_in_column(df_text,'text',df)


df = df.rename(columns={'case':'ignore_case'})

df['ignore_case'] = df['ignore_case'].apply(lambda x: not x)

df.head()