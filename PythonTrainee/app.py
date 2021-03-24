from Packages.parser import Parser


def main():
    """Main (starting) point"""
    a = Parser()
    a.get_url_jobs_tut_by_for_parse()
    a.get_soup()
    a.get_links_for_parse()
    a.get_dict_word_count_for_parse()
    a.parse_jobs_tut_by()
    a.get_avg_word_count()
    a.output_values()


if __name__ == "__main__":
    main()
