def get_table_rows(table, tag_name='td'):
    teams_body = table.find_element_by_tag_name('tbody')
    rows = teams_body.find_elements_by_tag_name('tr')
    table_rows = [row.find_elements_by_tag_name(
        tag_name) for row in rows if row]
    return [row for row in table_rows if row]


def get_team_abbr(cell): return cell.find_element_by_tag_name(
    'a').get_attribute('href').split('/')[-2]
