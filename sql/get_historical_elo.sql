with historical_elo as (
    select 
        d_d_id, elo_ranking, elo_date
    from base.elo
)
select 
    d.d_name,
    e.elo_ranking,
    e.elo_date
from historical_elo e
inner join base.drivers d
on
    e.d_d_id = d.d_id
;