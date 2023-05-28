from databuri.datasources import Air4Thai

Api = Air4Thai()
df = Api.fetch(
    stations=[],
    measurements=[],
    sdate='2019-01-01',
    edate='2019-02-03',
)

print(df)