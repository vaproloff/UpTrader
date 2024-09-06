from django import template
from menu.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/draw_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    current_url = request.path
    menu_items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent')

    def build_tree(items, parent=None):
        tree = []
        for item in items:
            if item.parent == parent:
                children = build_tree(items, parent=item)
                tree.append({'item': item, 'children': children, 'active': item.get_url() in current_url})
        return tree

    menu_tree = build_tree(menu_items)
    return {'menu': menu_tree}
