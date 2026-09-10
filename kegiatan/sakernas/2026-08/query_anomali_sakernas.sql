WITH Data_Anomali AS (
        SELECT
        ROW_NUMBER() OVER (ORDER BY CONCAT(art.level_6_full_code, root.no_dsrt, art.ppno)) AS rn,
        art.level_2_code AS KODE_KAB,
        art.level_3_name AS KEC,
        art.level_4_name AS DESA,
        art.level_5_code AS SLS,
        art.level_6_full_code AS "Kode Wilayah",
        CONCAT(art.level_6_full_code, root.no_dsrt, art.ppno) AS ID_ART,
        root.namakrt AS KRT,
        art.dem_name AS nama_art,

        CONCAT('PML: ', p.PML, '; PPL: ', p.PPL, '; Status: ', base.assignment_status_alias) AS petugas,
        CONCAT(root.catatan, '; ', root.survey_period_id) AS catatan,
        CONCAT('https://fasih-sm.bps.go.id/app/assignment-detail/', art.assignment_id) AS Link,

        -- ==========================================
        -- BLOK ANOMALI A
        -- ==========================================
        CASE 
            WHEN dem_age >= 5 AND mjj_kbli_value IS NOT NULL AND (mjj_kbli_value IN (59111, 59121, 59131, 60311, 85101, 85201, 85311, 85315, 85321, 85401, 85403, 85550, 85560, 86101, 86102, 86104, 87101, 87201, 87301, 88101, 88901, 91111, 91121, 91211, 91221) OR (mjj_kbli_value >= 84111 AND mjj_kbli_value <= 84300)) AND mjj_emprel_value IS NOT NULL AND mju_ins_value IS NOT NULL AND (mjj_emprel_value IN (2, 3) OR mju_ins_value <> 1) THEN 1 ELSE 0 
        END AS A1,
        CASE 
            WHEN dem_age >= 5 AND sjj_kbli_value IS NOT NULL AND (sjj_kbli_value IN (59111, 59121, 59131, 60311, 85101, 85201, 85311, 85315, 85321, 85401, 85403, 85550, 85560, 86101, 86102, 86104, 87101, 87201, 87301, 88101, 88901, 91111, 91121, 91211, 91221) OR (sjj_kbli_value >= 84111 AND sjj_kbli_value <= 84300)) AND sjj_emprel_value IS NOT NULL AND sjj_emprel_value IN (2, 3) THEN 1 ELSE 0 
        END AS A2,
        CASE 
            WHEN dem_age >= 5 AND mpk_kbli_value IS NOT NULL AND (mpk_kbli_value IN (59111, 59121, 59131, 60311, 85101, 85201, 85311, 85315, 85321, 85401, 85403, 85550, 85560, 86101, 86102, 86104, 87101, 87201, 87301, 88101, 88901, 91111, 91121, 91211, 91221) OR (mpk_kbli_value >= 84111 AND mpk_kbli_value <= 84300)) AND mpk_status_value IS NOT NULL AND mpk_status_value IN (1, 2, 3, 7) THEN 1 ELSE 0 
        END AS A3,

        -- ==========================================
        -- BLOK ANOMALI B
        -- ==========================================
        CASE WHEN dem_age >= 5 AND dem_edl_value IS NOT NULL AND dem_edl_value < 8 AND mjj_kbji_value IN (1111, 1112, 2141, 2142, 2143, 2144, 2145, 2146, 2149, 2151, 2152, 2153, 2161, 2162, 2163, 2211, 2212, 2250, 2261, 2262, 2263, 2264, 2265, 2266, 2267, 2310, 2330, 2411, 2611, 2612, 2619, 2631, 2632, 2634) THEN 1 ELSE 0 END AS B1,
        CASE WHEN dem_age >= 5 AND dem_edl_value IS NOT NULL AND dem_edl_value < 8 AND sjj_kbji_value IN (1111, 1112, 2141, 2142, 2143, 2144, 2145, 2146, 2149, 2151, 2152, 2153, 2161, 2162, 2163, 2211, 2212, 2250, 2261, 2262, 2263, 2264, 2265, 2266, 2267, 2310, 2330, 2411, 2611, 2612, 2619, 2631, 2632, 2634) THEN 1 ELSE 0 END AS B2,
        CASE WHEN dem_age >= 5 AND dem_edl_value IS NOT NULL AND dem_edl_value < 8 AND mpk_kbji_value IN (1111, 1112, 2141, 2142, 2143, 2144, 2145, 2146, 2149, 2151, 2152, 2153, 2161, 2162, 2163, 2211, 2212, 2250, 2261, 2262, 2263, 2264, 2265, 2266, 2267, 2310, 2330, 2411, 2611, 2612, 2619, 2631, 2632, 2634) THEN 1 ELSE 0 END AS B3,

        -- ==========================================
        -- BLOK ANOMALI C
        -- ==========================================
        CASE WHEN dem_age >= 5 AND dem_edl_value IS NOT NULL AND (dem_edl_value >= 4 AND dem_edl_value <= 12) AND (dem_edf_kd_value IS NULL OR dem_edf_kd_value = '') THEN 1 ELSE 0 END AS C1,
        CASE WHEN dem_age >= 5 AND dem_p1th_value IS NOT NULL AND dem_p1th_value = 1 AND (dem_kdpl_x_value IS NULL OR dem_kdpl_x_value = '') THEN 1 ELSE 0 END AS C2,
        CASE WHEN dem_age >= 5 AND mjj_emprel_value IS NOT NULL AND (mjj_kbli_value IS NULL OR mjj_kbli_value = '') THEN 1 ELSE 0 END AS C3,
        CASE WHEN dem_age >= 5 AND mjj_emprel_value IS NOT NULL AND (mjj_kbji_value IS NULL OR mjj_kbji_value = '') THEN 1 ELSE 0 END AS C4,
        CASE WHEN dem_age >= 5 AND sjb_text_value IS NOT NULL AND sjb_text_value = 1 AND (sjj_kbli_value IS NULL OR sjj_kbli_value = '') THEN 1 ELSE 0 END AS C5,
        CASE WHEN dem_age >= 5 AND sjb_text_value IS NOT NULL AND sjb_text_value = 1 AND (sjj_kbji_value IS NULL OR sjj_kbji_value = '') THEN 1 ELSE 0 END AS C6,
        CASE WHEN dem_age >= 5 AND mpk_henti_value IS NOT NULL AND mpk_henti_value = 1 AND (mpk_kbli_value IS NULL OR mpk_kbli_value = '') THEN 1 ELSE 0 END AS C7,
        CASE WHEN dem_age >= 5 AND mpk_henti_value IS NOT NULL AND mpk_henti_value = 1 AND (mpk_kbji_value IS NULL OR mpk_kbji_value = '') THEN 1 ELSE 0 END AS C8,
        CASE WHEN dem_age >= 15 AND pkln_wkt_y IS NOT NULL AND pkln_wkt_m_value IS NOT NULL AND ((pkln_wkt_y = 2021 AND pkln_wkt_m_value >= 8) OR (pkln_wkt_y = 2025 AND pkln_wkt_m_value <= 8) OR (pkln_wkt_y > 2021 AND pkln_wkt_y < 2025)) AND (pkln_kbli_value IS NULL OR pkln_kbli_value = '') THEN 1 ELSE 0 END AS C9,
        CASE WHEN dem_age >= 15 AND pkln_wkt_y IS NOT NULL AND pkln_wkt_m_value IS NOT NULL AND ((pkln_wkt_y = 2021 AND pkln_wkt_m_value >= 8) OR (pkln_wkt_y = 2025 AND pkln_wkt_m_value <= 8) OR (pkln_wkt_y > 2021 AND pkln_wkt_y < 2025)) AND (pkln_kbji_value IS NULL OR pkln_kbji_value = '') THEN 1 ELSE 0 END AS C10,

        -- ==========================================
        -- BLOK ANOMALI D
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbli_value IS NOT NULL AND (mjj_kbli_value >= 84111 AND mjj_kbli_value <= 84300) AND mjjemprel1_value IS NOT NULL AND mjj_emprel_value IS NOT NULL AND mig_ctz_value IS NOT NULL AND mjj_rem_ta_value IS NOT NULL AND mjj_p_uph_value IS NOT NULL AND (mjjemprel1_value = 2 OR mjj_emprel_value IN (2, 3, 5) OR mig_ctz_n_value = 2 OR mjj_rem_ta_value = 2 OR mjj_p_uph_value <> 1) THEN 1 ELSE 0 END AS D1,
        CASE WHEN dem_age >= 5 AND sjj_kbli_value IS NOT NULL AND (sjj_kbli_value >= 84111 AND sjj_kbli_value <= 84300) AND sjjemprel1_value IS NOT NULL AND sjj_emprel_value IS NOT NULL AND mig_ctz_value IS NOT NULL AND sjd_rem_ta_value IS NOT NULL AND (sjjemprel1_value = 2 OR sjj_emprel_value IN (2, 3, 5) OR mig_ctz_value = 2 OR sjd_rem_ta_value = 2) THEN 1 ELSE 0 END AS D2,
        CASE WHEN dem_age >= 5 AND mpk_kbli_value IS NOT NULL AND (mpk_kbli_value >= 84111 AND mpk_kbli_value <= 84300) AND mpk_status_value IS NOT NULL AND mig_ctz_value IS NOT NULL AND (mpk_status_value IN (1, 2, 3, 5, 6, 7, 9) OR mig_ctz_value = 2) THEN 1 ELSE 0 END AS D3,

        -- ==========================================
        -- BLOK ANOMALI E
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_emprel_value IS NOT NULL AND mjj_emprel_value = 5 AND mjj_kbji_value IS NOT NULL AND (mjj_kbji_value >= 0111 AND mjj_kbji_value <= 4419) THEN 1 ELSE 0 END AS E1,
        CASE WHEN dem_age >= 5 AND sjj_emprel_value IS NOT NULL AND sjj_emprel_value = 5 AND sjj_kbji_value IS NOT NULL AND (sjj_kbji_value >= 0111 AND sjj_kbji_value <= 4419) THEN 1 ELSE 0 END AS E2,
        CASE WHEN dem_age >= 5 AND mpk_status_value IS NOT NULL AND mpk_status_value = 9 AND mpk_kbji_value IS NOT NULL AND (mpk_kbji_value >= 0111 AND mpk_kbji_value <= 4419) THEN 1 ELSE 0 END AS E3,

        -- ==========================================
        -- BLOK ANOMALI F
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_emprel_value IS NOT NULL AND mjj_emprel_value = 5 AND mjj_kbli_value IS NOT NULL AND ((mjj_kbli_value > 82990 AND mjj_kbli_value < 85101) OR (mjj_kbli_value > 85104 AND mjj_kbli_value < 85560) OR (mjj_kbli_value > 85699 AND mjj_kbli_value < 86201) OR (mjj_kbli_value > 63900 AND mjj_kbli_value < 64191) OR (mjj_kbli_value > 64999 AND mjj_kbli_value < 66149) OR (mjj_kbli_value > 33203 AND mjj_kbli_value < 35133) OR (mjj_kbli_value > 28152 AND mjj_kbli_value < 30912) OR (mjj_kbli_value > 10423 AND mjj_kbli_value < 10501) OR mjj_kbli_value IN (85578, 87301, 87991, 66292, 64920, 60311, 49111, 49119, 49120, 52212, 35159, 35401, 35202, 20292, 91111, 91121, 91211, 91300, 91221, 94110, 94121, 94200, 94920)) THEN 1 ELSE 0 END AS F1,
        CASE WHEN dem_age >= 5 AND sjj_emprel_value IS NOT NULL AND sjj_emprel_value = 5 AND sjj_kbli_value IS NOT NULL AND ((sjj_kbli_value > 82990 AND sjj_kbli_value < 85101) OR (sjj_kbli_value > 85104 AND sjj_kbli_value < 85560) OR (sjj_kbli_value > 85699 AND sjj_kbli_value < 86201) OR (sjj_kbli_value > 63900 AND sjj_kbli_value < 64191) OR (sjj_kbli_value > 64999 AND sjj_kbli_value < 66149) OR (sjj_kbli_value > 33203 AND sjj_kbli_value < 35133) OR (sjj_kbli_value > 28152 AND sjj_kbli_value < 30912) OR (sjj_kbli_value > 10423 AND sjj_kbli_value < 10501) OR sjj_kbli_value IN (85578, 87301, 87991, 66292, 64920, 60311, 49111, 49119, 49120, 52212, 35159, 35401, 35202, 20292, 91111, 91121, 91211, 91300, 91221, 94110, 94121, 94200, 94920)) THEN 1 ELSE 0 END AS F2,
        CASE WHEN dem_age >= 5 AND mpk_status_value IS NOT NULL AND mpk_status_value = 9 AND mpk_kbli_value IS NOT NULL AND ((mpk_kbli_value > 82990 AND mpk_kbli_value < 85101) OR (mpk_kbli_value > 85104 AND mpk_kbli_value < 85560) OR (mpk_kbli_value > 85699 AND mpk_kbli_value < 86201) OR (mpk_kbli_value > 63900 AND mpk_kbli_value < 64191) OR (mpk_kbli_value > 64999 AND mpk_kbli_value < 66149) OR (mpk_kbli_value > 33203 AND mpk_kbli_value < 35133) OR (mpk_kbli_value > 28152 AND mpk_kbli_value < 30912) OR (mpk_kbli_value > 10423 AND mpk_kbli_value < 10501) OR mpk_kbli_value IN (85578, 87301, 87991, 66292, 64920, 60311, 49111, 49119, 49120, 52212, 35159, 35401, 35202, 20292, 91111, 91121, 91211, 91300, 91221, 94110, 94121, 94200, 94920)) THEN 1 ELSE 0 END AS F3,

        -- ==========================================
        -- BLOK ANOMALI G
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND mjj_kbli_value IS NOT NULL AND mjj_kbji_value = 2320 AND mjj_kbli_value NOT IN (85321, 85322, 85323, 85324, 85401, 85402, 85403, 85404) THEN 1 ELSE 0 END AS G1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND sjj_kbli_value IS NOT NULL AND sjj_kbji_value = 2320 AND sjj_kbli_value NOT IN (85321, 85322, 85323, 85324, 85401, 85402, 85403, 85404) THEN 1 ELSE 0 END AS G2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND mpk_kbli_value IS NOT NULL AND mpk_kbji_value = 2320 AND mpk_kbli_value NOT IN (85321, 85322, 85323, 85324, 85401, 85402, 85403, 85404) THEN 1 ELSE 0 END AS G3,

        -- ==========================================
        -- BLOK ANOMALI H
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND mjj_kbli_value IS NOT NULL AND mjj_kbji_value = 2330 AND mjj_kbli_value NOT IN (85311, 85312, 85313, 85314, 85315, 85316, 85317, 85318, 85321, 85322, 85323, 85324, 85330) THEN 1 ELSE 0 END AS H1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND sjj_kbli_value IS NOT NULL AND sjj_kbji_value = 2330 AND sjj_kbli_value NOT IN (85311, 85312, 85313, 85314, 85315, 85316, 85317, 85318, 85321, 85322, 85323, 85324, 85330) THEN 1 ELSE 0 END AS H2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND mpk_kbli_value IS NOT NULL AND mpk_kbji_value = 2330 AND mpk_kbli_value NOT IN (85311, 85312, 85313, 85314, 85315, 85316, 85317, 85318, 85321, 85322, 85323, 85324, 85330) THEN 1 ELSE 0 END AS H3,

        -- ==========================================
        -- BLOK ANOMALI I
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjjemprel1_value IS NOT NULL AND mjj_kbji_value IS NOT NULL AND mjj_kbli_value IS NOT NULL AND mju_ins_value IS NOT NULL AND (mjj_kbji_value >= 0111 AND mjj_kbji_value <= 0315) AND (mjj_kbli_value < 84221 OR mjj_kbli_value > 84232 OR mjjemprel1_value <> 1 OR mju_ins_value <> 1) THEN 1 ELSE 0 END AS I1,
        CASE WHEN dem_age >= 5 AND sjjemprel1_value IS NOT NULL AND sjj_kbji_value IS NOT NULL AND sjj_kbli_value IS NOT NULL AND (sjj_kbji_value >= 0111 AND sjj_kbji_value <= 0315) AND (sjj_kbli_value < 84221 OR sjj_kbli_value > 84232 OR sjjemprel1_value <> 1) THEN 1 ELSE 0 END AS I2,
        CASE WHEN dem_age >= 5 AND mpk_status_value IS NOT NULL AND mpk_kbji_value IS NOT NULL AND mpk_kbli_value IS NOT NULL AND (mpk_kbji_value >= 0111 AND mpk_kbji_value <= 0315) AND (mpk_kbli_value < 84221 OR mpk_kbli_value > 84232 OR mpk_status_value <> 4) THEN 1 ELSE 0 END AS I3,

        -- ==========================================
        -- BLOK ANOMALI J
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND (mjj_kbji_value >= 0111 AND mjj_kbji_value <= 0115) AND (dem_edl_value < 9 OR dem_age < 18) THEN 1 ELSE 0 END AS J1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND (sjj_kbji_value >= 0111 AND sjj_kbji_value <= 0115) AND (dem_edl_value < 9 OR dem_age < 18) THEN 1 ELSE 0 END AS J2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND (mpk_kbji_value >= 0111 AND mpk_kbji_value <= 0115) AND (dem_edl_value < 9 OR dem_age < 18) THEN 1 ELSE 0 END AS J3,

        -- ==========================================
        -- BLOK ANOMALI K
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND (mjj_kbji_value >= 0211 AND mjj_kbji_value <= 0215) AND (dem_edl_value < 4 OR dem_age < 16) THEN 1 ELSE 0 END AS K1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND (sjj_kbji_value >= 0211 AND sjj_kbji_value <= 0215) AND (dem_edl_value < 4 OR dem_age < 16) THEN 1 ELSE 0 END AS K2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND (mpk_kbji_value >= 0211 AND mpk_kbji_value <= 0215) AND (dem_edl_value < 4 OR dem_age < 16) THEN 1 ELSE 0 END AS K3,

        -- ==========================================
        -- BLOK ANOMALI L
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND (mjj_kbji_value >= 0311 AND mjj_kbji_value <= 0315) AND (dem_edl_value < 3 OR dem_age < 16) THEN 1 ELSE 0 END AS L1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND (sjj_kbji_value >= 0311 AND sjj_kbji_value <= 0315) AND (dem_edl_value < 3 OR dem_age < 16) THEN 1 ELSE 0 END AS L2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND (mpk_kbji_value >= 0311 AND mpk_kbji_value <= 0315) AND (dem_edl_value < 3 OR dem_age < 16) THEN 1 ELSE 0 END AS L3,

        -- ==========================================
        -- BLOK ANOMALI M
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND mjj_kbli_value IS NOT NULL AND (mjj_kbji_value IN (1311, 1312, 3142, 3143) OR (mjj_kbji_value >= 6111 AND mjj_kbji_value <= 6340) OR (mjj_kbji_value >= 9211 AND mjj_kbji_value <= 9216)) AND (mjj_kbli_value < 01111 OR mjj_kbli_value > 03300) THEN 1 ELSE 0 END AS M1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND sjj_kbli_value IS NOT NULL AND (sjj_kbji_value IN (1311, 1312, 3142, 3143) OR (sjj_kbji_value >= 6111 AND sjj_kbji_value <= 6340) OR (sjj_kbji_value >= 9211 AND sjj_kbji_value <= 9216)) AND (sjj_kbli_value < 01111 OR sjj_kbli_value > 03300) THEN 1 ELSE 0 END AS M2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND mpk_kbli_value IS NOT NULL AND (mpk_kbji_value IN (1311, 1312, 3142, 3143) OR (mpk_kbji_value >= 6111 AND mpk_kbji_value <= 6340) OR (mpk_kbji_value >= 9211 AND mpk_kbji_value <= 9216)) AND (mpk_kbli_value < 01111 OR mpk_kbli_value > 03300) THEN 1 ELSE 0 END AS M3,

        -- ==========================================
        -- BLOK ANOMALI N
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbli_value IS NOT NULL AND dem_edl_value IS NOT NULL AND ((mjj_kbli_value >= 64110 AND mjj_kbli_value <= 64124) OR (mjj_kbli_value >= 84111 AND mjj_kbli_value <= 84234) OR mjj_kbli_value = 99000) AND dem_edl_value < 2 THEN 1 ELSE 0 END AS N1,
        CASE WHEN dem_age >= 5 AND sjj_kbli_value IS NOT NULL AND dem_edl_value IS NOT NULL AND ((sjj_kbli_value >= 64110 AND sjj_kbli_value <= 64124) OR (sjj_kbli_value >= 84111 AND sjj_kbli_value <= 84234) OR sjj_kbli_value = 99000) AND dem_edl_value < 2 THEN 1 ELSE 0 END AS N2,
        CASE WHEN dem_age >= 5 AND mpk_kbli_value IS NOT NULL AND dem_edl_value IS NOT NULL AND ((mpk_kbli_value >= 64110 AND mpk_kbli_value <= 64124) OR (mpk_kbli_value >= 84111 AND mpk_kbli_value <= 84234) OR mpk_kbli_value = 99000) AND dem_edl_value < 2 THEN 1 ELSE 0 END AS N3,

        -- ==========================================
        -- BLOK ANOMALI O
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND mjj_kbli_value IS NOT NULL AND mjjemprel1_value IS NOT NULL AND mjj_emprel_value IS NOT NULL AND mju_ins_value IS NOT NULL AND mjj_kbji_value IN (1111, 1112, 2612, 3351, 3352, 3353, 3354, 3359, 5411, 5413) AND (mjj_kbli_value < 84111 OR mjj_kbli_value > 84300 OR mjjemprel1_value = 2 OR mjj_emprel_value IN (2, 3, 5) OR mju_ins_value <> 1) THEN 1 ELSE 0 END AS O1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND sjj_kbli_value IS NOT NULL AND sjjemprel1_value IS NOT NULL AND sjj_emprel_value IS NOT NULL AND sjj_kbji_value IN (1111, 1112, 2612, 3351, 3352, 3353, 3354, 3359, 5411, 5413) AND (sjj_kbli_value < 84111 OR sjj_kbli_value > 84300 OR sjjemprel1_value = 2 OR sjj_emprel_value IN (2, 3, 5)) THEN 1 ELSE 0 END AS O2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND mpk_kbli_value IS NOT NULL AND mpk_status_value IS NOT NULL AND mpk_kbji_value IN (1111, 1112, 2612, 3351, 3352, 3353, 3354, 3359, 5411, 5413) AND (mpk_kbli_value < 84111 OR mpk_kbli_value > 84300 OR mpk_status_value IN (1, 2, 3, 5, 6, 7, 9)) THEN 1 ELSE 0 END AS O3,

        -- ==========================================
        -- BLOK ANOMALI P
        -- ==========================================
        CASE WHEN dem_age >= 5 AND dem_age < 15 AND mjj_kbji_value IS NOT NULL AND ((mjj_kbji_value >= 1111 AND mjj_kbji_value <= 1431) OR (mjj_kbji_value >= 2111 AND mjj_kbji_value <= 2356) OR (mjj_kbji_value >= 2411 AND mjj_kbji_value <= 2643) OR (mjj_kbji_value >= 3111 AND mjj_kbji_value <= 3413)) THEN 1 ELSE 0 END AS P1,
        CASE WHEN dem_age >= 5 AND dem_age < 15 AND sjj_kbji_value IS NOT NULL AND ((sjj_kbji_value >= 1111 AND sjj_kbji_value <= 1431) OR (sjj_kbji_value >= 2111 AND sjj_kbji_value <= 2356) OR (sjj_kbji_value >= 2411 AND sjj_kbji_value <= 2643) OR (sjj_kbji_value >= 3111 AND sjj_kbji_value <= 3413)) THEN 1 ELSE 0 END AS P2,
        CASE WHEN dem_age >= 5 AND dem_age < 15 AND mpk_kbji_value IS NOT NULL AND ((mpk_kbji_value >= 1111 AND mpk_kbji_value <= 1431) OR (mpk_kbji_value >= 2111 AND mpk_kbji_value <= 2356) OR (mpk_kbji_value >= 2411 AND mpk_kbji_value <= 2643) OR (mpk_kbji_value >= 3111 AND mpk_kbji_value <= 3413)) THEN 1 ELSE 0 END AS P3,

        -- ==========================================
        -- BLOK ANOMALI Q
        -- ==========================================
        CASE WHEN dem_age >= 5 AND mjj_kbji_value IS NOT NULL AND dem_edl_value IS NOT NULL AND (mjj_kbji_value >= 1113 AND mjj_kbji_value <= 1431) AND dem_edl_value < 2 THEN 1 ELSE 0 END AS Q1,
        CASE WHEN dem_age >= 5 AND sjj_kbji_value IS NOT NULL AND dem_edl_value IS NOT NULL AND (sjj_kbji_value >= 1113 AND sjj_kbji_value <= 1431) AND dem_edl_value < 2 THEN 1 ELSE 0 END AS Q2,
        CASE WHEN dem_age >= 5 AND mpk_kbji_value IS NOT NULL AND dem_edl_value IS NOT NULL AND (mpk_kbji_value >= 1113 AND mpk_kbji_value <= 1431) AND dem_edl_value < 2 THEN 1 ELSE 0 END AS Q3

    FROM tok_3fd42e0e.art_roster art
    LEFT JOIN tok_3fd42e0e.root_table root ON root.assignment_id = art.assignment_id
    LEFT JOIN tok_3fd42e0e.petugas p ON p.assignment_id = root.assignment_id 
    LEFT JOIN tok_3fd42e0e.base_table_assignment base ON base.id = art.assignment_id
    
    WHERE base.is_active = 1 
      -- Filter status diseragamkan dengan semua contoh terakhir (tidak mengikutkan DRAFT dan OPEN)
      AND base.assignment_status_alias NOT IN ('DRAFT', 'OPEN') 
)
SELECT 
    rn,
    KODE_KAB,
    KEC,
    DESA,
    SLS,
    "Kode Wilayah",
    ID_ART,
    KRT,
    nama_art,
    petugas, 

    -- MENGHITUNG TOTAL ANOMALI YANG TERJADI PADA BARIS INI
    (A1 + A2 + A3 + B1 + B2 + B3 + C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8 + C9 + C10 + 
     D1 + D2 + D3 + E1 + E2 + E3 + F1 + F2 + F3 + G1 + G2 + G3 + H1 + H2 + H3 + 
     I1 + I2 + I3 + J1 + J2 + J3 + K1 + K2 + K3 + L1 + L2 + L3 + M1 + M2 + M3 + 
     N1 + N2 + N3 + O1 + O2 + O3 + P1 + P2 + P3 + Q1 + Q2 + Q3) AS jumlah_anomali,
    
    -- MENGGABUNGKAN STRING NAMA ANOMALI
    -- Menggunakan trick LTRIM(STUFF(.., 1, 1, '')) agar koma paling depan otomatis terhapus
    LTRIM(STUFF(CONCAT(
        CASE WHEN A1 = 1 THEN ',A1' ELSE '' END,
        CASE WHEN A2 = 1 THEN ',A2' ELSE '' END,
        CASE WHEN A3 = 1 THEN ',A3' ELSE '' END,
        CASE WHEN B1 = 1 THEN ',B1' ELSE '' END,
        CASE WHEN B2 = 1 THEN ',B2' ELSE '' END,
        CASE WHEN B3 = 1 THEN ',B3' ELSE '' END,
        CASE WHEN C1 = 1 THEN ',C1' ELSE '' END,
        CASE WHEN C2 = 1 THEN ',C2' ELSE '' END,
        CASE WHEN C3 = 1 THEN ',C3' ELSE '' END,
        CASE WHEN C4 = 1 THEN ',C4' ELSE '' END,
        CASE WHEN C5 = 1 THEN ',C5' ELSE '' END,
        CASE WHEN C6 = 1 THEN ',C6' ELSE '' END,
        CASE WHEN C7 = 1 THEN ',C7' ELSE '' END,
        CASE WHEN C8 = 1 THEN ',C8' ELSE '' END,
        CASE WHEN C9 = 1 THEN ',C9' ELSE '' END,
        CASE WHEN C10= 1 THEN ',C10' ELSE '' END,
        CASE WHEN D1 = 1 THEN ',D1' ELSE '' END,
        CASE WHEN D2 = 1 THEN ',D2' ELSE '' END,
        CASE WHEN D3 = 1 THEN ',D3' ELSE '' END,
        CASE WHEN E1 = 1 THEN ',E1' ELSE '' END,
        CASE WHEN E2 = 1 THEN ',E2' ELSE '' END,
        CASE WHEN E3 = 1 THEN ',E3' ELSE '' END,
        CASE WHEN F1 = 1 THEN ',F1' ELSE '' END,
        CASE WHEN F2 = 1 THEN ',F2' ELSE '' END,
        CASE WHEN F3 = 1 THEN ',F3' ELSE '' END,
        CASE WHEN G1 = 1 THEN ',G1' ELSE '' END,
        CASE WHEN G2 = 1 THEN ',G2' ELSE '' END,
        CASE WHEN G3 = 1 THEN ',G3' ELSE '' END,
        CASE WHEN H1 = 1 THEN ',H1' ELSE '' END,
        CASE WHEN H2 = 1 THEN ',H2' ELSE '' END,
        CASE WHEN H3 = 1 THEN ',H3' ELSE '' END,
        CASE WHEN I1 = 1 THEN ',I1' ELSE '' END,
        CASE WHEN I2 = 1 THEN ',I2' ELSE '' END,
        CASE WHEN I3 = 1 THEN ',I3' ELSE '' END,
        CASE WHEN J1 = 1 THEN ',J1' ELSE '' END,
        CASE WHEN J2 = 1 THEN ',J2' ELSE '' END,
        CASE WHEN J3 = 1 THEN ',J3' ELSE '' END,
        CASE WHEN K1 = 1 THEN ',K1' ELSE '' END,
        CASE WHEN K2 = 1 THEN ',K2' ELSE '' END,
        CASE WHEN K3 = 1 THEN ',K3' ELSE '' END,
        CASE WHEN L1 = 1 THEN ',L1' ELSE '' END,
        CASE WHEN L2 = 1 THEN ',L2' ELSE '' END,
        CASE WHEN L3 = 1 THEN ',L3' ELSE '' END,
        CASE WHEN M1 = 1 THEN ',M1' ELSE '' END,
        CASE WHEN M2 = 1 THEN ',M2' ELSE '' END,
        CASE WHEN M3 = 1 THEN ',M3' ELSE '' END,
        CASE WHEN N1 = 1 THEN ',N1' ELSE '' END,
        CASE WHEN N2 = 1 THEN ',N2' ELSE '' END,
        CASE WHEN N3 = 1 THEN ',N3' ELSE '' END,
        CASE WHEN O1 = 1 THEN ',O1' ELSE '' END,
        CASE WHEN O2 = 1 THEN ',O2' ELSE '' END,
        CASE WHEN O3 = 1 THEN ',O3' ELSE '' END,
        CASE WHEN P1 = 1 THEN ',P1' ELSE '' END,
        CASE WHEN P2 = 1 THEN ',P2' ELSE '' END,
        CASE WHEN P3 = 1 THEN ',P3' ELSE '' END,
        CASE WHEN Q1 = 1 THEN ',Q1' ELSE '' END,
        CASE WHEN Q2 = 1 THEN ',Q2' ELSE '' END,
        CASE WHEN Q3 = 1 THEN ',Q3' ELSE '' END
    ), 1, 1, '')) AS daftar_anomali,
    
    catatan, Link

FROM Data_Anomali
where (A1 + A2 + A3 + B1 + B2 + B3 + C1 + C2 + C3 + C4 + C5 + C6 + C7 + C8 + C9 + C10 + 
     D1 + D2 + D3 + E1 + E2 + E3 + F1 + F2 + F3 + G1 + G2 + G3 + H1 + H2 + H3 + 
     I1 + I2 + I3 + J1 + J2 + J3 + K1 + K2 + K3 + L1 + L2 + L3 + M1 + M2 + M3 + 
     N1 + N2 + N3 + O1 + O2 + O3 + P1 + P2 + P3 + Q1 + Q2 + Q3) > 0
