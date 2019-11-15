from app import db, static

def __get_value(values, key):
    try: return values[0][key]
    except (IndexError, KeyError) as e: return None

def generate(start, end):

    formatted = lambda date: "{0}/{1}/{2}".format(date.month, date.day, date.year)
    date_range_header = "%s - %s" % (formatted(start), formatted(end))
    headers = [date_range_header, "Visitors", "Visitors (unique)", "Clones", "Clones (unique)"]
    value_matrix = []

    for family in static.repos()["families"]:
        family_name = family["name"]
        platforms = family["platforms"]
        for platform in platforms:
            # Name
            platform_name = platform["platform"]
            name = "{0} {1}".format(family_name, platform_name)

            # Repo
            platform_repo = platform["repo"]
            agr = [{'$match': {"repo": platform_repo, "timestamp": {'$gte': start, '$lt': end}}}, { '$group': {'_id': 1, 'count': { '$sum': "$count" }, 'uniques': { '$sum': "$uniques" } }}]

            # Views
            view = list(db.view.aggregate(agr))
            view_count = __get_value(view, 'count') or 0
            view_uniques = __get_value(view, 'uniques') or 0

            # Clones
            clone = list(db.clone.aggregate(agr))
            clone_count = __get_value(clone, 'count') or 0
            clone_uniques = __get_value(clone, 'uniques') or 0

            # Markdown Output
            value_matrix.append([name, view_count, view_uniques, clone_count, clone_uniques])

    return headers, value_matrix
