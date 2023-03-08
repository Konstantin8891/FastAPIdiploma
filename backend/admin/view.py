from flask import url_for, request, redirect
from flask_login import current_user
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from markupsafe import Markup
from sqlalchemy.orm import selectinload, joinedload, scoped_session, sessionmaker
from wtforms import StringField, TextAreaField, validators

import sys
sys.path.append('..')

from database import SessionLocal, engine
from models import Favorite, IngredientAmount


# current_session = scoped_session(sessionmaker(
#     autocommit=False, autoflush=False, bind=engine
# ))

PAGE_SIZE = 10


class UserView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    # def is_accessible(self):
    #     return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     app.logger.info('request.url = ', request.url)
    #     return redirect(url_for('login', next=request.url))


class TagView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    # def is_accessible(self):
    #     return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('login', next=request.url))


class IngredientView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    # def is_accessible(self):
    #     return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('login', next=request.url))


# class LocationImageInlineModelForm(object):
#     # Setup AJAX lazy-loading for the ImageType inside the inline model
#     form_ajax_refs = {
#         "image_type": QueryAjaxModelLoader(
#             name="image_type",
#             session=current_session,
#             model=IngredientAmount,
#             fields=("amount",),
#             order_by="id",
#             placeholder="Please use an AJAX query to select an image type for the image",
#             # minimum_input_length=0,
#         )
#     }


# class IngredientAmountView(ModelView):
#     column_display_all_relations = True
#     form_columns = ('id', 'ingredient', 'amount')
#     inline_models = ((Ingredient, {'form_columns': ('id', 'name', 'measurement_unit')}), )


class RecipeView(ModelView):

    def _list_thumbnail(view, context, model, name):
        if not model.image:
            return ''

        return Markup('<img src="%s">' % model.image)

    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    # column_auto_select_related = True
    # column_select_related_list = ('ingredients', 'ingredients.ingredient')
    column_display_pk = True
    column_display_all_relations = True
    # column_display_actions = True
    column_filters = ('name', 'author.username', 'tags.name')
    # column_list = ('name', 'ingredients', 'custom_field')
    # form_columns = [Recipe.name, ]
    column_exclude_list = ('favorites_r', 'shoppingcart_r')
    column_details_exclude_list = ('favorites_r', 'shoppingcart_r')
    create_template = 'create_recipe.html'
    # column_sortable_list = ('id', ) 
    # edit_modal = True

    inline_models = ((
        IngredientAmount,
        {
            'form_columns': ('id', 'amount', 'ingredient'),
        }
    ),) # работает
    column_formatters = {
        'image': _list_thumbnail
    }
    form_extra_fields = {'image': form.ImageUploadField}
    # form_ajax_refs = {
    #     'ingredients': {
    #         'fields': ('id', 'amount', 'ingredient'),
    #         'placeholder': 'Please select',
    #         'page_size': 10,
    #         'minimum_input_length': 0,
    #     }
    # }
    page_size = 10 # работает
    column_list = (
        'id',
        'name',
        'text',
        'cooking_time',
        'image',
        'ingredients',
        'tags',
        'author',
        'created',
        'favorites'
    )
    # inline_models = (IngredientAmountView(IngredientAmount, current_session), )
    # inline_models = (LocationImageInlineModelForm, )
    # form_ajax_refs = {
    #     "image_type": QueryAjaxModelLoader(
    #         name="image_type",
    #         session=current_session,
    #         model=IngredientAmount,
    #         fields=("amount", "ingredient"),
    #         order_by="id",
    #         placeholder="Please use an AJAX query to select an image type for the image",
    #         # minimum_input_length=0,
    #     )
    # }
    # column_filters = ('name', 'author.username', 'tags.name', 'ingredientamount.amount')
        # column_auto_select_related = True
    # form_ajax_refs = {
    #     'recipe': QueryAjaxModelLoader('recipe', current_session, Recipe, fields=['ingredients'], page_size=10)
    # }
    # form_ajax_refs = {
    #     'ingredients': {
    #         'fields': ['ingredient_id', 'amount'],
    #         'page_size': 10
    #     }
    # }
    # inline_models = ['ingredients', ]
    # def is_accessible(self):
    #     return current_user.is_authenticated

    # def inaccessible_callback(self, name, **kwargs):
    #     return redirect(url_for('login', next=request.url))

    # def get_query(self):
    #     return self.session.query(Recipe).order_by(Recipe.id).options(
    #         joinedload(Recipe.ingredients).joinedload(IngredientAmount.ingredient)
    #         # joinedload(Recipe.ingredients)
    #     ).options(joinedload(Recipe.tags)).options(
    #         joinedload(Recipe.author)
    #     )
    
    # def get_query(self):
    #     query = super().get_query()
    #     return query.order_by(Recipe.id)

    # def get_list(self, page, sort_column, sort_desc, search, filters,
    #              execute=True, page_size=None):
    #     """
    #         Return records from the database.

    #         :param page:
    #             Page number
    #         :param sort_column:
    #             Sort column name
    #         :param sort_desc:
    #             Descending or ascending sort
    #         :param search:
    #             Search query
    #         :param execute:
    #             Execute query immediately? Default is `True`
    #         :param filters:
    #             List of filter tuples
    #         :param page_size:
    #             Number of results. Defaults to ModelView's page_size. Can be
    #             overriden to change the page_size limit. Removing the page_size
    #             limit requires setting page_size to 0 or False.
    #     """

    #     # Will contain join paths with optional aliased object
    #     joins = {}
    #     count_joins = {}

    #     query = self.get_query()
    #     count_query = self.get_count_query() if not self.simple_list_pager else None

    #     # Apply search criteria
    #     if self._search_supported and search:
    #         query, count_query, joins, count_joins = self._apply_search(query,
    #                                                                     count_query,
    #                                                                     joins,
    #                                                                     count_joins,
    #                                                                     search)

    #     # Apply filters
    #     if filters and self._filters:
    #         query, count_query, joins, count_joins = self._apply_filters(query,
    #                                                                      count_query,
    #                                                                      joins,
    #                                                                      count_joins,
    #                                                                      filters)

    #     # Calculate number of rows if necessary
    #     count = count_query.scalar() if count_query else None

    #     # Auto join
    #     # for j in self._auto_joins:
    #     #     query = query.options(joinedload(j))

    #     # Sorting
    #     query, joins = self._apply_sorting(query, joins, sort_column, sort_desc)

    #     # Pagination
    #     query = self._apply_pagination(query, page, page_size)

    #     # Execute if needed
    #     # if execute:
    #     #     query = query.all()

    #     return count, query

# admin.add_view(UserView(User, SessionLocal))
# admin.add_view(TagView(Tag, SessionLocal))
# admin.add_view(IngredientView(Ingredient, SessionLocal))
# admin.add_view(RecipeView(Recipe, SessionLocal))
