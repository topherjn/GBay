from data_access.base_data_access_object import BaseDAO

class Report(BaseDAO):
    category_report_sql = "SELECT c.description, count(get_it_now), min(i.get_it_now), max(get_it_now), avg(get_it_now)FROM category c LEFT OUTER JOIN item i ON c.category_id = i.category_id GROUP BY c.category_id ORDER BY c.description"
