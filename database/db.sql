-- NOTE: the code below contains the SQL for the object itself
-- as well as for its dependencies or children (if applicable).
-- 
-- This feature is only a convenience in order to allow you to test
-- the whole object's SQL definition at once.
-- 
-- When exporting or generating the SQL for the whole database model
-- all objects will be placed at their original positions.


-- object: tempotech | type: SCHEMA --
-- DROP SCHEMA IF EXISTS tempotech CASCADE;
CREATE SCHEMA tempotech;
-- ddl-end --
ALTER SCHEMA tempotech OWNER TO weather;
-- ddl-end --

-- object: tempotech."Location" | type: TABLE --
-- DROP TABLE IF EXISTS tempotech."Location" CASCADE;
CREATE TABLE tempotech."Location" (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 0 MAXVALUE 2147483647 START WITH 1 CACHE 1 ),
	country char(2),
	"stateName" varchar(50),
	state char(2),
	city_name varchar(50),
	lat float,
	lon float,
	CONSTRAINT location_pk PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE tempotech."Location" OWNER TO weather;
-- ddl-end --

-- object: tempotech."Weather" | type: TABLE --
-- DROP TABLE IF EXISTS tempotech."Weather" CASCADE;
CREATE TABLE tempotech."Weather" (
	id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT BY 1 MINVALUE 0 MAXVALUE 2147483647 START WITH 1 CACHE 1 ),
	"currentTemperature" numeric,
	"feelsLikeTemperature" numeric,
	"minTemperature" numeric,
	"maxTemperature" numeric,
	humidity numeric,
	"windSpeed" numeric,
	"timestampUtc" timestamp,
	CONSTRAINT "Weather_pk" PRIMARY KEY (id)
);
-- ddl-end --
ALTER TABLE tempotech."Weather" OWNER TO weather;
-- ddl-end --

-- object: tempotech."WeatherLocation" | type: TABLE --
-- DROP TABLE IF EXISTS tempotech."WeatherLocation" CASCADE;
CREATE TABLE tempotech."WeatherLocation" (
	"id_Location" bigint NOT NULL,
	"id_Weather" bigint NOT NULL,
	CONSTRAINT "WeatherLocation_pk" PRIMARY KEY ("id_Location","id_Weather")
);
-- ddl-end --
ALTER TABLE tempotech."WeatherLocation" OWNER TO weather;
-- ddl-end --

-- object: "Location_fk" | type: CONSTRAINT --
-- ALTER TABLE tempotech."WeatherLocation" DROP CONSTRAINT IF EXISTS "Location_fk" CASCADE;
ALTER TABLE tempotech."WeatherLocation" ADD CONSTRAINT "Location_fk" FOREIGN KEY ("id_Location")
REFERENCES tempotech."Location" (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

-- object: "Weather_fk" | type: CONSTRAINT --
-- ALTER TABLE tempotech."WeatherLocation" DROP CONSTRAINT IF EXISTS "Weather_fk" CASCADE;
ALTER TABLE tempotech."WeatherLocation" ADD CONSTRAINT "Weather_fk" FOREIGN KEY ("id_Weather")
REFERENCES tempotech."Weather" (id) MATCH FULL
ON DELETE CASCADE ON UPDATE CASCADE;
-- ddl-end --

