import logging

logging.basicConfig(filename='user_activity.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def add_movie(movie_title, genre, actors, category, rating, frames, reviews):
    logging.info('Добавлен новый фильм: %s', movie_title)
    logging.info('Жанры: %s', genre)
    logging.info('Актеры: %s', actors)
    logging.info('Категории: %s', category)
    logging.info('Рейтинг: %s', rating)
    logging.info('Изображения кадров фильма: %s', frames)
    logging.info('Отзывы: %s', reviews)


add_movie(
    movie_title='Название фильма',
    genre=['Жанр1', 'Жанр2'],
    actors=['Актер1', 'Актер2'],
    category='Категория',
    rating=8.5,
    # frames=['Кадр1.jpg', 'Кадр2.jpg'],
    reviews={'user1': {'like': True, 'comment': 'Отличный фильм!'},
             'user2': {'like': False, 'comment': 'Не понравился'}}
)
