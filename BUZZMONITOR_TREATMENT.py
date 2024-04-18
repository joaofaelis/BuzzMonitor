import pandas as pd
import os
import shutil

def org_insta():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    directory_base = os.path.join(script_dir, "database_original")
    directory_base_log = os.path.join(script_dir, 'bases_log')
    excel_path = os.path.join(directory_base_log, "insta_organization.xlsx")

    dfs = []

    for name_archive in os.listdir(directory_base):
        full_path = os.path.join(directory_base, name_archive)

        if os.path.isfile(full_path) and name_archive.endswith('.xlsx'):
            df = pd.read_excel(full_path)
            dfs.append(df)

    database_concat = pd.concat(dfs, ignore_index=True)
    new_df = database_concat.copy()

    url_dict = {}
    new_df['URL'] = new_df['URL'].astype(str)
    link_menor_list = {}

    for index, row in new_df.iterrows():
        if row["SERVICE"] == "instagram" and pd.notnull(row['URL']):
            instagram_url = row['URL']
            if instagram_url and instagram_url.startswith('c/'):
                split_link_menor = instagram_url.split('/')
                link_menor = split_link_menor[1]
                apply_link = '/'.join(split_link_menor[2:])
                link_menor_list[link_menor] = apply_link


            if 'https://www.instagram.com/p/' in instagram_url:
                barra_split_insta = instagram_url.split('/')
                if len(barra_split_insta) >= 7:
                    index_url_complete = barra_split_insta[6]
                    link_completo = barra_split_insta[0:7]
                    link_completo_insta = '/'.join(link_completo)
                    if index_url_complete not in url_dict:
                        url_dict[index_url_complete] = link_completo_insta

    for id_link, r in link_menor_list.items():
        for key, value in url_dict.items():
            if key == id_link:
                if r:
                    teste = url_dict[id_link] + '/' + r
                    teste2 = new_df[new_df['URL'] == url_dict[id_link]]
                    new_df.loc[teste2.index, 'URL'] = teste


    new_df = new_df[~new_df['URL'].str.startswith('c/')]
    new_df.to_excel(excel_path, index=False)

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    path_database = os.path.join(script_dir, 'treated_database')
    path_final = os.path.join(path_database, 'Base_tratada.xlsx')
    directory_base_log = os.path.join(script_dir, 'bases_log')
    service_organization = os.path.join(directory_base_log, "service_organization.xlsx")
    archives = os.listdir(directory_base_log)
    for name_archive in archives:
        full_path = os.path.join(directory_base_log, name_archive)
    database_insta = pd.read_excel(full_path)
    df_ordination = database_insta.sort_values(by=['SERVICE', 'THREAD_ID', 'URL', 'DATE', 'TIME', 'ID'])
    df_ordination.to_excel(service_organization, index=False)

    directory_main = service_organization
    database_main = pd.read_excel(directory_main)
    new_df = database_main.copy()
    new_id = 1


    for index, row in new_df.iterrows():
        if row["SERVICE"] in ("facebook", "linkedin"):
            if pd.notnull(row['ID']):
                underlines_count = str(row['ID']).count("_")
                if underlines_count <= 1:
                    new_df.loc[index, 'novo_id'] = new_id
                    new_id += 1

                elif underlines_count == 2:
                    splited_id = str(row['ID']).split("_")
                    current_formatted_id = '_'.join(splited_id[:3])
                    previous_row = new_df.iloc[index - 1]
                    previous_row_splited_id = str(previous_row['ID']).split("_")
                    previous_row_underlines_count = str(previous_row['ID']).count("_")
                    previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:3])

                    if previous_row_underlines_count == 3:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif current_formatted_id == previous_row_current_formatted_id:
                        new_df.loc[index, 'novo_id'] = previous_row["novo_id"]
                    else:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1


                elif underlines_count == 3:
                    splited_id = str(row['ID']).split("_")
                    current_formatted_id = '_'.join(splited_id[:3])
                    previous_row = new_df.iloc[index - 1]
                    previous_row_underlines_count = str(previous_row['ID']).count("_")
                    previous_row_splited_id = str(previous_row['ID']).split("_")
                    previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:3])

                    if previous_row_underlines_count == 3 and current_formatted_id != previous_row_current_formatted_id:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif current_formatted_id == previous_row_current_formatted_id:
                        new_df.loc[index, 'novo_id'] = previous_row["novo_id"]

                    else:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1
            else:
                previous_row = new_df.iloc[index - 1]

                if previous_row['THREAD_ID'] == row["THREAD_ID"]:
                    new_df.loc[index, 'novo_id'] = previous_row["novo_id"]
                else:
                    new_df.loc[index, 'novo_id'] = new_id
                    new_id += 1

        if row["SERVICE"] == 'tiktok':
            if pd.notnull(row['ID']):
                underlines_count = str(row['ID']).count("_")

                if underlines_count <= 1:
                    new_df.loc[index, 'novo_id'] = new_id
                    new_id += 1

                elif underlines_count == 2:
                    splited_id = str(row['ID']).split("_")
                    current_formatted_id = '_'.join(splited_id[:2])
                    previous_row = new_df.iloc[index - 1]
                    previous_row_splited_id = str(previous_row['ID']).split("_")
                    previous_row_underlines_count = str(previous_row['ID']).count("_")
                    previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:2])
                    if previous_row_underlines_count == 3:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif current_formatted_id == previous_row_current_formatted_id:
                        new_df.loc[index, 'novo_id'] = previous_row["novo_id"]
                    else:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1

        if row["SERVICE"] == 'instagram':
            if pd.isnull(row["THREAD_ID"]):
                if pd.notnull(row['ID']):
                    underlines_count = str(row['ID']).count("_")
                    if underlines_count < 1:
                        new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1


                    elif underlines_count == 1:
                        splited_id = str(row['ID']).split("_")
                        current_formatted_id = '_'.join(splited_id[:2])
                        previous_row = new_df.iloc[index - 1]
                        previous_row_splited_id = str(previous_row['ID']).split("_")
                        previous_row_underlines_count = str(previous_row['ID']).count("_")
                        previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:2])

                        if previous_row_underlines_count == 1 and current_formatted_id == previous_row_current_formatted_id:
                            new_df.loc[index, 'novo_id'] = previous_row["novo_id"]
                        else:
                            new_df.loc[index, 'novo_id'] = new_id
                        new_id += 1
            else:
                # Caso a coluna THREAD_ID não esteja vazia
                previous_row = new_df.iloc[index - 1]
                if previous_row['THREAD_ID'] == row["THREAD_ID"]:
                    new_df.loc[index, 'novo_id'] = previous_row["novo_id"]
                else:
                    new_df.loc[index, 'novo_id'] = new_id
                new_id += 1

        if row["SERVICE"] == 'youtube':
            if pd.notnull(row['ID']):
                points_count = str(row['ID']).count(".")
                if points_count < 1:
                    new_df.loc[index, 'novo_id'] = new_id
                    new_id += 1
                elif points_count == 1:
                    splited_id = str(row['ID']).split(".")
                    current_formatted_id = '.'.join(splited_id[:1])
                    previous_row = new_df.iloc[index - 1]
                    previous_row_splited_id = str(previous_row['ID']).split(".")
                    previous_row_underlines_count = str(previous_row['ID']).count(".")
                    previous_row_current_formatted_id = '.'.join(previous_row_splited_id[:1])
                    if previous_row_underlines_count == 0 and current_formatted_id == previous_row_current_formatted_id:
                        new_df.loc[index, 'novo_id'] = previous_row["novo_id"]
                    else:
                        new_df.loc[index, 'novo_id'] = new_id
                    new_id += 1


    new_df.to_excel(path_final, index=False)

    for file in os.listdir(directory_base_log):
        file_path = os.path.join(directory_base_log, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Erro ao tentar excluir {file_path}: {e}")


org_insta()
main()

