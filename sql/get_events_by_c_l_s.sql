with selected_season as (
	select *
	from base.seasons s
		left join base.leagues l 
			on l_name = %(league)s
		left join base.championships c 
			on c_name = %(cs)s
	where 1=1
		and s.s_desc = %(season)s
		and s.l_l_id = l.l_id 
		and l.c_c_id = c.c_id
)
select * from base.events e
right join selected_season s on e.s_s_id = s.s_id;