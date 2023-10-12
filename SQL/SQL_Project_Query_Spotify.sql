USE Spotify
CREATE TABLE tbl_spotify_most_played_23 (
	track_name nvarchar(255),
	artist_name nvarchar(255),
	artist_count int,
	released_year int,
	released_month int,
	released_day int,
	in_spotify_playlists int,
	in_spotify_charts int,
	streams int,
	in_apple_playlists int,
	in_apple_charts int,
	in_deezer_playlists int,
	in_deezer_charts int,
	in_shazam_charts int,
	bpm int,
    key_ varchar(10),
    mode varchar(10),
    danceability int,
    valence int,
    energy int,
    acousticness int,
    instrumentalness int,
    liveness int,
    speechiness int
);
GO
--removing whitespaces on string columns
UPDATE tbl_spotify_most_played_23
SET 
	[track_name] = TRIM(track_name),
	[artist_name] = TRIM(artist_name),
	[key_] = TRIM(key_),
	[mode] = TRIM(mode)
GO


--checking for duplicates
SELECT track_name, COUNT(*) AS total_count
FROM [dbo].[tbl_spotify_most_played_23]
GROUP BY track_name
HAVING COUNT(*) > 1
GO

--streams datatype to bigint bc of overflow error.
ALTER TABLE tbl_spotify_most_played_23
ALTER COLUMN streams bigint
GO


/*Adding constraints for data integrity. 
Added CHECK constraint to enusre streams are positive.*/
ALTER TABLE [dbo].[tbl_spotify_most_played_23]
ADD CONSTRAINT ck_streams_pos CHECK (streams > 0)
GO

--if no year is provided, default to 2023. 
ALTER TABLE [dbo].[tbl_spotify_most_played_23]
ADD CONSTRAINT df_release_year DEFAULT 2023 FOR released year


--total streams by artists 
SELECT TOP(3) artist_name, SUM(streams) AS TotalStreams
FROM tbl_spotify_most_played_23
GROUP BY artist_name
ORDER BY TotalStreams DESC; 
GO

--avg Danceability by mode
SELECT mode, AVG(danceability) AS AVGDanceability
FROM tbl_spotify_most_played_23
GROUP BY mode
GO

--monthly stream trends
SELECT Top(3) DATENAME(MONTH,DATEFROMPARTS(released_year, released_month,01)) AS theMonth, SUM(streams) AS TotalStreams, LEN(SUM(streams)) AS lengt
FROM tbl_spotify_most_played_23
GROUP BY released_month, released_year
ORDER BY TotalStreams DESC
GO

--finding highest valence with all track_name that starts with the word 'love'
SELECT track_name, valence
FROM tbl_spotify_most_played_23
WHERE track_name LIKE '%Love%'
ORDER BY valence DESC
GO

SELECT MAX(valence)
FROM tbl_spotify_most_played_23
GO

--INNER JOINs using INTO
SELECT track_name, danceability
INTO #high_dance_songs
FROM tbl_spotify_most_played_23
WHERE danceability > 70
GO 
SELECT track_name, energy
INTO #high_energy_songs
FROM tbl_spotify_most_played_23
WHERE energy > 80
GO
SELECT hd.track_name ,hd.danceability, he.energy
FROM #high_dance_songs AS hd
JOIN #high_energy_songs AS he
ON hd.track_name = he.track_name
GO

--unique track names that appear in either apple and spotify charts
SELECT track_name
FROM tbl_spotify_most_played_23
WHERE in_spotify_charts = 1
UNION
SELECT track_name
FROM tbl_spotify_most_played_23
WHERE in_apple_charts = 1
GO


--common track names that appear in both apple and spotify charts
SELECT track_name,artist_name
FROM tbl_spotify_most_played_23
WHERE in_spotify_charts = 1
INTERSECT
SELECT track_name,artist_name
FROM tbl_spotify_most_played_23
WHERE in_apple_charts = 1
GO

--CASE statement with a derived table to find out avg energy for each danceability group.
SELECT 
	Danceability_grp,
	AVG(energy) AS avg_energy
FROM (
	SELECT
		CASE
			WHEN danceability >= 70 THEN 'High Danceability'
			WHEN danceability BETWEEN 40 AND 69 THEN 'Moderate Danceability'
			ELSE 'Low Danceability'
		END AS Danceability_grp, 
		energy
	FROM tbl_spotify_most_played_23
) AS sb_query
GROUP BY Danceability_grp
ORDER BY avg_energy
GO

--Rankings tracks by streams within each month
SELECT released_month, track_name, streams,
		RANK() OVER (PARTITION BY released_month ORDER BY streams DESC) AS monthly_rank
FROM tbl_spotify_most_played_23
GO


--categorizing beats per minute using a Scalar UDF. 
CREATE FUNCTION dbo.fn_bpm_category (@bpm int)
RETURNS NVARCHAR(20)
AS
BEGIN
    DECLARE @category NVARCHAR(20)

    IF @bpm < 100
        SET @category = 'Slow'
    ELSE IF @bpm >= 100 AND @bpm <= 120
        SET @category = 'Moderate'
    ELSE
        SET @category = 'Fast'

    RETURN @category
END
GO
SELECT track_name, bpm, dbo.fn_bpm_category(bpm) AS BPM_Category
FROM tbl_spotify_most_played_23
