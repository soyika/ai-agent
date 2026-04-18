from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import WriteApi, QueryApi
from app.core.config import settings


class InfluxDBAdapter:
    def __init__(self):
        self._client = None
        self._write_api = None
        self._query_api = None

    def _initialize(self):
        if self._client is None:
            self._client = InfluxDBClient(
                url=settings.INFLUXDB_URL,
                token=settings.INFLUXDB_TOKEN,
                org=settings.INFLUXDB_ORG,
            )
            self._write_api = self._client.write_api()
            self._query_api = self._client.query_api()

    async def write_sensor_data(self, sensor_data: dict):
        self._initialize()
        point = (
            Point("sensor_data")
            .tag("device_id", sensor_data.get("device_id", "unknown"))
            .tag("sensor_type", sensor_data.get("sensor_type", "unknown"))
            .field("value", sensor_data.get("value", 0))
        )
        for key in ["temperature", "humidity", "soil_moisture", "light", "co2"]:
            if key in sensor_data:
                point.field(key, sensor_data[key])
        self._write_api.write(bucket=settings.INFLUXDB_BUCKET, record=point)

    async def query_sensor_data(self, device_id: str, hours: int = 24) -> list[dict]:
        self._initialize()
        query = f'''
            from(bucket: "{settings.INFLUXDB_BUCKET}")
            |> range(start: -{hours}h)
            |> filter(fn: (r) => r["_measurement"] == "sensor_data")
            |> filter(fn: (r) => r["device_id"] == "{device_id}")
        '''
        tables = self._query_api.query(query)
        results = []
        for table in tables:
            for record in table.records:
                results.append({
                    "time": record.get_time().isoformat(),
                    "value": record.get_value(),
                    **record.values,
                })
        return results


influxdb_adapter = InfluxDBAdapter()
