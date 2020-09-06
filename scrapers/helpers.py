def get_table_rows(table):
    teams_body = table.find_element_by_tag_name('tbody')
    rows = teams_body.find_elements_by_tag_name('tr')
    cell_rows = [row.find_elements_by_tag_name('td') for row in rows]
    return [row for row in cell_rows if row]
