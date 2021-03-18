from Packages.parser import Parser


def main():
    """Основная (начальная) точка"""
    a = Parser()
    a.get_url_jobs_tut_by_for_parse()
    a.get_links_for_parse()
    a.parse_jobs_tut_by()
    a.output_values()


if __name__ == "__main__":
    main()
