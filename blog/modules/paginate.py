import tornado.web


class PaginateModule(tornado.web.UIModule):
    """分页模版"""

    def render(self, page, pages):
        """
        :param page: current page
        :param pages: all pages
        :return: all_page: list of pages
        """
        if not isinstance(page, int) or page < 1: page = 1
        if not isinstance(pages, int): pages = 1
        if page > pages: page = pages

        if pages <= 6:
            all_page = list(range(1, pages + 1))
        else:
            if page in [1, 2]:
                all_page = list(range(1, 4))
                all_page.append(".")
                all_page.append(pages)
            elif page in [pages, pages - 1]:
                all_page = [1, "."]
                all_page.extend(list(range(pages - 3, pages + 1)))

            else:
                all_page = [page - 1, page, page + 1]
                all_page.insert(0, 1)
                if page != 3:
                    all_page.insert(1, ".")
                if page != pages-2:
                    all_page.append(".")
                all_page.append(pages)
        return self.render_string(
            "modules/paginate.html", page=page, all_page=all_page
        )
