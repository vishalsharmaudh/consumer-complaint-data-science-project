-- Question 1
-- How many complaints are present in the dataset?

SELECT COUNT(*) AS total_complaints
FROM complaints;


-- Question 2
-- Are complaint IDs unique?

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT complaint_id) AS unique_complaint_ids
FROM complaints;


-- Question 3
-- Which important columns contain missing values?

SELECT
    COUNT(*) FILTER (WHERE company_response_to_consumer IS NULL) AS missing_company_response,
    COUNT(*) FILTER (WHERE consumer_complaint_narrative IS NULL) AS missing_narrative,
    COUNT(*) FILTER (WHERE state IS NULL) AS missing_state,
    COUNT(*) FILTER (WHERE company IS NULL) AS missing_company
FROM complaints;
-- ============================================================
-- 2. COMPLAINT VOLUME & TRENDS
-- ============================================================

-- Question 4
-- Which products receive the most complaints?

SELECT
    product,
    COUNT(*) AS complaint_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS complaint_share_pct
FROM complaints
GROUP BY product
ORDER BY complaint_count DESC;


-- Question 5
-- Which states have the highest number of complaints?

SELECT
    state,
    COUNT(*) AS complaint_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS complaint_share_pct
FROM complaints
GROUP BY state
ORDER BY complaint_count DESC
LIMIT 10;


-- Question 6
-- How has complaint volume changed over time?

SELECT
    EXTRACT(YEAR FROM date_received)::INT AS complaint_year,
    COUNT(*) AS complaint_count
FROM complaints
WHERE date_received IS NOT NULL
GROUP BY complaint_year
ORDER BY complaint_year;

-- ============================================================
-- 3. PRODUCT & ISSUE ANALYSIS
-- ============================================================

-- Question 7
-- What are the most common complaint issues?

SELECT
    issue,
    COUNT(*) AS complaint_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS complaint_share_pct
FROM complaints
WHERE issue IS NOT NULL
GROUP BY issue
ORDER BY complaint_count DESC
LIMIT 10;


-- Question 8
-- What are the most common issues within each product?

WITH issue_counts AS (
    SELECT
        product,
        issue,
        COUNT(*) AS complaint_count,
        ROW_NUMBER() OVER (
            PARTITION BY product
            ORDER BY COUNT(*) DESC
        ) AS issue_rank
    FROM complaints
    WHERE product IS NOT NULL
      AND issue IS NOT NULL
    GROUP BY product, issue
)
SELECT
    product,
    issue,
    complaint_count
FROM issue_counts
WHERE issue_rank <= 3
ORDER BY product, complaint_count DESC;


-- Question 9
-- Which products have the highest average number of complaints per company?

SELECT
    product,
    COUNT(*) AS complaint_count,
    COUNT(DISTINCT company) AS company_count,
    ROUND(
        COUNT(*)::NUMERIC / NULLIF(COUNT(DISTINCT company), 0),
        2
    ) AS avg_complaints_per_company
FROM complaints
WHERE product IS NOT NULL
  AND company IS NOT NULL
GROUP BY product
HAVING COUNT(*) >= 500
ORDER BY avg_complaints_per_company DESC;

-- ============================================================
-- 4. COMPANY ANALYSIS
-- ============================================================

-- Question 10
-- Which companies receive the most complaints?

SELECT
    company,
    COUNT(*) AS complaint_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS complaint_share_pct
FROM complaints
WHERE company IS NOT NULL
GROUP BY company
ORDER BY complaint_count DESC
LIMIT 10;


-- Question 11
-- Which companies have the highest average response time,
-- considering only companies with at least 500 complaints?

SELECT
    company,
    COUNT(*) AS complaint_count,
    ROUND(
        AVG(date_sent_to_company - date_received)::NUMERIC,
        2
    ) AS avg_response_days
FROM complaints
WHERE company IS NOT NULL
  AND date_received IS NOT NULL
  AND date_sent_to_company IS NOT NULL
GROUP BY company
HAVING COUNT(*) >= 500
ORDER BY avg_response_days DESC
LIMIT 10;


-- Question 12
-- Which companies have the highest percentage of responses
-- taking more than 7 days, considering companies with at least
-- 100 valid responses?

SELECT
    company,
    COUNT(*) AS complaint_count,
    COUNT(*) FILTER (
        WHERE date_sent_to_company - date_received > 7
    ) AS delayed_over_7_days,
    ROUND(
        COUNT(*) FILTER (
            WHERE date_sent_to_company - date_received > 7
        ) * 100.0 / COUNT(*),
        2
    ) AS delayed_over_7_days_pct
FROM complaints
WHERE company IS NOT NULL
  AND date_received IS NOT NULL
  AND date_sent_to_company IS NOT NULL
GROUP BY company
HAVING COUNT(*) >= 100
ORDER BY delayed_over_7_days_pct DESC
LIMIT 10;

-- ============================================================
-- 5. RESPONSE OUTCOME ANALYSIS
-- ============================================================

-- Question 13
-- What is the overall distribution of complaint outcomes?

SELECT
    company_response_to_consumer AS response_outcome,
    COUNT(*) AS complaint_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS outcome_share_pct
FROM complaints
GROUP BY company_response_to_consumer
ORDER BY complaint_count DESC;


-- Question 14
-- How does complaint outcome vary across products?

SELECT
    product,
    company_response_to_consumer AS response_outcome,
    COUNT(*) AS complaint_count,
    ROUND(
        COUNT(*) * 100.0
        / SUM(COUNT(*)) OVER (PARTITION BY product),
        2
    ) AS outcome_share_pct
FROM complaints
WHERE product IS NOT NULL
  AND company_response_to_consumer IS NOT NULL
GROUP BY product, company_response_to_consumer
ORDER BY product, complaint_count DESC;


-- Question 15
-- Which products have the highest percentage of untimely responses?

SELECT
    product,
    COUNT(*) AS complaint_count,
    COUNT(*) FILTER (
        WHERE company_response_to_consumer = 'Untimely response'
    ) AS untimely_complaints,
    ROUND(
        COUNT(*) FILTER (
            WHERE company_response_to_consumer = 'Untimely response'
        ) * 100.0 / COUNT(*),
        2
    ) AS untimely_response_pct
FROM complaints
WHERE product IS NOT NULL
  AND company_response_to_consumer IS NOT NULL
GROUP BY product
HAVING COUNT(*) >= 500
ORDER BY untimely_response_pct DESC;

-- ============================================================
-- 6. RESPONSE-TIME ANALYSIS
-- ============================================================

-- Question 16
-- What is the overall average response time and percentage
-- of responses taking more than 7 days?

SELECT
    COUNT(*) AS valid_responses,
    ROUND(
        AVG(date_sent_to_company - date_received)::NUMERIC,
        2
    ) AS avg_response_days,
    COUNT(*) FILTER (
        WHERE date_sent_to_company - date_received > 7
    ) AS responses_over_7_days,
    ROUND(
        COUNT(*) FILTER (
            WHERE date_sent_to_company - date_received > 7
        ) * 100.0 / COUNT(*),
        2
    ) AS over_7_days_pct
FROM complaints
WHERE date_received IS NOT NULL
  AND date_sent_to_company IS NOT NULL;


-- Question 17
-- How does average response time vary by complaint outcome?

SELECT
    company_response_to_consumer AS response_outcome,
    COUNT(*) AS complaint_count,
    ROUND(
        AVG(date_sent_to_company - date_received)::NUMERIC,
        2
    ) AS avg_response_days
FROM complaints
WHERE company_response_to_consumer IS NOT NULL
  AND date_received IS NOT NULL
  AND date_sent_to_company IS NOT NULL
GROUP BY company_response_to_consumer
ORDER BY avg_response_days DESC;


-- Question 18
-- How does average response time change over time?

SELECT
    DATE_TRUNC('month', date_received)::DATE AS complaint_month,
    COUNT(*) AS complaint_count,
    ROUND(
        AVG(date_sent_to_company - date_received)::NUMERIC,
        2
    ) AS avg_response_days
FROM complaints
WHERE date_received IS NOT NULL
  AND date_sent_to_company IS NOT NULL
GROUP BY complaint_month
ORDER BY complaint_month;

-- ============================================================
-- 7. ADVANCED SQL INSIGHTS
-- ============================================================

-- Question 19
-- How does monthly complaint volume change compared with
-- the previous month?

WITH monthly_complaints AS (
    SELECT
        DATE_TRUNC('month', date_received)::DATE AS complaint_month,
        COUNT(*) AS complaint_count
    FROM complaints
    WHERE date_received IS NOT NULL
    GROUP BY complaint_month
)
SELECT
    complaint_month,
    complaint_count,
    LAG(complaint_count) OVER (
        ORDER BY complaint_month
    ) AS previous_month_count,
    ROUND(
        (
            complaint_count
            - LAG(complaint_count) OVER (ORDER BY complaint_month)
        ) * 100.0
        / NULLIF(
            LAG(complaint_count) OVER (ORDER BY complaint_month),
            0
        ),
        2
    ) AS month_over_month_growth_pct
FROM monthly_complaints
ORDER BY complaint_month;

-- Question 20
-- Which companies were among the top 3 complaint recipients
-- in each month?

WITH monthly_company_counts AS (
    SELECT
        DATE_TRUNC('month', date_received)::DATE AS complaint_month,
        company,
        COUNT(*) AS complaint_count
    FROM complaints
    WHERE date_received IS NOT NULL
      AND company IS NOT NULL
    GROUP BY complaint_month, company
),
ranked_companies AS (
    SELECT
        complaint_month,
        company,
        complaint_count,
        RANK() OVER (
            PARTITION BY complaint_month
            ORDER BY complaint_count DESC
        ) AS company_rank
    FROM monthly_company_counts
)
SELECT
    complaint_month,
    company,
    complaint_count,
    company_rank
FROM ranked_companies
WHERE company_rank <= 3
ORDER BY complaint_month, company_rank;

-- Question 21
-- What is the overall timely vs. untimely response rate?

SELECT
    timely_response,
    COUNT(*) AS complaint_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS share_pct
FROM complaints
WHERE timely_response IS NOT NULL
GROUP BY timely_response
ORDER BY complaint_count DESC;


-- Question 22
-- Which products have the highest untimely-response rate
-- (per timely_response, not company_response_to_consumer)?

SELECT
    product,
    COUNT(*) AS complaint_count,
    COUNT(*) FILTER (WHERE timely_response = 'No') AS untimely_count,
    ROUND(
        COUNT(*) FILTER (WHERE timely_response = 'No') * 100.0 / COUNT(*),
        2
    ) AS untimely_pct
FROM complaints
WHERE product IS NOT NULL
  AND timely_response IS NOT NULL
GROUP BY product
HAVING COUNT(*) >= 500
ORDER BY untimely_pct DESC;


-- Question 23
-- Which submission channels have the highest untimely-response rate?

SELECT
    submitted_via,
    COUNT(*) AS complaint_count,
    COUNT(*) FILTER (WHERE timely_response = 'No') AS untimely_count,
    ROUND(
        COUNT(*) FILTER (WHERE timely_response = 'No') * 100.0 / COUNT(*),
        2
    ) AS untimely_pct
FROM complaints
WHERE submitted_via IS NOT NULL
  AND timely_response IS NOT NULL
GROUP BY submitted_via
HAVING COUNT(*) >= 100
ORDER BY untimely_pct DESC;


-- Question 24
-- Which states have the highest untimely-response rate?
-- (Mirrors the EDA finding: Indiana, Connecticut, Washington highest;
-- Mississippi, South Carolina lowest, among high-volume states.)

SELECT
    state,
    COUNT(*) AS complaint_count,
    COUNT(*) FILTER (WHERE timely_response = 'No') AS untimely_count,
    ROUND(
        COUNT(*) FILTER (WHERE timely_response = 'No') * 100.0 / COUNT(*),
        2
    ) AS untimely_pct
FROM complaints
WHERE state IS NOT NULL
  AND timely_response IS NOT NULL
GROUP BY state
HAVING COUNT(*) >= 500
ORDER BY untimely_pct DESC;

-- Question 25
-- Confirming the leakage relationship found in EDA: how does
-- company_response_to_consumer align with timely_response?

SELECT
    company_response_to_consumer AS response_outcome,
    timely_response,
    COUNT(*) AS complaint_count
FROM complaints
WHERE company_response_to_consumer IS NOT NULL
  AND timely_response IS NOT NULL
GROUP BY company_response_to_consumer, timely_response
ORDER BY company_response_to_consumer, complaint_count DESC;