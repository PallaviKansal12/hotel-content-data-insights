-- 1) Risk distribution overview
SELECT
    risk_level,
    COUNT(*) AS hotels_evaluated
FROM content_evaluation_results
GROUP BY risk_level
ORDER BY CASE risk_level
    WHEN 'LOW' THEN 1
    WHEN 'MEDIUM' THEN 2
    WHEN 'HIGH' THEN 3
    ELSE 4
END;

-- 2) Human review workload
SELECT
    SUM(CASE WHEN human_review_required = TRUE THEN 1 ELSE 0 END) AS hotels_needing_review,
    ROUND(100.0 * SUM(CASE WHEN human_review_required = TRUE THEN 1 ELSE 0 END) / COUNT(*), 2) AS review_share_percent
FROM content_evaluation_results;

-- 3) Most common issue types
SELECT
    TRIM(value) AS issue_type,
    COUNT(*) AS occurrences
FROM (
    SELECT UNNEST(STRING_TO_ARRAY(unsupported_claims, ' | ')) AS value
    FROM content_evaluation_results
    WHERE unsupported_claims IS NOT NULL AND unsupported_claims <> ''
) t
WHERE TRIM(value) <> ''
GROUP BY TRIM(value)
ORDER BY occurrences DESC;

-- 4) Average confidence by risk level
SELECT
    risk_level,
    ROUND(AVG(confidence) * 100, 2) AS avg_confidence_percent
FROM content_evaluation_results
GROUP BY risk_level
ORDER BY CASE risk_level
    WHEN 'LOW' THEN 1
    WHEN 'MEDIUM' THEN 2
    WHEN 'HIGH' THEN 3
    ELSE 4
END;

-- 5) Hotels requiring intervention
SELECT
    hotel_name,
    risk_level,
    unsupported_claim_count,
    confidence
FROM content_evaluation_results
WHERE human_review_required = TRUE
ORDER BY unsupported_claim_count DESC, confidence ASC;
