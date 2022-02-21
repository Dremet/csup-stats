with latest_elo as (
    select 
        d_d_id, elo_ranking, elo_date
    from base.elo
    group by 
        d_d_id, elo_ranking, elo_date
    having 
        elo_date = max(elo_date)
)
select 
    d.d_name,
    e.elo_ranking,
    e.elo_date,
    d.d_steering_device
from latest_elo e
inner join base.drivers d
on
    e.d_d_id = d.d_id
where d.d_two_letter_continent_code = %(region)s
;