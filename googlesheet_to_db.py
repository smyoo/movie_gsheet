import movie_data as mv

sheet_url = mv.config['googlesheet']['url_sjyoo']
sheet_name = "연도별 외국영화 수입현황의 사본"
worksheet = mv.connect_googlesheet(sheet_url, sheet_name)
range_list = worksheet.range('A2:K999')
range_list.append("end")
sql_list = []
values = []
row_no = 0
cnt = 0
for cell in range_list:
    if cell == "end":
        break
    if row_no > 0 and row_no < cell.row :
        if values[0] == '':
            continue
        sql = "insert into movie_info values ('{0}');".format("', '".join(values))
        sql_list.append(sql)
        row_no = cell.row
        values = []
        values.append(cell.value.replace("'", "\\'"))
        cnt = cnt + 1
    else:
        values.append(cell.value.replace("'", "\\'"))
        row_no = cell.row
mv.init_table("movie_info")
mv.insert_into_table(sql_list)
print(">>> Completed.. {0} rows inserted.".format(cnt))