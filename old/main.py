import pandas as pd

def org_insta():

    directory = r"C:\Users\João Faelis\Downloads\Unio_1713203246486.9995_posts.xlsx"
    database = pd.read_excel(directory)
    new_df = database.copy()

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
    new_df.to_excel('insta_organization.xlsx', index=False)

def main():
    directory = r'insta_organization.xlsx'
    database = pd.read_excel(directory)
    new_df = database.copy()

    new_id = 1
    df_ordination = new_df.sort_values(by=['SERVICE', 'THREAD_ID', 'URL', 'DATE', 'TIME', 'ID'])

    for index, row in df_ordination.iterrows():
        if row["SERVICE"] in ("facebook", "linkedin"):
            if pd.notnull(row['ID']):
                underlines_count = str(row['ID']).count("_")
                if underlines_count <= 1:
                    df_ordination.loc[index, 'novo_id'] = new_id
                    new_id += 1

                elif underlines_count == 2:
                    splited_id = str(row['ID']).split("_")
                    current_formatted_id = '_'.join(splited_id[:3])
                    previous_row = df_ordination.iloc[index - 1]
                    previous_row_splited_id = str(previous_row['ID']).split("_")
                    previous_row_underlines_count = str(previous_row['ID']).count("_")
                    previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:3])

                    if previous_row_underlines_count == 3:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif current_formatted_id == previous_row_current_formatted_id:
                        df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]
                    else:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1


                elif underlines_count == 3:
                    splited_id = str(row['ID']).split("_")
                    current_formatted_id = '_'.join(splited_id[:3])
                    previous_row = df_ordination.iloc[index - 1]
                    previous_row_underlines_count = str(previous_row['ID']).count("_")
                    previous_row_splited_id = str(previous_row['ID']).split("_")
                    previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:3])

                    if previous_row_underlines_count == 3 and current_formatted_id != previous_row_current_formatted_id:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif current_formatted_id == previous_row_current_formatted_id:
                        df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]

                    else:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1
            else:
                previous_row = df_ordination.iloc[index - 1]

                if previous_row['THREAD_ID'] == row["THREAD_ID"]:
                    df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]
                else:
                    df_ordination.loc[index, 'novo_id'] = new_id
                    new_id += 1

        if row["SERVICE"] == 'tiktok':
            if pd.notnull(row['ID']):
                underlines_count = str(row['ID']).count("_")

                if underlines_count <= 1:
                    df_ordination.loc[index, 'novo_id'] = new_id
                    new_id += 1

                elif underlines_count == 2:
                    splited_id = str(row['ID']).split("_")
                    current_formatted_id = '_'.join(splited_id[:2])
                    previous_row = df_ordination.iloc[index - 1]
                    previous_row_splited_id = str(previous_row['ID']).split("_")
                    previous_row_underlines_count = str(previous_row['ID']).count("_")
                    previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:2])
                    if previous_row_underlines_count == 3:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif current_formatted_id == previous_row_current_formatted_id:
                        df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]
                    else:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1

        if row["SERVICE"] == 'instagram':
            if pd.isnull(row["THREAD_ID"]):
                if pd.notnull(row['ID']):
                    underlines_count = str(row['ID']).count("_")
                    if underlines_count < 1:
                        df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1

                    elif underlines_count == 1:
                        splited_id = str(row['ID']).split("_")
                        current_formatted_id = '_'.join(splited_id[:2])
                        previous_row = df_ordination.iloc[index - 1]
                        previous_row_splited_id = str(previous_row['ID']).split("_")
                        previous_row_underlines_count = str(previous_row['ID']).count("_")
                        previous_row_current_formatted_id = '_'.join(previous_row_splited_id[:2])

                        if previous_row_underlines_count == 1 and current_formatted_id == previous_row_current_formatted_id:
                            df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]
                        else:
                            df_ordination.loc[index, 'novo_id'] = new_id
                        new_id += 1
            else:
                # Caso a coluna THREAD_ID não esteja vazia
                previous_row = df_ordination.iloc[index - 1]
                if previous_row['THREAD_ID'] == row["THREAD_ID"]:
                    df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]
                else:
                    df_ordination.loc[index, 'novo_id'] = new_id
                new_id += 1


        if row["SERVICE"] == 'youtube':
            if pd.notnull(row['ID']):
                points_count = str(row['ID']).count(".")
                if points_count < 1:
                    df_ordination.loc[index, 'novo_id'] = new_id
                    new_id += 1
                elif points_count == 1:
                    splited_id = str(row['ID']).split(".")
                    current_formatted_id = '.'.join(splited_id[:1])
                    previous_row = df_ordination.iloc[index - 1]
                    previous_row_splited_id = str(previous_row['ID']).split(".")
                    previous_row_underlines_count = str(previous_row['ID']).count(".")
                    previous_row_current_formatted_id = '.'.join(previous_row_splited_id[:1])
                    if previous_row_underlines_count == 0 and current_formatted_id == previous_row_current_formatted_id:
                        df_ordination.loc[index, 'novo_id'] = previous_row["novo_id"]
                    else:
                        df_ordination.loc[index, 'novo_id'] = new_id
                    new_id += 1

    df_ordination.to_excel('Base_tratada.xlsx', index=False)


org_insta()
main()

