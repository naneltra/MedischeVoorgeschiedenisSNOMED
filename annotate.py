import pandas as pd
from pathlib import Path
from tqdm import tqdm
from dotenv import load_dotenv
import os
import typer
from medcat.cat import CAT


app = typer.Typer()

# import importlib
# importlib.reload(snomed_mapping)
# importlib.reload(vumc_mapping)
# importlib.reload(plot_compare)

tqdm.pandas(desc="processing vumc dataextract")
load_dotenv()

##############################################
##      LOAD MEDISCHE VOORGESCHIEDENIS
##############################################

def load_data():
    VOORGESCHIEDENIS_PATH = Path('./data/medische_voorgeschiedenis_processed.csv')

    df = pd.read_csv(VOORGESCHIEDENIS_PATH)

    # df = df.rename(columns={"db_id":"id","diagn_proc":"text"})
    # df = df.set_index('id')
    df = df.loc[~df['diagn_proc'].isna()]
    return df


##############################################
##      ANNOTATE
##############################################


@app.command()
def annotate():
    print("loading data")
    df = load_data()
    
    def data_iterator(data: pd.DataFrame):
        for id, row in data[['diagn_proc']].iterrows():
            yield (id, str(row['diagn_proc']))

    generator = data_iterator(df)

    # df['word_count'] = df.loc[~df['diagn_proc'].isna(),'diagn_proc'].apply(lambda x: len(x.split(' ')))

    # calculate mean document length for batch optimization = 43
    # df.loc[~df['text'].isna(),'text'].apply(lambda x: len(x)).mean()
    # 43 * 8 * 200
    batch_size_chars = 100000
    print('loading model')
    model_location = os.getenv('MODEL_PATH')
    mymodel = CAT.load_model_pack(model_location)
    
    
    # fix spelling 
    mymodel = CAT.load_model_pack('../models/20240603_d4ce199c05d6c6ca.zip')

    print('start annotation')
    results = mymodel.multiprocessing_batch_char_size(tqdm(generator, total=df.shape[0]),  # Formatted data
                                                batch_size_chars = batch_size_chars,
                                                nproc=10)

    def get_snomed_results(id: str):
        if id not in results:
            return []
        if 'entities' in results[id]:
            entities_dict = results[id]['entities']
            return [(v['pretty_name'],v['cui'],v['meta_anns']['Negation']['value'],v['type_ids'][0]) for k,v in entities_dict.items()]
        return []

    df['concepts'] = df.apply(lambda x: get_snomed_results(x.name), axis=1)
    print('save to disk')
    df.to_csv('./data/output.csv',index=None)

    # df['concepts'] = df['concepts'].apply(lambda x: list(eval(x)))

    # df_backup = df.copy()
    # df_backup.head()
    # df = df_backup



if __name__ == "__main__":
    app()
