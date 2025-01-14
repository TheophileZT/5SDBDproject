import os

import pandas as pd


def merger_two_csv(csv1_name,csv2_name):
    
    csv1_path = os.path.join("filtered_data", csv1_name)
    csv2_path = os.path.join("filtered_data", csv2_name)
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)

    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])

    # Fusionner les deux DataFrames sur le champ 'timestamp'
    merged_df = pd.merge(df1, df2, on='timestamp', how='inner')  # 'inner' pour conserver uniquement les lignes correspondantes

    # Exporter le résultat dans un nouveau fichier CSV
    csv1_base = os.path.splitext(csv1_name)[0]
    csv2_base = os.path.splitext(csv2_name)[0]
    output_name = f"merge_{csv1_base}_{csv2_base}.csv"
    output_path = os.path.join("filtered_data", output_name)
    merged_df.to_csv(output_path, index=False)

    print(f"Fichier fusionné exporté avec succès : {output_path}")


##il y a soucis de merger
def merger_three_csv(csv1_name,csv2_name,csv3_name):
    
    csv1_path = os.path.join("filtered_data", csv1_name)
    csv2_path = os.path.join("filtered_data", csv2_name)
    csv3_path = os.path.join("filtered_data", csv3_name)
    df1 = pd.read_csv(csv1_path)
    df2 = pd.read_csv(csv2_path)
    df3 = pd.read_csv(csv3_path)

    df1['timestamp'] = pd.to_datetime(df1['timestamp'])
    df2['timestamp'] = pd.to_datetime(df2['timestamp'])
    df3['timestamp'] = pd.to_datetime(df3['timestamp'])

    # Fusionner les deux DataFrames sur le champ 'timestamp'
    merged_df = pd.merge(df1, df2, on='timestamp', how='inner')
    merged_df = pd.merge(merged_df, df3, on='timestamp', how='left')

    # Les colonnes id_event et closest_stations resteront NaN si aucun événement ne correspond
    merged_df['id_event'] = merged_df['id_event'].fillna('null')
    merged_df['closest_stations'] = merged_df['closest_stations'].fillna('null')


    # Exporter le résultat dans un nouveau fichier CSV
    csv1_base = os.path.splitext(csv1_name)[0]
    csv2_base = os.path.splitext(csv2_name)[0]
    csv3_base = os.path.splitext(csv3_name)[0]
    output_name = f"merge_{csv1_base}_{csv2_base}_{csv3_base}.csv"
    output_path = os.path.join("filtered_data", output_name)
    
    merged_df.to_csv(output_path, index=False)
    print(f"Fichier fusionné exporté avec succès : {output_path}")

