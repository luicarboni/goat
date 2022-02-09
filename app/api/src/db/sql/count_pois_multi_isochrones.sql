
CREATE OR REPLACE FUNCTION basic.count_pois_multi_isochrones (userid_input integer, modus text, minutes integer, speed_input numeric, region_type text, region text, amenities text[], scenario_id_input integer DEFAULT 0, active_upload_ids integer[] DEFAULT '{}'::integer[])
    RETURNS TABLE (region_name text, count_pois integer, geom geometry, buffer_geom geometry)
    AS $function$
DECLARE
    buffer_geom geometry;
    region_geom geometry;
    region_name text;
    excluded_pois_id text[] := ARRAY[]::text[];
BEGIN

    IF modus = 'scenario' THEN
        excluded_pois_id = basic.modified_pois(scenario_id_input);
    END IF;

    IF region_type = 'study_area' THEN
        SELECT s.geom, name  
        INTO region_geom, region_name
        FROM basic.sub_study_area s
        WHERE ST_Intersects (s.geom, ST_SETSRID(ST_GeomFromText(region), 4326));
    ELSE
        SELECT ST_GeomFromText(region) 
        INTO region_geom;
        region_name = 'envelope';
    END IF;
    buffer_geom = ST_Buffer(region_geom::geography, speed_input  * 60 * minutes)::geometry;
    
    RETURN query 
	WITH intersected_pois AS (
        SELECT p.id
		FROM basic.poi p
		WHERE ST_Intersects(buffer_geom, p.geom)
		AND p.category IN (SELECT UNNEST(amenities))
		AND p.uid NOT IN (SELECT UNNEST(excluded_pois_id))
		UNION ALL 
		SELECT p.id
		FROM customer.poi_user p
		WHERE ST_Intersects(buffer_geom, p.geom)
		AND p.category IN (SELECT UNNEST(amenities))
		AND p.uid NOT IN (SELECT UNNEST(excluded_pois_id))
		AND p.data_upload_id IN (SELECT UNNEST(active_upload_ids))
		UNION ALL 
		SELECT p.id
		FROM customer.poi_modified p
		WHERE ST_Intersects(buffer_geom, p.geom)
		AND p.category IN (SELECT UNNEST(amenities))
		AND p.scenario_id = scenario_id_input 
    ),
    count_pois AS 
    (
    	SELECT count(*) AS cnt
    	FROM intersected_pois
    )    
    SELECT region_name, c.cnt::integer,
    region_geom, buffer_geom
	FROM count_pois c;
END;
$function$
LANGUAGE plpgsql;

/* Example with starting point to find study_area
SELECT * FROM basic.count_pois_multi_isochrones(1,'scenario',10,1.33,'study_area',
'POINT(11.570115749093093 48.15360025891228)', ARRAY['bar','restaurant','pub','french_supermarket','fancy_market'], 1, ARRAY[3]);
 
 * Example with drawn polygon
SELECT * FROM basic.count_pois_multi_isochrones(1,'scenario',10,1.33,'study_area',
'POLYGON ((11.570115749093093 48.15360025891228, 11.570274296106232 48.1518693270582, 11.572708788648153 48.15118483030911, 11.574984827528402 48.15223125586774, 11.574826384986741 48.15396220424526, 11.57239179909107 48.154646710542, 11.570115749093093 48.15360025891228))',
ARRAY['bar','restaurant','pub','french_supermarket','fancy_market'], 1, ARRAY[3]);
 */
