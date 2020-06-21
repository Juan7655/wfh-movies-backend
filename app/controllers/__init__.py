__all__ = ['register_paths', 'movie_controller', 'genre_controller', 'rating_controller', 'review_controller', 'tag_controller',
           'user_controller', 'watchlist_controller', 'recommendation_controller']
paths = {}


def register_paths(app):
    [app.include_router(
        router,
        prefix=f'/{entity_name}',
        tags=[entity_name.capitalize() + 's'],
    ) for entity_name, router in paths.items()]
