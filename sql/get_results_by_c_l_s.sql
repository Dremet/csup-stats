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
),
selected_events as (
	select * from base.events e
	right join selected_season s on e.s_s_id = s.s_id
),
selected_races as (
	select * from base.races r
	right join selected_events e on e.e_id = r.e_e_id
)
select * from selected_races r
left join base.race_results rr on r.r_id = rr.r_r_id
left join base.quali_results q on r.r_id = q.r_r_id and rr.d_d_id = q.d_d_id
left join base.team_mappings tm on r.s_id = tm.s_s_id and rr.d_d_id = tm.d_d_id
left join base.teams t on t.t_id = tm.t_t_id
left join base.drivers d on d.d_id = rr.d_d_id
;