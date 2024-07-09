-- Create the following measures for metrics calculation. 
-- Sales Amount 
-- Cost of goods sold (COGS)
-- Return Amount 
-- Profit Amount 
-- Profit Margin 
CREATE VIEW sales AS
SELECT
    *,
    (MSRP * SalesQuantity) as SaleAmount,
    (UnitCost * SalesQuantity) as COGS,
    (MSRP * ReturnQuantity) as ReturnAmount,
    (
        (MSRP * SalesQuantity) - (UnitCost * SalesQuantity) - (MSRP * ReturnQuantity)
    ) as ProfitAmount,
    (
        (
            (MSRP * SalesQuantity) - (UnitCost * SalesQuantity) - (MSRP * ReturnQuantity)
        ) /(MSRP * SalesQuantity)
    ) as ProfitMargin
FROM
    factsales
ORDER BY
    SalesKey;

-- Merge all products dimension tables to one to enable creating hierachy for visuals 
CREATE VIEW products AS
SELECT
    p.*,
    pc.ProductCategoryKey,
    pc.ProductCategoryLabel,
    pc.ProductCategoryName,
    ps.ProductSubcategoryLabel,
    ps.ProductSubcategoryName
FROM
    product p
    LEFT JOIN productsubcategory ps ON p.ProductSubcategoryKey = ps.ProductSubcategoryKey
    LEFT JOIN productcategory pc ON ps.ProductCategoryKey = pc.ProductCategoryKey
WHERE
    pc.ProductCategoryKey NOT IN (7, 8);

-- Create main transaction table for analsis (model table)
CREATE VIEW consoto_store AS
SELECT
    s.SalesKey,
    s.DateKey,
    s.SalesQuantity,
    s.ReturnQuantity,
    s.DiscountQuantity,
    s.SaleAmount,
    s.COGS,
    s.ReturnAmount,
    s.ProfitAmount,
    s.ProfitMargin,
    st.StoreName,
    g.ContinentName,
    g.Region,
    g.States,
    p.ProductName,
    p.ProductCategoryName,
    p.ProductSubcategoryName,
    pr.PromotionName,
    pr.DiscountPercent,
    c.ChannelName
FROM
    sales s
    LEFT JOIN stores st ON s.StoreKey = st.StoreKey
    LEFT JOIN geography g ON st.geographykey = g.geographykey
    LEFT JOIN products p ON s.ProductKey = p.ProductKey
    LEFT JOIN promotion pr ON s.PromotionKey = pr.PromotionKey
    LEFT JOIN channel c ON s.channelKey = c.ChannelKey;

-- Perform data preprocessing
-- Check for duplicates
SELECT
    SALESKEY,
    COUNT(*) as num_duplicates
FROM
    consoto_store
GROUP BY
    SALESKEY
HAVING
    COUNT(*) > 1;

-- Check for null values
SELECT
    "SalesQuantity" as ColumnName,
    COUNT(*) as null_count
FROM
    consoto_store
WHERE
    SalesQuantity IS NULL
UNION
SELECT
    "SaleAmount" as ColumnName,
    COUNT(*) as null_count
FROM
    consoto_store
WHERE
    SaleAmount IS NULL
UNION
SELECT
    "ProfitAmount" as ColumnName,
    COUNT(*) as null_count
FROM
    consoto_store
WHERE
    ProfitAmount IS NULL;

-- Exploratory Data Analysis (Question based)
-- Calculate gross and net revenue
SELECT
    SUM(SaleAmount) as "Gross Revenue",
    (SUM(SaleAmount) - SUM(ReturnAmount)) as "Net Revenue"
FROM
    consoto_store;

-- Which days that typically have the highest number of transactions.
SELECT
    Day_Name AS Days,
    COUNT(SalesKey) AS Transactions
FROM
    consoto_store
GROUP BY
    Day_Name
ORDER BY
    2 DESC;