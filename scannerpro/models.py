from django.db import models, connection

class TickerBase(models.Model):
    # Constants for market cap choices
    LARGE_CAP = 'Large Cap'
    MID_CAP = 'Mid Cap'
    SMALL_CAP = 'Small Cap'

    MARKET_CAP_CHOICES = [
        (LARGE_CAP, 'Large Cap'),
        (MID_CAP, 'Mid Cap'),
        (SMALL_CAP, 'Small Cap'),
    ]

    # Constants for sector choices
    AUTOMOBILE = 'Automobile'
    BANKING = 'Banking'
    CAPITAL_GOODS = 'Capital Goods'
    CEMENT = 'Cement'
    CHEMICALS = 'Chemicals'
    FINANCE = 'Finance'
    FMCG = 'FMCG'
    INDEX = 'Index'
    INFRASTRUCTURE = 'Infrastructure'
    MEDIA = 'Media'
    METALS = 'Metals'
    OIL_AND_GAS = 'Oil and Gas'
    PHARMA = 'Pharma'
    POWER = 'Power'
    REALTY = 'Realty'
    TECHNOLOGY = 'Technology'
    TELECOM = 'Telecom'
    TEXTILE = 'Textile'
    OTHERS = 'Others'

    SECTOR_CHOICES = [
        (AUTOMOBILE, 'Automobile'),
        (BANKING, 'Banking'),
        (CAPITAL_GOODS, 'Capital Goods'),
        (CEMENT, 'Cement'),
        (CHEMICALS, 'Chemicals'),
        (FINANCE, 'Finance'),
        (FMCG, 'FMCG'),
        (INDEX, 'Index'),
        (INFRASTRUCTURE, 'Infrastructure'),
        (MEDIA, 'Media'),
        (METALS, 'Metals'),
        (OIL_AND_GAS, 'Oil and Gas'),
        (PHARMA, 'Pharma'),
        (POWER, 'Power'),
        (REALTY, 'Realty'),
        (TECHNOLOGY, 'Technology'),
        (TELECOM, 'Telecom'),
        (TEXTILE, 'Textile'),
        (OTHERS, 'Others'),
    ]

    ticker_name = models.CharField(max_length=200, unique=True)
    ticker_symbol = models.CharField(max_length=20, unique=True)
    ticker_sector = models.CharField(
        max_length=50,
        choices=SECTOR_CHOICES,
        default=OTHERS,
    )
    ticker_sub_sector = models.CharField(max_length=100, blank=True, null=True)
    ticker_market_cap = models.CharField(
        max_length=20,
        choices=MARKET_CAP_CHOICES,
        default=LARGE_CAP,
    )

    def __str__(self):
        return f"{self.ticker_symbol} ({self.ticker_sector}) - {self.ticker_market_cap}"

    def save(self, *args, **kwargs):
        # Call the original save method to insert the TickerBase record
        super().save(*args, **kwargs)
        
        # Get the table name (using ticker_name or ticker_symbol)
        table_name = self.ticker_symbol.lower()
        
        # Create SQL query to create the new table dynamically
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS "{table_name}" (
            id SERIAL PRIMARY KEY,
            date DATE NOT NULL,
            open_price FLOAT NOT NULL,
            high_price FLOAT NOT NULL,
            low_price FLOAT NOT NULL,
            close_price FLOAT NOT NULL,
            volume BIGINT
        )
        """
        
        # Execute the query to create the table
        with connection.cursor() as cursor:
            cursor.execute(create_table_query)


from django.db import models

class StockData(models.Model):
    symbol = models.CharField(max_length=100)
    ltp = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.ltp} at {self.timestamp}"
