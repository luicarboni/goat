CREATE OR REPLACE FUNCTION basic.trigger_update_poi_modified() 
RETURNS TRIGGER AS $trigger_update_poi_modified$
DECLARE 
	user_id integer; 
BEGIN
	
	SELECT s.user_id  
	INTO user_id 
	FROM customer.scenario s 
	WHERE s.id = NEW.scenario_id; 
	
	PERFORM basic.reached_pois_heatmap('poi_modified'::text, NEW.geom, user_id, NEW.scenario_id, ARRAY[0]::integer[], NEW.uid); 
	RETURN NEW;

END;
$trigger_update_poi_modified$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_poi_modified ON customer.poi_modified; 
CREATE TRIGGER trigger_update_poi_modified AFTER UPDATE ON customer.poi_modified
FOR EACH ROW EXECUTE PROCEDURE basic.trigger_update_poi_modified();