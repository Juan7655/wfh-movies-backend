from sqlalchemy import text


def get_rolling_avg_movie_ratings(db):
    sql = text("""
select year, ratings_cum_sum / count_cum_sum as moving_rating
from (with T as (
    select EXTRACT(ISOYEAR FROM to_timestamp(timestamp)) as year, sum(rating) as sum_val, count(rating) as vote_count
    from rating where movie = 33154
    group by year order by year
) Select T.year,
             sum(T.sum_val) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)    as ratings_cum_sum,
             sum(T.vote_count) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) as count_cum_sum
      from T) as U;
    """)
    return dict((int(i), j) for i, j in db.execute(sql))
