class Pager:

    def get_paginated_context(context):
        if context['page_obj'] != None:
            page_obj = context['page_obj']
            if(page_obj.paginator.num_pages > 5):
                if page_obj.number < 3:
                    pages = range(1, 6)
                elif page_obj.number > (page_obj.paginator.num_pages - 3):
                    pages = range((page_obj.paginator.num_pages - 4),
                                  page_obj.paginator.num_pages + 1)
                else:
                    pages = range((page_obj.number - 2), (page_obj.number + 3))
            else:
                pages = range(1, page_obj.paginator.num_pages + 1)
            context['pages'] = pages
        return context
